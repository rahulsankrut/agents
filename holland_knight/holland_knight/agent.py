"""Holland Knight Legal Multi-Agent System - Main Agent Entry Point"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any
import requests
import os

# Import prompts
from holland_knight.prompt import ROOT_AGENT_INSTR
from holland_knight.sub_agents.legal_qa.prompt import LEGAL_QA_INSTR
from holland_knight.sub_agents.document_generation.prompt import DOCUMENT_GENERATION_INSTR


def court_listener_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Search Court Listener database for legal cases, opinions, and documents.
    
    Args:
        query: Search query for legal cases or documents
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        Dictionary containing search results with case information
    """
    api_key = os.getenv("COURT_LISTENER_API_KEY")
    if not api_key:
        return {"error": "Court Listener API key not configured"}
    
    base_url = "https://www.courtlistener.com/api/rest/v3/search/"
    
    params = {
        "q": query,
        "stat_Precedential": "on",
        "order_by": "score desc",
        "stat_Non-Precedential": "on",
        "format": "json",
        "stat_Unknown": "on",
    }
    
    headers = {
        "Authorization": f"Token {api_key}",
        "User-Agent": "Holland-Knight-Legal-Agent/1.0"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])[:max_results]
        
        # Format results for better readability
        formatted_results = []
        for result in results:
            formatted_result = {
                "case_name": result.get("caseName", "N/A"),
                "court": result.get("court", "N/A"),
                "date_filed": result.get("dateFiled", "N/A"),
                "absolute_url": result.get("absolute_url", "N/A"),
                "snippet": result.get("snippet", "N/A"),
                "precedential": result.get("stat_Precedential", False),
            }
            formatted_results.append(formatted_result)
        
        return {
            "query": query,
            "total_results": data.get("count", 0),
            "results": formatted_results
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to search Court Listener: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


# Create tools
court_listener_search_tool = FunctionTool(court_listener_search)

# Create sub-agents
legal_qa_agent = Agent(
    model="gemini-2.5-pro",
    name="legal_qa_agent",
    description="Specialized agent for answering legal questions and researching case law",
    instruction=LEGAL_QA_INSTR,
    tools=[court_listener_search_tool],
)

document_generation_agent = Agent(
    model="gemini-2.5-pro",
    name="document_generation_agent",
    description="Specialized agent for generating legal documents and contracts",
    instruction=DOCUMENT_GENERATION_INSTR,
)

# Main agent for deployment
root_agent = Agent(
    model="gemini-2.5-pro",
    name="root_agent",
    description="Holland Knight Legal Multi-Agent System - coordinates legal Q&A and document generation",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=[
        legal_qa_agent,
        document_generation_agent,
    ],
)
