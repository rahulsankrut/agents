# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for UPS Developer Assistant."""

import pytest
from ups_developer_assistant import root_agent
from ups_developer_assistant.sub_agents.legacy_api_documentation.agent import legacy_api_documentation_agent
from ups_developer_assistant.sub_agents.search.agent import search_agent
from ups_developer_assistant.sub_agents.code_generation.agent import code_generation_agent


def test_root_agent_creation():
    """Test that the root agent is created successfully."""
    assert root_agent is not None
    assert root_agent.name == "ups_developer_assistant"
    assert root_agent.model == "gemini-2.5-flash"


def test_legacy_api_documentation_agent_creation():
    """Test that the Legacy API Documentation agent is created successfully."""
    assert legacy_api_documentation_agent is not None
    assert legacy_api_documentation_agent.name == "legacy_api_documentation_agent"
    assert legacy_api_documentation_agent.model == "gemini-2.5-flash"


def test_search_agent_creation():
    """Test that the Search agent is created successfully."""
    assert search_agent is not None
    assert search_agent.name == "search_agent"
    assert search_agent.model == "gemini-2.5-flash"


def test_code_generation_agent_creation():
    """Test that the Code Generation agent is created successfully."""
    assert code_generation_agent is not None
    assert code_generation_agent.name == "code_generation_agent"
    assert code_generation_agent.model == "gemini-2.5-pro"


def test_hybrid_agent_configuration():
    """Test that the agent has both sub-agents and tools configured correctly."""
    # Check sub-agents
    assert len(root_agent.sub_agents) == 2
    assert legacy_api_documentation_agent in root_agent.sub_agents
    assert code_generation_agent in root_agent.sub_agents
    
    # Check tools
    assert len(root_agent.tools) == 1
    from google.adk.tools.agent_tool import AgentTool
    assert isinstance(root_agent.tools[0], AgentTool)
    assert root_agent.tools[0].agent == search_agent
