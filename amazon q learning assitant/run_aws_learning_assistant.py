#!/usr/bin/env python3
"""
AWS Learning Assistant - Runner Script
------------------------------------
This script runs all components of the AWS Learning Assistant:
1. Fetches and processes AWS updates
2. Sends email with summaries and quiz
3. Starts the web interface
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser

def run_aws_learning_assistant():
    """Run the AWS Learning Assistant script."""
    print("Running AWS Learning Assistant...")
    subprocess.run([sys.executable, "aws_learning_assistant.py"])
    print("AWS Learning Assistant completed.")

def run_web_interface():
    """Run the web interface."""
    print("Starting web interface...")
    # Start the web interface in a separate process
    web_process = subprocess.Popen([sys.executable, "web_interface.py"])
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Open the web interface in the default browser
    webbrowser.open("http://localhost:5000")
    
    return web_process

def main():
    """Main function to run all components."""
    # Check if required files exist
    required_files = [
        "aws_learning_assistant.py",
        "web_interface.py",
        "learning_tracker.py",
        ".env"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: The following required files are missing: {', '.join(missing_files)}")
        print("Please make sure all required files are in the current directory.")
        return
    
    # Run the AWS Learning Assistant in a separate thread
    assistant_thread = threading.Thread(target=run_aws_learning_assistant)
    assistant_thread.start()
    
    # Run the web interface
    web_process = run_web_interface()
    
    try:
        # Wait for the AWS Learning Assistant to complete
        assistant_thread.join()
        
        print("\nAWS Learning Assistant has completed.")
        print("The web interface is still running. Press Ctrl+C to stop it.")
        
        # Keep the script running until the user interrupts
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the web interface...")
        web_process.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
