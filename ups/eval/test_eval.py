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

"""Evaluation script for UPS Developer Assistant."""

import json
from google.adk.evaluation import evaluate_agent

from ups_developer_assistant import root_agent


def test_eval():
    """Run evaluation tests for the UPS Developer Assistant."""
    
    # Load test data
    with open("eval/data/test_data.json", "r") as f:
        test_data = json.load(f)
    
    # Run evaluation
    results = evaluate_agent(
        agent=root_agent,
        test_data=test_data,
    )
    
    print("Evaluation Results:")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == "__main__":
    test_eval()
