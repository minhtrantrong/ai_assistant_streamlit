import json
from typing import List
from agno.agent import Agent
from agno.models.response import ModelResponse
from agents.llm_gemini import llm
from prompts.report import REPORT_PROMPT, VIETNAMESE_REPORTING_TEMPLATE

class ReportAgent(Agent):
    """
    A specialized agent for creating ESG reports in Vietnamese.
    This agent analyzes provided documents and templates to generate a structured report.
    """
    
    name = "Report Agent"
    description = "Generates comprehensive ESG reports in Vietnamese based on provided documents and report templates."
    
    def __init__(self, **kwargs):
        super().__init__(
            model=llm,
            instructions=[REPORT_PROMPT],
            **kwargs
        )
        
    def execute(self, doc_contents: List[str], template_contents: List[str], user_request: str) -> ModelResponse:
        """
        Processes document and template content to create an ESG report.
        
        Args:
            doc_contents: A list of strings, where each string is the content of an uploaded document.
            template_contents: A list of strings, where each string is the content of an uploaded template.
            user_request: The user's specific request for the report.
            
        Returns:
            A ModelResponse object containing the generated report content.
        """
        # Combine all document and template content into a single context string
        all_docs_content = "\n\n".join(doc_contents)
        all_templates_content = "\n\n".join(template_contents)
        
        # Format the prompt for the model
        full_prompt = (
            f"Tài liệu tham khảo (tài liệu nội bộ, báo cáo, v.v.):\n{all_docs_content}\n\n"
            f"Mẫu báo cáo:\n{all_templates_content}\n\n"
            f"Yêu cầu của người dùng: {user_request}\n\n"
            f"{VIETNAMESE_REPORTING_TEMPLATE}\n\n"
        )
        
        print("Sending request to Report Agent model...")
        
        try:
            # Generate the response using the agent's run method
            # The run method sends the full prompt to the LLM
            report_content = self.run(full_prompt)
            
            # Return a ModelResponse with the final report content
            return ModelResponse(content=report_content.content)
            
        except Exception as e:
            error_message = f"An error occurred while generating the report: {e}"
            print(error_message)
            return ModelResponse(content=error_message)