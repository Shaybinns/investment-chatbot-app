from typing import List, Dict

class DataPreprocessor:
    def __init__(self):
        self.knowledge_levels = {
            'beginner': (1, 3),
            'intermediate': (4, 7),
            'expert': (8, 10)
        }

    def preprocess_chat_data(self, messages: List[Dict]):
        """Preprocess chat data for training"""
        processed_data = []
        for msg in messages:
            # Add preprocessing logic
            processed_data.append({
                'input': msg['user_message'],
                'output': msg['ai_response'],
                'knowledge_level': msg['user_knowledge_level']
            })
        return processed_data

    def prepare_training_batch(self, data: List[Dict]):
        """Prepare data batch for model training"""
        return {
            'inputs': [d['input'] for d in data],
            'outputs': [d['output'] for d in data],
            'metadata': [{'knowledge_level': d['knowledge_level']} for d in data]
        }