from litellm import completion # type: 
# import litellm
# litellm._turn_on_debug()
from dotenv import load_dotenv
from mcp_research.crew import SimpleCrew
# Load environment variables from .env file
load_dotenv()


def run():
        action_input = {"query": "I want got to Beijing on May 1st,2025, what is the travel advise?"}  # Direct string value
        try:
            response = SimpleCrew().crew().kickoff(inputs=action_input)
            print("Response:", response)
        except Exception as e:
            print(f"Error running crew: {e}")


if __name__ == "__main__":
    import sys
    run()
