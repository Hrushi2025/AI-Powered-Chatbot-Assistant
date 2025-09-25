# llm_service.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the local Alpaca model
MODEL_NAME = "chavinlo/alpaca-native"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def generate_llm_response(prompt: str, user_id: str = "U001", language: str = "en") -> str:
    """
    Generate a natural language response using a local Alpaca LLM.
    """
    try:
        # Tokenize the input
        inputs = tokenizer(prompt, return_tensors="pt")

        # Generate response (CPU-friendly)
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error generating LLM response: {e}"
