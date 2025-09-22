# agents/research_agent.py

# from google import genai
import google.generativeai as genai
import os
from typing import List, Optional
from agno.agent import Agent
from agno.models.response import ModelResponse
# from agno.tools.googlesearch import GoogleSearch
from agno.tools.googlesearch import GoogleSearchTools
from agents.llm_gemini import llm
from prompts.research import RESEARCH_PROMPT



# Ensure the Gemini API key is loaded
from dotenv import load_dotenv
load_dotenv()

# Use a more powerful model for complex research tasks.
# RESEARCH_MODEL_NAME = 'gemini-2.5-flash' 
# RESEARCH_MODEL_NAME = 'gemini-1.5-pro-latest' 

class ResearchAgent(Agent):
    """
    A specialized agent for conducting in-depth research using a chain-of-thought and Google Search.
    It can analyze complex queries and synthesize information into a structured response.
    """
    
    def __init__(self, **kwargs):
        # Instantiate the model directly using the genai alias
        # self._research_model = genai.GenerativeModel(RESEARCH_MODEL_NAME)
        
        # Instantiate the search tool
        self.search_tool = GoogleSearchTools()
        
        super().__init__(
            name="Research Agent",
            description="Conducts in-depth research by performing searches and synthesizing information.",
            model=llm, # Pass the GenerativeModel instance here
            tools=[self.search_tool],
            instructions=[RESEARCH_PROMPT],
            **kwargs
        )
        
    def execute(self, user_request: str) -> ModelResponse:
        """
        Executes a research query by using a chain-of-thought approach with internet search.
        
        Args:
            user_request: The user's research question.
            
        Returns:
            A ModelResponse object containing the research findings.
        """
        print(f"Research Agent is working on: '{user_request}'")

        try:
            initial_prompt = (
                f"Query: {user_request}"
            )
            
            # The `self.run()` method automatically uses the model and tools
            # passed in the __init__ method.
            response = self.run(initial_prompt)

            return response
            
        except Exception as e:
            error_message = f"An error occurred during research: {e}"
            print(error_message)
            return ModelResponse(content=error_message)
