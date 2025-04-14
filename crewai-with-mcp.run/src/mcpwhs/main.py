#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from mcpwhs.crew import PIAIC

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_session_id():
    """Get session ID from environment or command line arguments."""
    return os.getenv("MCPX_SESSION_ID") or (len(sys.argv) > 1 and sys.argv[1])

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        PIAIC(session_id=session_id).crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        PIAIC(session_id=session_id).crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        PIAIC(session_id=session_id).crew().replay(task_id=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        PIAIC(session_id=session_id).crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")