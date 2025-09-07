from transformers import AutoTokenizer

# Choose any tokenizer depending on your model
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text, truncation=True))
