import os
import yaml
import logging
from transformers import AutoModelForCausalLM, Trainer, TrainingArguments, AutoTokenizer
from google.cloud import storage
from typing import List, Dict
from datasets import Dataset

def finetune_model(raw_data: List[Dict[str, str]], output_dir: str, use_case: str) -> None:
    """
    Fine-tunes the LLaMa 3:2:1B model using the provided network traffic data.
    
    Args:
        raw_data (List[Dict[str, str]]): The dataset containing network traffic logs.
        output_dir (str): Directory to save the fine-tuned model.
        use_case (str): Use case for anomaly detection (e.g., attack detection or malfunction).
    
    Raises:
        Exception: If any step in the fine-tuning process fails.
    """
    # Load configuration
    config = yaml.safe_load(open('config/config.yaml'))
    
    # Setup logging
    logger = logging.getLogger(__name__)
    
    try:
        # Load tokenizer and LLaMa 3:2:1B model
        logger.info(f"Loading tokenizer and model: {config['model']['base_model']}")
        tokenizer = AutoTokenizer.from_pretrained(config['model']['base_model'])
        model = AutoModelForCausalLM.from_pretrained(config['model']['base_model'])
        
        # Preprocess data specific to network traffic logs
        logger.info("Preprocessing network traffic logs...")
        dataset = preprocess_data(raw_data, tokenizer, use_case)
        
        # Define training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=config['training']['epochs'],
            per_device_train_batch_size=config['training']['batch_size'],
            learning_rate=config['training']['learning_rate'],
            save_steps=config['training']['save_steps'],
            save_total_limit=config['training']['save_total_limit'],
            logging_dir=config['logging']['file'],
            logging_steps=config['training']['logging_steps'],
            evaluation_strategy=config['training'].get('evaluation_strategy', 'steps'),
            load_best_model_at_end=config['training'].get('load_best_model_at_end', False),
            metric_for_best_model=config['training'].get('metric_for_best_model', None),
            greater_is_better=config['training'].get('greater_is_better', False),
            seed=config['training'].get('seed', 42),
        )
        
        # Prepare trainer
        logger.info("Preparing trainer...")
        trainer = prepare_trainer(model, tokenizer, training_args, dataset, config['training'].get('data_collator', None))
        
        # Start training
        logger.info("Starting training...")
        training_output = trainer.train()
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        logger.info(f"Model saved to {output_dir}")
        
        # Save training metrics
        if 'metrics' in training_output:
            save_training_metrics(training_output.metrics, output_dir)
            logger.info("Training metrics saved.")
        
        # Upload model to Google Cloud Storage
        upload_to_gcs(output_dir, 'your-model-bucket', 'finetuned_model/')
        
    except Exception as e:
        logger.error(f"Error during fine-tuning: {str(e)}")
        raise e


def upload_to_gcs(local_dir: str, bucket_name: str, gcs_dir: str):
    """
    Upload the fine-tuned model directory to Google Cloud Storage.
    
    Args:
        local_dir (str): Local directory containing the fine-tuned model.
        bucket_name (str): Name of the GCS bucket.
        gcs_dir (str): Directory within the bucket where the model will be uploaded.
    """
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            gcs_path = os.path.join(gcs_dir, os.path.relpath(local_path, local_dir))
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            print(f"Uploaded {file} to gs://{bucket_name}/{gcs_path}")
