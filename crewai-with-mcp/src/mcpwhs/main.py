#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mcpwhs.crew import MCPCrew
import os
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crew.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# sign-up https://www.mcp.run/


def run():
    """
    Run the crew.
    """
    inputs = {"query": "Hello, I want got to Beijing on May 1st,2025, what is the travel advise?"}
    
    try:
        crew = MCPCrew()
        print("MCPCrew initialized")

        result = crew.crew().kickoff(inputs=inputs)
        # session_id = get_session_id()
        # if not session_id:
        #     raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        # response = MCPCrew(session_id=session_id).crew().kickoff(inputs=inputs)
        # response = SimpleCrew().crew().kickoff(inputs=inputs)
        # print("Response:", response)
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
        MCPCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        # session_id = get_session_id()
        # if not session_id:
        #     raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        # MCPCrew(session_id=session_id).crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)


    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MCPCrew().crew().replay(task_id=sys.argv[1])
        # session_id = get_session_id()
        # if not session_id:
        #     raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        # MCPCrew(session_id=session_id).crew().replay(task_id=sys.argv[2])


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
        MCPCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
        # session_id = get_session_id()
        # if not session_id:
        #     raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        # MCPCrew(session_id=session_id).crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)


    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()