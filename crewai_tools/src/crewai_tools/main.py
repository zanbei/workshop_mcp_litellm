from litellm import completion # type: ignore

from dotenv import load_dotenv
from mcp_research.crew import SimpleCrew
# Load environment variables from .env file
load_dotenv()

def run():
        action_input = {"query": "Write a short creative story about a fun day."}  # Direct string value
        try:
            SimpleCrew().crew().kickoff(inputs=action_input)
        except Exception as e:
            print(f"Error running crew: {e}")


if __name__ == "__main__":
    import sys
    run()
