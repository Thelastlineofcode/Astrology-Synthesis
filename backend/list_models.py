#!/usr/bin/env python3
"""List available Gemini models for your API key."""

import os
import sys
from google import genai
from google.genai import types

def list_available_models():
    """List all available models."""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found")
        return

    print(f"Using API key: {api_key[:10]}...")
    print("\n" + "="*80)
    print("Fetching available models...")
    print("="*80 + "\n")

    try:
        # Initialize client
        client = genai.Client(api_key=api_key)

        # List models
        models = client.models.list()

        print(f"Found {len(list(models))} models:\n")

        for model in client.models.list():
            print(f"Model: {model.name}")
            if hasattr(model, 'display_name'):
                print(f"  Display Name: {model.display_name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"  Methods: {model.supported_generation_methods}")
            print()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_available_models()
