#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mcpwhs.crew import MCPCrew
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# mcp-crew-ai --agents /home/ubuntu/MCP-Research-Work-PIAIC/mcp-crew-ai/examples/agents.yml --tasks /home/ubuntu/MCP-Research-Work-PIAIC/mcp-crew-ai/examples/tasks.yml --topic "travel advise" --variables '{"date": "2025-05-01", "focus": "weather, fashion"}' --verbose 
# export MCPX_SESSION_ID="your_session_id_here" # sign-up https://www.mcp.run/
def get_session_id():
    """Get session ID from environment or command line arguments."""
    return os.getenv("MCPX_SESSION_ID") or (len(sys.argv) > 1 and sys.argv[1])

def run():
    """
    Run the crew.
    """
    inputs = {"query": "I want got to Beijing on May 1st,2025, what is the travel advise?"}
    
    try:
        # MCPCrew().crew().kickoff(inputs=inputs)
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        response = MCPCrew(session_id=session_id).crew().kickoff(inputs=inputs)
        # response = SimpleCrew().crew().kickoff(inputs=inputs)
        print("Response:", response)
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
        # MCPCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        MCPCrew(session_id=session_id).crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)


    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        # MCPCrew().crew().replay(task_id=sys.argv[1])
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        MCPCrew(session_id=session_id).crew().replay(task_id=sys.argv[2])


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
        # MCPCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
        session_id = get_session_id()
        if not session_id:
            raise ValueError("Please provide MCPX_SESSION_ID as an environment variable or command line argument")
        
        MCPCrew(session_id=session_id).crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)


    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()