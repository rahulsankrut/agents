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

"""Search sub-agent for UPS Developer Assistant."""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .prompts import return_instructions_root

search_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    instruction=return_instructions_root(),
    tools=[
        google_search,
    ]
)
