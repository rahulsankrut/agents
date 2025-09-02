"""Tests for the presentation chatbot."""

import pytest
import textwrap
from presentation_chatbot.agent import root_agent


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test that the agent initializes correctly."""
    assert root_agent is not None
    assert root_agent.name == "presentation_chatbot"
    assert root_agent.model == "gemini-2.5-pro"


def test_agent_configuration():
    """Test agent configuration."""
    assert root_agent.tools is not None
    assert len(root_agent.tools) >= 1
    
    # Check that our tools are present
    tool_names = [tool.__name__ for tool in root_agent.tools]
    assert "generate_presentation" in tool_names
    assert "get_presentation_templates" in tool_names


def test_agent_instructions():
    """Test that agent has instructions."""
    assert root_agent.global_instruction is not None
    assert len(root_agent.global_instruction) > 0
    assert "presentation" in root_agent.global_instruction.lower()
    
    assert root_agent.instruction is not None
    assert len(root_agent.instruction) > 0
    assert "presentation" in root_agent.instruction.lower()
