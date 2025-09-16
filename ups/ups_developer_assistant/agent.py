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

"""UPS Developer Assistant - Root Agent"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from ups_developer_assistant import prompt
from ups_developer_assistant.sub_agents.legacy_api_documentation.agent import legacy_api_documentation_agent
from ups_developer_assistant.sub_agents.search.agent import search_agent
from ups_developer_assistant.sub_agents.code_generation.agent import code_generation_agent


root_agent = Agent(
    model="gemini-2.5-flash",
    name="ups_developer_assistant",
    description="A UPS Developer Assistant using specialized sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        legacy_api_documentation_agent,
        code_generation_agent,
    ],
    tools=[
        AgentTool(agent=search_agent),
    ],
)
