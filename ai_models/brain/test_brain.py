import asyncio
import os
from dotenv import load_dotenv
from . import InvestmentBrain

async def test_brain():
    # Load environment variables
    load_dotenv()
    
    # Get API key and verify it's loaded
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print('⚠️ ERROR: OPENAI_API_KEY not found in .env file')
        return
    
    print('🤖 Initializing Investment Brain...')
    brain = InvestmentBrain(api_key)
    
    # Test messages
    test_messages = [
        "What's your analysis of NVIDIA stock's current valuation?",
        "How should I think about diversification in my portfolio?",
    ]
    
    for message in test_messages:
        print('\n' + '='*50)
        print(f'🔍 Testing message: "{message}"')
        print('='*50)
        
        try:
            print('\n⏳ Processing...')
            response = await brain.process_message(message)
            
            print('\n📝 Results:')
            print(f'\nResponse: {response.get("response", "No response")}')
            print(f'\nSentiment Analysis:')
            sentiment = response.get('sentiment', {})
            if sentiment:
                print(f'- Bullish: {sentiment.get("bullish", 0)*100:.1f}%')
                print(f'- Bearish: {sentiment.get("bearish", 0)*100:.1f}%')
                print(f'- Confidence: {sentiment.get("confidence", 0)*100:.1f}%')
            
            # Check if we got entities
            entities = response.get('entities', {})
            if entities:
                print('\nExtracted Entities:')
                for category, items in entities.items():
                    if items:  # Only print categories that have items
                        print(f'- {category.capitalize()}: {", ".join(items)}')
            
        except Exception as e:
            print(f'\n❌ Error: {str(e)}')

if __name__ == "__main__":
    print('\n🚀 Starting Investment Brain Test\n')
    asyncio.run(test_brain())
    print('\n✅ Test Complete\n')