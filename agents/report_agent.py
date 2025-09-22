# agents/report_agent.py

import json
from typing import List
from agno.agent import Agent
from agno.models.response import ModelResponse
from agents.llm_gemini import llm
from prompts.report import REPORT_PROMPT, VIETNAMESE_REPORTING_TEMPLATE
from agents.research_agent import ResearchAgent  # NEW: Import the ResearchAgent

class ReportAgent(Agent):
    """
    A specialized agent for creating ESG reports in Vietnamese.
    This agent can request additional information from a ResearchAgent.
    """
    
    name = "Report Agent"
    description = "Generates comprehensive ESG reports in Vietnamese based on provided documents, templates, and external research."
    
    def __init__(self, **kwargs):
        # Instantiate the ResearchAgent as a tool
        self.research_agent = ResearchAgent()
        
        super().__init__(
            model=llm,
            instructions=[REPORT_PROMPT],
            # Pass the ResearchAgent as a tool
            # The agent will see this as a function it can call
            tools=[self.research_agent],
            **kwargs
        )
        
    def execute(self, doc_contents: List[str], template_contents: List[str], user_request: str) -> ModelResponse:
        """
        Processes document and template content and performs research to create an ESG report.
        
        Args:
            doc_contents: A list of strings, where each string is the content of an uploaded document.
            template_contents: A list of strings, where each string is the content of an uploaded template.
            user_request: The user's specific request for the report.
            
        Returns:
            A ModelResponse object containing the generated report content.
        """
        # Combine all document and template content into a single context string
        print("Report Agent model is working ...")
        all_docs_content = "\n\n".join(doc_contents)
        all_templates_content = "\n\n".join(template_contents)
        print("Invoke research agent ...")
        research = self.research_agent.run(user_request)
        research_content = research.content
        print(f"Research content: {research_content}")
        
        # Format the prompt for the model. Crucially, the prompt tells the model
        # to consider using its tools (the ResearchAgent) to gather information.
        full_prompt = (
            f"Tài liệu tham khảo (tài liệu nội bộ, báo cáo, v.v.):\n{all_docs_content}\n\n"
            f"Mẫu báo cáo:\n{all_templates_content}\n\n"
            f"Yêu cầu của người dùng: {user_request}\n\n"
            f"Sử dụng công cụ `research_agent` để tìm kiếm thông tin bổ sung {research_content}.\n\n"
            f"{VIETNAMESE_REPORTING_TEMPLATE}\n\n"
        )
        
        
        
        try:
            # The `self.run()` method orchestrates the chain-of-thought and tool calls.
            # It will automatically decide if it needs to call `research_agent.execute()`.
            report_content = self.run(full_prompt)
            
            # The final content is what the model generates after its reasoning loop.
            return ModelResponse(content=report_content.content)
            
        except Exception as e:
            error_message = f"An error occurred while generating the report: {e}"
            print(error_message)
            return ModelResponse(content=error_message)