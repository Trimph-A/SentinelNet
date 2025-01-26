import pandas as pd
from datasets import Dataset
from typing import List, Dict
import logging

def preprocess_data(raw_data: List[Dict[str, str]], tokenizer, use_case: str, max_length: int = 512) -> Dataset:
    """
    Preprocesses raw network traffic data by tokenizing and formatting it for training.
    
    Args:
        raw_data (List[Dict[str, str]]): The raw dataset containing network traffic logs.
        tokenizer: The tokenizer to use for processing text.
        use_case (str): Specific use case (attack detection or malfunction).
        max_length (int): Maximum sequence length. Defaults to 512.
    
    Returns:
        Dataset: A Hugging Face Dataset object ready for training.
    
    Raises:
        ValueError: If the input data does not conform to expected structure.
    """
    logger = logging.getLogger(__name__)
    
    df = pd.DataFrame(raw_data)
    logger.info(f"DataFrame created with {len(df)} samples.")
    
    def tokenize_function(examples):
        return tokenizer(examples['input'], truncation=True, padding='max_length', max_length=max_length)
    
    tokenized_inputs = df['input'].tolist()
    tokenized_outputs = df['output'].tolist()
    
    tokenized_data = tokenizer(tokenized_inputs, truncation=True, padding='max_length', max_length=max_length)
    labels = tokenizer(tokenized_outputs, truncation=True, padding='max_length', max_length=max_length)['input_ids']
    
    labels = [
        [(label if label != tokenizer.pad_token_id else -100) for label in label_seq]
        for label_seq in labels
    ]
    
    tokenized_data['labels'] = labels
    
    dataset = Dataset.from_dict(tokenized_data)
    logger.info("Data has been tokenized and formatted for training.")
    
    return dataset
