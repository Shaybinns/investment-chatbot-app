# AI Investment Brain

This component implements a sophisticated AI brain for the investment chatbot with the following features:

## Key Features
- Persistent memory using Redis
- Real-time market data integration (Yahoo Finance)
- Portfolio optimization
- Trading platform integration (Trading212)
- Research capabilities (Perplexity API)
- Continuous learning through feedback loops

## Architecture
- `brain.py`: Core AI brain implementation
- `memory.py`: Memory management and persistence
- `api.py`: FastAPI endpoints
- Docker configuration for containerized deployment

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
REDIS_URL=redis://localhost:6379
TRADING212_API_KEY=your_key
PERPLEXITY_API_KEY=your_key
```

3. Run the API:
```bash
uvicorn api:app --reload
```

## API Endpoints
- `/ws/chat/{user_id}`: WebSocket endpoint for chat
- `/analyze/portfolio/{user_id}`: Portfolio analysis and optimization
- `/analyze/market`: Market data analysis
- `/feedback/{interaction_id}`: User feedback handling
- `/memory/{user_id}`: Memory retrieval
- `/research`: Multi-source research queries

## Memory System
The brain maintains different types of memories:
- Conversation history
- Market data analysis
- Portfolio states
- User feedback
- Research findings

## Learning Mechanism
The system implements continuous learning through:
1. User feedback collection
2. Interaction analysis
3. Performance monitoring
4. Model updates based on accumulated data

## Dependencies
- FastAPI
- Redis
- yfinance
- scipy
- numpy
- Trading212 API
- Perplexity API