# AI Brain Component

## Overview
Centralized AI brain using ChatGPT with persistent memory and multiple data sources.

## Components
- `brain.py`: Main AI controller
- `memory_manager.py`: Manages short/long-term memory
- `knowledge_base.py`: Base financial knowledge
- `data_providers/`: External data integrations

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY='your-key'
```

## Usage
```python
from brain import Brain

brain = Brain(openai_api_key='your-key')
response = brain.process_message('What stocks should I invest in?')
```