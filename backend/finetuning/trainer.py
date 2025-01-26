from transformers import Trainer, DataCollatorForLanguageModeling, default_data_collator
from datasets import Dataset
import logging

def prepare_trainer(model, tokenizer, training_args, dataset: Dataset, data_collator=None) -> Trainer:
    """
    Prepares the Hugging Face Trainer with the given model, tokenizer, and dataset.
    
    Args:
        model: The pre-trained model to fine-tune (LLaMa 3:2:1B).
        tokenizer: The tokenizer corresponding to the model.
        training_args: Training arguments for the Trainer.
        dataset: The dataset for training.
        data_collator: Optional data collator. If None, uses default.
    
    Returns:
        Trainer: Configured Trainer instance.
    """
    logger = logging.getLogger(__name__)
    
    if data_collator is None:
        logger.info("Using default data collator.")
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,
        )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    return trainer
