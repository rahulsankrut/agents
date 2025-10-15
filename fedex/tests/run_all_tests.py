"""Run all tests for the FedEx Market Intelligence Agent."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_config import run_config_tests
from test_tools import run_all_tests as run_tool_tests
from test_agent import run_agent_tests


def main():
    """Run all test suites."""
    print("\n" + "=" * 70)
    print(" " * 15 + "FEDEX MARKET INTELLIGENCE AGENT")
    print(" " * 20 + "COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()
    
    results = []
    
    # Run configuration tests
    print("\n📋 PHASE 1: Configuration Tests")
    print("-" * 70)
    results.append(("Configuration", run_config_tests()))
    
    # Run tool tests
    print("\n\n🔧 PHASE 2: Tool Tests")
    print("-" * 70)
    results.append(("Tools", run_tool_tests()))
    
    # Run agent tests
    print("\n\n🤖 PHASE 3: Agent Tests")
    print("-" * 70)
    results.append(("Agent", run_agent_tests()))
    
    # Final summary
    print("\n\n" + "=" * 70)
    print(" " * 25 + "FINAL SUMMARY")
    print("=" * 70)
    
    for test_suite, exit_code in results:
        status = "✓ PASSED" if exit_code == 0 else "✗ FAILED"
        print(f"{test_suite:20s}: {status}")
    
    print("=" * 70)
    
    # Overall result
    all_passed = all(exit_code == 0 for _, exit_code in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThe FedEx Market Intelligence Agent is ready to use.")
        print("Run 'python demo.py' to start the interactive demo.")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\nPlease review the errors above and fix any issues.")
        failed = [name for name, code in results if code != 0]
        print(f"Failed suites: {', '.join(failed)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    print()  # Extra line for readability
    sys.exit(exit_code)

