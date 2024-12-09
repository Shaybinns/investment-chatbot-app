import os
from brain import Brain

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

# Initialize brain
brain = Brain(openai_api_key=api_key)

# Test basic financial advice
print("\nTest 1: Basic financial advice")
response = brain.process_message("What's a good investment strategy for beginners?")
print(f"Response: {response}\n")

# Test stock data integration
print("\nTest 2: Stock data")
response = brain.process_message("What's the current price and performance of AAPL stock?")
print(f"Response: {response}\n")

# Test memory retention
print("\nTest 3: Memory retention")
response = brain.process_message("Based on our previous discussion, what investment strategy did you recommend?")
print(f"Response: {response}\n")

# Test portfolio optimization
print("\nTest 4: Portfolio optimization")
response = brain.process_message("How should I optimize a portfolio with AAPL, MSFT, and GOOGL?")
print(f"Response: {response}\n")