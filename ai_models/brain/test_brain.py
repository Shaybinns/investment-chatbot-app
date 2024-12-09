import asyncio
import os
from dotenv import load_dotenv
from . import InvestmentBrain

async def test_brain():
    # Load environment variables
    load_dotenv()
    
    # Initialize the brain with OpenAI API key
    brain = InvestmentBrain(os.getenv('OPENAI_API_KEY'))
    
    # Test a message
    response = await brain.process_message(
        "What do you think about investing in tech stocks given the current market conditions?"
    )
    
    # Print the response and sentiment
    print(f"Response: {response.get('response', 'No response')}")
    print(f"Sentiment: {response.get('sentiment', 'No sentiment')}")

if __name__ == "__main__":
    asyncio.run(test_brain())