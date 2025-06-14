# -*- coding: utf-8 -*-
"""predictor

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17lAaDskGGC6UrQVfeAp7vm8pjCphZHN2
"""

# emotion_classifier/predictor.py
import torch
from .model_loader import get_model_assets
from .preprocess import preprocess_text_for_cli # Use the CLI-specific preprocessor

class EmotionPredictor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmotionPredictor, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_len=128): # max_len should match training
        if self._initialized:
            return

        print("Initializing EmotionPredictor (this should happen only once)...")
        try:
            self.model, self.tokenizer, self.label_encoder = get_model_assets()
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.max_len = max_len
            self._initialized = True
            print(f"EmotionPredictor initialized successfully. Using device: {self.device}")
        except Exception as e:
            print(f"FATAL: Failed to initialize EmotionPredictor: {e}")
            # You might want to raise the exception or handle it more gracefully
            # For now, it will prevent the CLI from working if initialization fails.
            self._initialized = False # Ensure it's marked as not initialized
            raise # Re-raise the exception to make it clear initialization failed


    def predict(self, text_input):
        if not self._initialized:
            return "Error: Predictor not initialized. Model assets might be missing or download failed."

        processed_text = preprocess_text_for_cli(text_input)

        inputs = self.tokenizer.encode_plus(
            processed_text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=True, # Include for models that might use it
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)

        model_args = {'input_ids': input_ids, 'attention_mask': attention_mask}

        # Add token_type_ids if the tokenizer provided them and the model might use them
        if 'token_type_ids' in inputs and inputs['token_type_ids'] is not None:
            # A more robust check for model compatibility with token_type_ids
            if hasattr(self.model, 'config') and getattr(self.model.config, 'type_vocab_size', 0) > 0:
                 model_args['token_type_ids'] = inputs['token_type_ids'].to(self.device)
            elif self.model.name_or_path.startswith('bert'): # Heuristic for BERT-like models
                 model_args['token_type_ids'] = inputs['token_type_ids'].to(self.device)


        with torch.no_grad():
            outputs = self.model(**model_args)
            logits = outputs.logits

        predicted_idx = torch.argmax(logits, dim=1).item()
        predicted_emotion = self.label_encoder.inverse_transform([predicted_idx])[0]

        return predicted_emotion