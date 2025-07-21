#!/usr/bin/env python3
"""
AWS Learning Assistant - Amazon Bedrock Enhancement
--------------------------------------------------
This module enhances the AWS Learning Assistant with Amazon Bedrock
to generate better summaries and more relevant quiz questions.
"""

import boto3
import json

def get_bedrock_client():
    """Initialize and return the Amazon Bedrock client."""
    return boto3.client('bedrock-runtime')

def generate_summary(content, max_length=200):
    """
    Generate a concise summary of AWS content using Amazon Bedrock.
    
    Args:
        content (str): The AWS update content to summarize
        max_length (int): Maximum length of the summary
        
    Returns:
        str: A concise summary of the content
    """
    client = get_bedrock_client()
    
    prompt = f"""
    Summarize the following AWS update in a concise, informative way.
    Focus on the key benefits, features, and use cases. Keep it under {max_length} characters.
    
    Content to summarize:
    {content}
    """
    
    # Using Claude model as an example
    response = client.invoke_model(
        modelId='anthropic.claude-v2',
        body=json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 500,
            "temperature": 0.5,
            "top_p": 0.9,
        })
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['completion'].strip()

def generate_quiz_question(content):
    """
    Generate a quiz question based on AWS content using Amazon Bedrock.
    
    Args:
        content (dict): The AWS update content with title, summary, and link
        
    Returns:
        dict: A quiz question with options and correct answer
    """
    client = get_bedrock_client()
    
    prompt = f"""
    Create a multiple-choice quiz question based on the following AWS update.
    The question should test understanding of the key concepts, benefits, or use cases.
    
    AWS Update Title: {content['title']}
    AWS Update Summary: {content['summary']}
    
    Format your response as a JSON object with the following structure:
    {{
        "question": "The question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "The correct option text",
        "correct_index": 0,  // The index of the correct answer (0-based)
        "explanation": "Brief explanation of why this is the correct answer"
    }}
    """
    
    # Using Claude model as an example
    response = client.invoke_model(
        modelId='anthropic.claude-v2',
        body=json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
        })
    )
    
    response_body = json.loads(response['body'].read())
    
    # Extract the JSON from the response
    response_text = response_body['completion'].strip()
    
    # Find the JSON object in the response
    try:
        # Try to parse the entire response as JSON
        quiz_data = json.loads(response_text)
    except json.JSONDecodeError:
        # If that fails, try to extract the JSON object from the text
        import re
        json_match = re.search(r'({.*})', response_text, re.DOTALL)
        if json_match:
            try:
                quiz_data = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                # Fallback to a default question if parsing fails
                quiz_data = {
                    "question": f"What is the main benefit of {content['title']}?",
                    "options": [
                        "Improved performance",
                        "Cost reduction",
                        "Enhanced security",
                        "Better user experience"
                    ],
                    "correct_answer": "Improved performance",
                    "correct_index": 0,
                    "explanation": "Please refer to the article for details."
                }
        else:
            # Fallback to a default question
            quiz_data = {
                "question": f"What is the main benefit of {content['title']}?",
                "options": [
                    "Improved performance",
                    "Cost reduction",
                    "Enhanced security",
                    "Better user experience"
                ],
                "correct_answer": "Improved performance",
                "correct_index": 0,
                "explanation": "Please refer to the article for details."
            }
    
    # Add the source link
    quiz_data["source"] = content["link"]
    
    return quiz_data

# Example usage:
# This module can be imported into the main aws_learning_assistant.py script
# and used to replace the basic summarize_updates and create_quiz_question functions
"""
# In aws_learning_assistant.py:

from bedrock_enhancement import generate_summary, generate_quiz_question

def summarize_updates(updates, count=3):
    summaries = []
    for update in updates[:count]:
        update_copy = update.copy()
        update_copy['summary'] = generate_summary(update['summary'])
        summaries.append(update_copy)
    return summaries

def create_quiz_question(update):
    return generate_quiz_question(update)
"""
