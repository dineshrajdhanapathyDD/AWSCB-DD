# AWS Learning Assistant

A personal knowledge assistant that automates daily learning with AWS documentation and creates quizzes to help you stay updated with AWS services and features.

## Features

- Curates content from AWS blogs and What's New RSS feeds
- Summarizes the top 3 AWS updates daily
- Creates quiz questions (multiple-choice or flashcards)
- Delivers content via email
- Web interface to view past updates and quiz results
- Learning progress tracking
- Amazon Bedrock integration for better content generation

## Setup Instructions

### Prerequisites

- Python 3.6+
- pip (Python package manager)
- AWS credentials (for Amazon Bedrock integration)

### Installation

1. Clone or download this repository to your local machine.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on the provided `.env.template`:

```bash
cp .env.template .env
```

4. Edit the `.env` file with your email configuration:
   - For Gmail users, you'll need to create an App Password (see [Google's instructions](https://support.google.com/accounts/answer/185833))
   - For other email providers, use the appropriate SMTP server and port

To **set up email sending in your AWS Learning Assistant project for demo purposes**, you’ll need to configure SMTP using either:

1.  **Gmail (App Password)**
    
2.  **Other email provider (like Outlook, Yahoo)**
    

Here’s a **step-by-step guide** for **Gmail**, plus a generic SMTP setup for others — suitable for running your assistant in demo mode:

----------

## ✅ Option 1: Gmail (with App Password)

> ❗ _Google blocks "less secure apps", so you must use an App Password—not your main Gmail password._

### 🔧 Steps:

1.  **Enable 2-Step Verification** on your Google Account  
    Go to: https://myaccount.google.com/security
    
2.  **Create an App Password**
    
    -   Visit: https://myaccount.google.com/apppasswords
        
    -   Choose: **Mail** as the app, **Other** (Custom name like "AWS Assistant")
        
    -   Google will generate a 16-character password — copy it.
        
3.  **Update `.env` file:**
    
    env
    
  
    
    `EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=yourname@gmail.com
    EMAIL_HOST_PASSWORD=your_app_password_here`
   

### Usage

Run the complete assistant (email updates and web interface):

```bash
python run_aws_learning_assistant.py
```

Or run individual components:

```bash
# Just fetch updates and send email
python aws_learning_assistant.py

# Just run the web interface
python web_interface.py
```

### Setting Up Automated Daily Emails

#### On Linux/macOS (using cron)

1. Open your crontab file:

```bash
crontab -e
```

2. Add a line to run the script daily at your preferred time (e.g., 8:00 AM):

```
0 8 * * * cd /path/to/script/directory && /usr/bin/python3 aws_learning_assistant.py
```

#### On Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create a new Basic Task
3. Set the trigger to Daily at your preferred time
4. Set the action to Start a Program
5. Browse to your Python executable (e.g., `C:\Python39\python.exe`)
6. Add the full path to the script as an argument (e.g., `C:\path\to\aws_learning_assistant.py`)

## Components

### 1. Core Assistant (`aws_learning_assistant.py`)
- Fetches content from AWS blogs and What's New RSS feeds
- Summarizes updates
- Creates quiz questions
- Sends email with daily content

### 2. Amazon Bedrock Enhancement (`bedrock_enhancement.py`)
- Uses Amazon Bedrock to generate better summaries
- Creates more relevant quiz questions
- Provides explanations for quiz answers

### 3. Web Interface (`web_interface.py`)
- Flask web application to view past updates
- Answer quiz questions
- Track learning progress
- View learning statistics

### 4. Learning Tracker (`learning_tracker.py`)
- Tracks updates read
- Records quiz answers
- Maintains learning streak
- Provides topic recommendations

## Enhancing the Assistant

1. **Personalization**: Modify the code to focus on specific AWS services or topics
2. **Integration with AWS Services**: Add integration with AWS services like CloudWatch for monitoring
3. **Mobile App**: Create a mobile app for on-the-go learning
4. **Social Features**: Add the ability to share quiz results or compete with friends

## License

This project is licensed under the MIT License - see the LICENSE file for details.
