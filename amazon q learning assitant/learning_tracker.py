#!/usr/bin/env python3
"""
AWS Learning Assistant - Learning Tracker
----------------------------------------
This module tracks learning progress, including:
- Updates read
- Quiz questions answered
- Correct answers
- Learning streak
"""

import json
import os
import datetime
from collections import defaultdict

class LearningTracker:
    def __init__(self, stats_file='learning_stats.json'):
        self.stats_file = stats_file
        self.stats = self._load_stats()
        
    def _load_stats(self):
        """Load stats from file or create default stats."""
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create default stats
            return {
                "total_updates": 0,
                "quizzes_answered": 0,
                "correct_answers": 0,
                "streak": 0,
                "last_activity_date": None,
                "topics": {},
                "daily_activity": {},
                "quiz_history": []
            }
    
    def _save_stats(self):
        """Save stats to file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_update_read(self, update):
        """Record that an update was read."""
        self.stats["total_updates"] += 1
        
        # Extract topics from the update title and add to topics dictionary
        topics = self._extract_topics(update["title"])
        for topic in topics:
            if topic in self.stats["topics"]:
                self.stats["topics"][topic] += 1
            else:
                self.stats["topics"][topic] = 1
        
        # Update daily activity
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today in self.stats["daily_activity"]:
            self.stats["daily_activity"][today]["updates_read"] += 1
        else:
            self.stats["daily_activity"][today] = {
                "updates_read": 1,
                "quizzes_answered": 0,
                "correct_answers": 0
            }
        
        # Update streak
        self._update_streak()
        
        # Save stats
        self._save_stats()
    
    def record_quiz_answer(self, quiz_question, user_answer, is_correct):
        """Record a quiz answer."""
        self.stats["quizzes_answered"] += 1
        if is_correct:
            self.stats["correct_answers"] += 1
        
        # Update daily activity
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today in self.stats["daily_activity"]:
            self.stats["daily_activity"][today]["quizzes_answered"] += 1
            if is_correct:
                self.stats["daily_activity"][today]["correct_answers"] += 1
        else:
            self.stats["daily_activity"][today] = {
                "updates_read": 0,
                "quizzes_answered": 1,
                "correct_answers": 1 if is_correct else 0
            }
        
        # Add to quiz history
        self.stats["quiz_history"].append({
            "date": today,
            "question": quiz_question["question"],
            "user_answer": user_answer,
            "correct_answer": quiz_question["correct_answer"],
            "is_correct": is_correct
        })
        
        # Update streak
        self._update_streak()
        
        # Save stats
        self._save_stats()
    
    def _update_streak(self):
        """Update the learning streak."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        last_date = self.stats["last_activity_date"]
        
        if last_date is None:
            # First activity
            self.stats["streak"] = 1
        else:
            # Convert string dates to datetime objects
            today_dt = datetime.datetime.strptime(today, "%Y-%m-%d")
            last_dt = datetime.datetime.strptime(last_date, "%Y-%m-%d")
            
            # Calculate the difference in days
            diff = (today_dt - last_dt).days
            
            if diff == 0:
                # Same day, streak unchanged
                pass
            elif diff == 1:
                # Consecutive day, increment streak
                self.stats["streak"] += 1
            else:
                # Streak broken
                self.stats["streak"] = 1
        
        # Update last activity date
        self.stats["last_activity_date"] = today
    
    def _extract_topics(self, title):
        """Extract AWS service topics from the title."""
        # List of common AWS services to look for
        aws_services = [
            "EC2", "S3", "Lambda", "DynamoDB", "RDS", "Aurora", "ECS", "EKS",
            "Fargate", "SQS", "SNS", "CloudFormation", "CloudWatch", "IAM",
            "Cognito", "API Gateway", "Step Functions", "Kinesis", "Glue",
            "Athena", "Redshift", "EMR", "SageMaker", "Comprehend", "Rekognition",
            "Polly", "Lex", "Bedrock", "CodeBuild", "CodePipeline", "CodeDeploy",
            "CloudFront", "Route 53", "VPC", "ELB", "ALB", "NLB", "WAF", "Shield",
            "GuardDuty", "Security Hub", "CloudTrail", "Config", "Secrets Manager",
            "KMS", "ACM", "Lake Formation", "EventBridge", "AppSync", "Amplify"
        ]
        
        # Find all AWS services mentioned in the title
        topics = []
        for service in aws_services:
            if service.lower() in title.lower():
                topics.append(service)
        
        # If no specific services found, use general categories
        if not topics:
            if "serverless" in title.lower():
                topics.append("Serverless")
            elif "container" in title.lower():
                topics.append("Containers")
            elif "machine learning" in title.lower() or "ml" in title.lower():
                topics.append("Machine Learning")
            elif "database" in title.lower() or "db" in title.lower():
                topics.append("Databases")
            elif "security" in title.lower():
                topics.append("Security")
            else:
                topics.append("General")
        
        return topics
    
    def get_stats(self):
        """Get the current stats."""
        return self.stats
    
    def get_topic_recommendations(self):
        """Get topic recommendations based on learning history."""
        if not self.stats["topics"]:
            return ["EC2", "S3", "Lambda"]  # Default recommendations
        
        # Find the most studied topics
        sorted_topics = sorted(self.stats["topics"].items(), key=lambda x: x[1], reverse=True)
        most_studied = [topic for topic, count in sorted_topics[:3]]
        
        # Find related topics to recommend
        related_topics = {
            "EC2": ["EBS", "Auto Scaling", "VPC"],
            "S3": ["CloudFront", "Glacier", "Storage Gateway"],
            "Lambda": ["API Gateway", "Step Functions", "EventBridge"],
            "DynamoDB": ["DAX", "DocumentDB", "AppSync"],
            "RDS": ["Aurora", "Neptune", "Redshift"],
            "ECS": ["EKS", "Fargate", "ECR"],
            "SageMaker": ["Comprehend", "Rekognition", "Forecast"],
            "CloudFormation": ["CDK", "SAM", "Service Catalog"],
            # Add more related topics as needed
        }
        
        recommendations = []
        for topic in most_studied:
            if topic in related_topics:
                recommendations.extend(related_topics[topic])
        
        # Return unique recommendations
        return list(set(recommendations))[:3]

# Example usage
if __name__ == "__main__":
    tracker = LearningTracker()
    
    # Example: Record an update read
    tracker.record_update_read({
        "title": "AWS Lambda now supports Python 3.9",
        "link": "https://aws.amazon.com/about-aws/whats-new/2021/07/aws-lambda-supports-python-3-9/"
    })
    
    # Example: Record a quiz answer
    quiz_question = {
        "question": "What is the maximum memory allocation for AWS Lambda?",
        "options": ["1 GB", "3 GB", "10 GB", "64 GB"],
        "correct_answer": "10 GB"
    }
    tracker.record_quiz_answer(quiz_question, "10 GB", True)
    
    # Print stats
    print(json.dumps(tracker.get_stats(), indent=2))
    
    # Get topic recommendations
    print("Recommended topics:", tracker.get_topic_recommendations())
