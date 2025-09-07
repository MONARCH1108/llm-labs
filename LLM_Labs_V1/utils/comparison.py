import time
import logging
import spacy
import textstat  # For syllable count

from utils.llms import query_groq_llm, query_gemini_llm, query_ollama_llm
from comparision_tools.tokenizer import count_tokens
from comparision_tools.prompt_classifier import classify_prompt

# Logger setup
logging.basicConfig(
    filename='llm_comparison.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def get_readability_metrics(text):
    doc = nlp(text)
    sentence_count = len(list(doc.sents))
    word_count = len([token for token in doc if token.is_alpha])
    syllable_count = textstat.syllable_count(text)

    try:
        flesch_score = (
            206.835
            - 1.015 * (word_count / sentence_count)
            - 84.6 * (syllable_count / word_count)
        ) if sentence_count > 0 and word_count > 0 else None
    except ZeroDivisionError:
        flesch_score = None

    return {
        "sentence_count": sentence_count,
        "syllable_count": syllable_count,
        "flesch_reading_ease": round(flesch_score, 2) if flesch_score is not None else "N/A"
    }

def run_comparative_evaluation(providers_models: dict, prompts: dict, user_input: str):
    results = {}

    for provider, models in providers_models.items():
        for model in models:
            for prompt_name, prompt in prompts.items():
                key = f"{provider}_{model}_{prompt_name}"
                start_time = time.time()

                try:
                    input_tokens = count_tokens(user_input + prompt)
                    prompt_type = classify_prompt(prompt)
                    prompt_length_words = len(prompt.split())

                    if provider == "groq":
                        response = query_groq_llm(user_input=user_input, model=model, prompt=prompt)
                    elif provider == "gemini":
                        response = query_gemini_llm(user_input=user_input, model=model, prompt=prompt)
                    elif provider == "ollama":
                        response = query_ollama_llm(user_input=user_input, model=model, prompt=prompt)
                    else:
                        response = "[Unsupported provider]"

                    duration = round(time.time() - start_time, 3)
                    output_tokens = count_tokens(response)
                    readability = get_readability_metrics(response)

                    results[key] = {
                        "provider": provider,
                        "model": model,
                        "prompt_name": prompt_name,
                        "prompt_type": prompt_type,
                        "prompt_length_words": prompt_length_words,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": input_tokens + output_tokens,
                        "response": response,
                        "response_time": duration,
                        "length": len(response.split()),
                        "readability": readability
                    }

                    logging.info(f"Provider: {provider.upper()} | Model: {model} | Prompt: {prompt_name}")
                    logging.info(f"Prompt Type: {prompt_type} | Prompt Length: {prompt_length_words} words")
                    logging.info(f"Tokens (Input/Output/Total): {input_tokens}/{output_tokens}/{input_tokens + output_tokens}")
                    logging.info(f"Response Time: {duration}s | Words: {len(response.split())}")
                    logging.info(
                        f"Readability - Sentences: {readability['sentence_count']}, "
                        f"Syllables: {readability['syllable_count']}, "
                        f"Flesch Score: {readability['flesch_reading_ease']}"
                    )
                    logging.info(f"Response:\n{response}\n{'-'*50}")

                except Exception as e:
                    logging.error(f"Error querying {provider} ({model}) with {prompt_name}: {e}")
                    results[key] = {
                        "provider": provider,
                        "model": model,
                        "prompt_name": prompt_name,
                        "response": f"Error: {e}",
                        "response_time": None,
                        "length": 0,
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "total_tokens": 0,
                        "prompt_type": "Unknown",
                        "prompt_length_words": 0,
                        "readability": {
                            "sentence_count": 0,
                            "syllable_count": 0,
                            "flesch_reading_ease": "N/A"
                        }
                    }

    print("\n📊 LLM Comparison Results:")
    for key, result in results.items():
        print(f"\n🔹 {result['provider'].upper()} ({result['model']}) | Prompt: {result['prompt_name']}")
        print(f"🧠 Prompt Type: {result['prompt_type']} | Prompt Length: {result['prompt_length_words']} words")
        print(f"🔢 Tokens - Input: {result['input_tokens']} | Output: {result['output_tokens']} | Total: {result['total_tokens']}")
        print(f"⏱️ Response Time: {result['response_time']} seconds")
        print(f"📝 Response Length: {result['length']} words")
        print(
            f"📚 Readability - Sentences: {result['readability']['sentence_count']} | "
            f"Syllables: {result['readability']['syllable_count']} | "
            f"Flesch Score: {result['readability']['flesch_reading_ease']}"
        )
        print(f"📤 Output:\n{result['response']}")
        print("\n" + "=" * 50)

    print("\n✅ All results have been logged to `llm_comparison.log`.")
