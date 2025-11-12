#!/usr/bin/env python3
"""
Simple test script for the Gemini LangChain agent.

This script demonstrates how to:
1. Initialize the Gemini agent
2. Send queries to the agent
3. View agent responses and metrics

Setup:
    1. Install dependencies: pip install -r requirements.txt
    2. Set GOOGLE_API_KEY in .env or export it:
       export GOOGLE_API_KEY="your-api-key-here"
    3. Run: python backend/test_gemini_agent.py
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from backend.agents.factory import create_gemini_agent


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 80 + "\n")


def test_gemini_agent():
    """Test the Gemini agent with sample queries."""

    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment variables")
        print("\nPlease set your Google API key:")
        print("  1. Get a free API key from: https://makersuite.google.com/app/apikey")
        print("  2. Add it to your .env file: GOOGLE_API_KEY=your-key-here")
        print("  3. Or export it: export GOOGLE_API_KEY='your-key-here'")
        return

    print("🚀 Initializing Gemini Agent...")
    print_separator()

    try:
        # Create agent
        agent = create_gemini_agent(
            api_key=api_key,
            model="gemini-1.5-flash",  # Fast and free
            verbose=True  # Show detailed output
        )

        print(f"✅ Agent initialized: {agent.agent_name}")
        print(f"   Model: {agent.model}")
        print(f"   Temperature: {agent.temperature}")
        print(f"   Max iterations: {agent.max_iterations}")
        print_separator()

        # Test queries
        test_queries = [
            {
                "query": "What does it mean to have Sun in Aries?",
                "chart_data": {"sun_sign": "Aries"}
            },
            {
                "query": "Tell me about Moon in Taurus compatibility with Sun in Aries",
                "chart_data": {
                    "sun_sign": "Aries",
                    "moon_sign": "Taurus"
                }
            },
            {
                "query": "What are the characteristics of the Ashwini nakshatra?",
                "chart_data": {"nakshatra": "Ashwini"}
            }
        ]

        for i, test_query in enumerate(test_queries, 1):
            print(f"📝 Test Query {i}:")
            print(f"   Query: {test_query['query']}")
            if test_query.get('chart_data'):
                print(f"   Chart Data: {test_query['chart_data']}")
            print()

            print("🤔 Invoking agent...")
            result = agent.invoke(test_query)

            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ Response received!")
                print(f"\n📖 Interpretation:\n{result['interpretation']}\n")
                print(f"📊 Metrics:")
                print(f"   - Model: {result['model']}")
                print(f"   - Strategy: {result['strategy']}")
                print(f"   - Tokens: {result['tokens']}")
                print(f"   - Cost: ${result['cost']:.6f}")
                print(f"   - Quality Score: {result['quality']}")

            print_separator()

            # Show cumulative metrics
            metrics = agent.get_metrics()
            print("📈 Cumulative Agent Metrics:")
            print(f"   - Total invocations: {metrics['invocations']}")
            print(f"   - Total tokens: {metrics['total_tokens']}")
            print(f"   - Total cost: ${metrics['total_cost']:.6f}")
            print(f"   - Avg tokens/call: {metrics['avg_tokens_per_call']:.0f}")
            print_separator()

        print("🎉 All tests completed successfully!")
        print("\nℹ️  Note: Gemini has a generous free tier, so you can test extensively.")
        print("   Visit https://ai.google.dev/pricing for rate limits.")

    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("\nPlease check your GOOGLE_API_KEY configuration.")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🌟 Gemini LangChain Agent Test Script 🌟")
    print_separator()
    test_gemini_agent()
