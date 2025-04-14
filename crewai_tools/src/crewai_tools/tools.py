from crewai.tools import BaseTool
from litellm import completion
import os

class SimpleMCPTool(BaseTool):
    name: str = "simple_tool"
    description: str = "A simple demo tool for CrewAI integration with Gemini."
    
    def _run(self, query: str) -> str:
        """Process the query using Gemini API"""
        result = completion(
            model='gemini/gemini-1.5-flash',
            api_key=os.getenv('GEMINI_API_KEY'),
            messages=[{"content": query, "role": "user"}]
        )
        response = result['choices'][0]['message']['content']  
        return response

def get_simple_tools():
    return [SimpleMCPTool()]
