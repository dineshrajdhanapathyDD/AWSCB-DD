#!/usr/bin/env python3
"""
AWS Learning Assistant
---------------------
This script fetches the latest AWS updates from blogs and RSS feeds,
summarizes the top 3 updates, and creates quiz questions based on the content.
The results are then sent via email.
"""

import feedparser
import requests
import smtplib
import random
import datetime
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Import Bedrock enhancement if available
try:
    from bedrock_enhancement import generate_summary, generate_quiz_question
    BEDROCK_AVAILABLE = True
    print("Amazon Bedrock enhancement is available and will be used.")
except (ImportError, Exception) as e:
    BEDROCK_AVAILABLE = False
    print(f"Amazon Bedrock enhancement is not available: {e}")
    print("Falling back to basic summarization and quiz generation.")

# Load environment variables from .env file
load_dotenv()

# Try to import the learning tracker
try:
    from learning_tracker import LearningTracker
    TRACKER_AVAILABLE = True
    tracker = LearningTracker()
    print("Learning tracker is available and will be used.")
except (ImportError, Exception) as e:
    TRACKER_AVAILABLE = False
    print(f"Learning tracker is not available: {e}")
    print("Learning progress will not be tracked.")

# Configuration
AWS_WHATS_NEW_RSS = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
AWS_BLOG_RSS = "https://aws.amazon.com/blogs/aws/feed/"
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def fetch_rss_feed(url):
    """Fetch and parse an RSS feed."""
    feed = feedparser.parse(url)
    return feed.entries

def extract_content(entry):
    """Extract title, link, and summary from an RSS entry."""
    return {
        "title": entry.title,
        "link": entry.link,
        "summary": BeautifulSoup(entry.summary, "html.parser").get_text() if hasattr(entry, "summary") else "",
        "published": entry.published if hasattr(entry, "published") else "",
    }

def get_latest_updates():
    """Get the latest updates from AWS blogs and What's New feed."""
    whats_new_entries = fetch_rss_feed(AWS_WHATS_NEW_RSS)
    blog_entries = fetch_rss_feed(AWS_BLOG_RSS)
    
    # Combine and sort by publication date (most recent first)
    all_entries = []
    for entry in whats_new_entries + blog_entries:
        content = extract_content(entry)
        all_entries.append(content)
    
    # Sort by publication date (assuming entries have a 'published' field)
    # Take the top 10 entries for further processing
    return all_entries[:10]

def summarize_updates(updates, count=3):
    """Summarize the top updates."""
    summaries = []
    
    for update in updates[:count]:
        if BEDROCK_AVAILABLE:
            # Use Bedrock to generate a better summary
            try:
                update_copy = update.copy()
                update_copy['summary'] = generate_summary(update['summary'])
                summaries.append(update_copy)
            except Exception as e:
                print(f"Error using Bedrock for summarization: {e}")
                # Fall back to the original summary
                summaries.append(update)
        else:
            # Just use the original summary
            summaries.append(update)
    
    return summaries

def create_quiz_question(update):
    """Create a quiz question based on an update."""
    if BEDROCK_AVAILABLE:
        try:
            # Use Bedrock to generate a better quiz question
            return generate_quiz_question(update)
        except Exception as e:
            print(f"Error using Bedrock for quiz generation: {e}")
            # Fall back to basic quiz generation
    
    # Basic quiz generation (fallback)
    question = f"What is the main benefit of the new feature described in '{update['title']}'?"
    
    # Generate some plausible options
    options = [
        "Improved performance",
        "Cost reduction",
        "Enhanced security",
        "Better user experience"
    ]
    
    # Randomly select a correct answer
    correct_index = random.randint(0, len(options) - 1)
    
    return {
        "question": question,
        "options": options,
        "correct_answer": options[correct_index],
        "correct_index": correct_index,
        "source": update["link"]
    }

def format_email_content(summaries, quiz_question):
    """Format the email content with summaries and quiz question."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #232F3E; color: white; padding: 10px; text-align: center; }}
            .summary {{ margin: 20px 0; padding: 10px; border-left: 4px solid #FF9900; }}
            .quiz {{ background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            .options {{ margin-left: 20px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 0.8em; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your AWS Daily Learning - {today}</h1>
            </div>
            
            <h2>Top AWS Updates Today</h2>
    """
    
    for i, summary in enumerate(summaries, 1):
        html += f"""
            <div class="summary">
                <h3>{i}. {summary['title']}</h3>
                <p>{summary['summary'][:200]}...</p>
                <p><a href="{summary['link']}">Read more</a></p>
            </div>
        """
    
    html += f"""
            <div class="quiz">
                <h2>Today's Quiz Question</h2>
                <p><strong>{quiz_question['question']}</strong></p>
                <div class="options">
    """
    
    for i, option in enumerate(quiz_question['options']):
        html += f"                <p>{chr(65+i)}. {option}</p>\n"
    
    html += f"""
                </div>
                <p><em>The answer will be revealed in tomorrow's email!</em></p>
                <p>Source: <a href="{quiz_question['source']}">Read the article</a></p>
            </div>
            
            <div class="footer">
                <p>This email was automatically generated by your AWS Learning Assistant.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(subject, html_content):
    """Send an email with the given subject and HTML content."""
    if not all([EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT]):
        print("Email configuration is incomplete. Please check your .env file.")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main():
    """Main function to run the AWS Learning Assistant."""
    print("Fetching latest AWS updates...")
    updates = get_latest_updates()
    
    print(f"Found {len(updates)} updates. Summarizing...")
    summaries = summarize_updates(updates)
    
    print("Creating quiz question...")
    quiz_question = create_quiz_question(random.choice(summaries))
    
    print("Formatting email content...")
    html_content = format_email_content(summaries, quiz_question)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    subject = f"AWS Daily Learning Update - {today}"
    
    print("Sending email...")
    if send_email(subject, html_content):
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
    
    # Save today's content for reference
    with open(f"aws_learning_{today}.json", "w") as f:
        json.dump({
            "summaries": summaries,
            "quiz_question": quiz_question
        }, f, indent=2)
    
    print(f"Content saved to aws_learning_{today}.json")
    
    # Track learning progress if available
    if TRACKER_AVAILABLE:
        print("Tracking learning progress...")
        for summary in summaries:
            tracker.record_update_read(summary)
        
        # We don't have a user answer yet, so we'll just record that the quiz was generated
        # In a real implementation, you might want to track answers through the web interface
        print("Learning progress tracked.")

if __name__ == "__main__":
    main()
