#!/usr/bin/env python3
"""
AWS Learning Assistant - Web Interface
-------------------------------------
A simple Flask web application to view past AWS updates and quiz results.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import glob
from datetime import datetime

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

app = Flask(__name__)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Create a basic HTML template
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>AWS Learning Assistant</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header {
            background-color: #232F3E;
            color: white;
            padding: 10px 20px;
            margin: -20px -20px 20px;
            border-radius: 5px 5px 0 0;
        }
        .summary {
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #FF9900;
            background-color: #fafafa;
        }
        .quiz {
            background-color: #f0f8ff;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .options {
            margin-left: 20px;
        }
        .correct {
            color: green;
            font-weight: bold;
        }
        .date-selector {
            margin: 20px 0;
        }
        select {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        button {
            padding: 8px 16px;
            background-color: #FF9900;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #e68a00;
        }
        .stats {
            margin-top: 20px;
            padding: 15px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AWS Learning Assistant</h1>
        </div>
        
        <div class="date-selector">
            <form method="GET" action="/">
                <label for="date">Select Date:</label>
                <select name="date" id="date">
                    {% for date in available_dates %}
                        <option value="{{ date }}" {% if date == selected_date %}selected{% endif %}>{{ date }}</option>
                    {% endfor %}
                </select>
                <button type="submit">View</button>
            </form>
        </div>
        
        {% if content %}
            <h2>AWS Updates for {{ selected_date }}</h2>
            
            {% for summary in content.summaries %}
                <div class="summary">
                    <h3>{{ summary.title }}</h3>
                    <p>{{ summary.summary }}</p>
                    <p><a href="{{ summary.link }}" target="_blank">Read more</a></p>
                </div>
            {% endfor %}
            
            <div class="quiz">
                <h2>Quiz Question</h2>
                <p><strong>{{ content.quiz_question.question }}</strong></p>
                <div class="options">
                    {% for option in content.quiz_question.options %}
                        <p {% if option == content.quiz_question.correct_answer %}class="correct"{% endif %}>
                            {{ loop.index | chr }}. {{ option }}
                            {% if option == content.quiz_question.correct_answer %}(Correct Answer){% endif %}
                        </p>
                    {% endfor %}
                </div>
                <p>Source: <a href="{{ content.quiz_question.source }}" target="_blank">Read the article</a></p>
            </div>
            
            {% if stats %}
            <div class="stats">
                <h2>Your Learning Stats</h2>
                <p>Total updates read: {{ stats.total_updates }}</p>
                <p>Quiz questions answered: {{ stats.quizzes_answered }}</p>
                <p>Correct answers: {{ stats.correct_answers }}</p>
                <p>Learning streak: {{ stats.streak }} days</p>
            </div>
            {% endif %}
        {% else %}
            <p>No content available for the selected date.</p>
        {% endif %}
    </div>
</body>
</html>
    """)

# Create a template for the Jinja2 filter
@app.template_filter('chr')
def chr_filter(number):
    return chr(64 + number)  # A=1, B=2, etc.

@app.route('/')
def index():
    # Get all available dates from the JSON files
    json_files = glob.glob('aws_learning_*.json')
    available_dates = [os.path.basename(f).replace('aws_learning_', '').replace('.json', '') for f in json_files]
    available_dates.sort(reverse=True)  # Most recent first
    
    # Get the selected date or default to the most recent
    selected_date = request.args.get('date', available_dates[0] if available_dates else None)
    
    content = None
    if selected_date:
        try:
            with open(f'aws_learning_{selected_date}.json', 'r') as f:
                content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            content = None
    
    # Load learning stats if available
    stats = None
    if TRACKER_AVAILABLE:
        stats = tracker.get_stats()
        
        # Get topic recommendations
        recommendations = tracker.get_topic_recommendations()
    else:
        try:
            with open('learning_stats.json', 'r') as f:
                stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats = {
                "total_updates": len(available_dates) * 3,  # 3 updates per day
                "quizzes_answered": len(available_dates),
                "correct_answers": 0,
                "streak": len(available_dates)
            }
            # Save default stats
            with open('learning_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
        
        recommendations = ["EC2", "S3", "Lambda"]  # Default recommendations
    
    return render_template('index.html', 
                          available_dates=available_dates,
                          selected_date=selected_date,
                          content=content,
                          stats=stats,
                          recommendations=recommendations)

@app.route('/answer/<date>/<int:answer_index>')
def submit_answer(date, answer_index):
    # Load the content for the given date
    try:
        with open(f'aws_learning_{date}.json', 'r') as f:
            content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return redirect(url_for('index'))
    
    # Check if the answer is correct
    correct = answer_index == content['quiz_question']['correct_index']
    
    # Update stats using the tracker if available
    if TRACKER_AVAILABLE:
        user_answer = content['quiz_question']['options'][answer_index]
        tracker.record_quiz_answer(content['quiz_question'], user_answer, correct)
    else:
        # Update stats manually
        try:
            with open('learning_stats.json', 'r') as f:
                stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats = {
                "total_updates": 0,
                "quizzes_answered": 0,
                "correct_answers": 0,
                "streak": 0
            }
        
        stats['quizzes_answered'] += 1
        if correct:
            stats['correct_answers'] += 1
        
        # Save updated stats
        with open('learning_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    # Flash a message about the answer
    if correct:
        flash('Correct! Great job!', 'success')
    else:
        correct_answer = content['quiz_question']['options'][content['quiz_question']['correct_index']]
        flash(f'Incorrect. The correct answer is: {correct_answer}', 'error')
    
    return redirect(url_for('index', date=date))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
