"""Test the main FedEx Market Intelligence Agent."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fedex_market_intelligence.agent import root_agent


def test_agent_initialization():
    """Test that the agent initializes correctly."""
    print("Testing Agent Initialization...")
    
    try:
        assert root_agent is not None, "Agent not initialized"
        assert root_agent.name == "fedex_market_intelligence_agent", "Wrong agent name"
        assert len(root_agent.tools) == 7, f"Expected 7 tools, got {len(root_agent.tools)}"
        
        print("✓ Agent initialized successfully")
        print(f"  - Name: {root_agent.name}")
        print(f"  - Tools: {len(root_agent.tools)}")
        print(f"  - Model: {root_agent.model}")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent initialization failed: {str(e)}")
        return False


def test_agent_tools_loaded():
    """Test that all tools are loaded correctly."""
    print("\nTesting Agent Tools...")
    
    try:
        assert hasattr(root_agent, 'tools'), "Agent has no tools attribute"
        tool_count = len(root_agent.tools)
        assert tool_count == 7, f"Expected 7 tools, got {tool_count}"
        
        print("✓ All 7 tools loaded successfully")
        for i, tool in enumerate(root_agent.tools, 1):
            if hasattr(tool, 'name'):
                print(f"  {i}. {tool.name}")
            elif hasattr(tool, 'function'):
                print(f"  {i}. {tool.function.__name__}")
        
        return True
        
    except Exception as e:
        print(f"✗ Tool loading failed: {str(e)}")
        return False


def test_agent_configuration():
    """Test agent configuration is correct."""
    print("\nTesting Agent Configuration...")
    
    try:
        # Check model
        assert root_agent.model == "gemini-2.5-pro", f"Wrong model: {root_agent.model}"
        
        # Check name
        assert root_agent.name == "fedex_market_intelligence_agent", f"Wrong name: {root_agent.name}"
        
        # Check instruction exists
        assert root_agent.instruction is not None, "No instruction set"
        assert len(root_agent.instruction) > 0, "Empty instruction"
        
        print("✓ Agent configuration valid")
        print(f"  - Model: {root_agent.model}")
        print(f"  - Instruction length: {len(root_agent.instruction)} characters")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent configuration test failed: {str(e)}")
        return False


def run_agent_tests():
    """Run all agent tests."""
    print("=" * 60)
    print("FedEx Market Intelligence Agent - Agent Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(test_agent_initialization())
    results.append(test_agent_tools_loaded())
    results.append(test_agent_configuration())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    exit_code = run_agent_tests()
    sys.exit(exit_code)

