import torch
from transformers import RobertaTokenizer, T5ForConditionalGeneration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeExplainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CodeExplainer, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        logger.info("Loading CodeT5 model...")
        # We use the 'multi-sum' version which is specifically better at EXPLAINING code
        # than the base version.
        try:
            self.tokenizer = RobertaTokenizer.from_pretrained("Salesforce/codet5-base-multi-sum")
            self.model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base-multi-sum")
            self.model.eval()
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError("Could not load the AI model.")

    def explain(self, code_snippet: str, max_length: int = 128) -> str:
        try:
            input_ids = self.tokenizer(code_snippet, return_tensors="pt", truncation=True).input_ids
            
            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids, 
                    max_length=max_length, 
                    num_beams=5,           # Helps find the best sentence structure
                    no_repeat_ngram_size=2, # FORCE STOPS repetition loops
                    early_stopping=True     # Stops when the sentence is complete
                )
            
            return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Error generating explanation."