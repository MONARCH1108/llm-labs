import subprocess
from utils.llms import query_groq_llm, query_gemini_llm, query_ollama_llm
from utils.prompts import (
    zero_shot_prompt, one_shot_prompt, few_shot_prompt,
    chain_of_thought_prompt, react_prompt, self_ask_prompt,
    tree_of_thought_prompt, instruction_constraints_prompt,
    persona_based_prompt_template
)
from utils.comparison import run_comparative_evaluation
from utils.report_generator import extract_log_metrics, generate_report


def select_prompt_templates():
    print("\nChoose Prompting Strategies (comma-separated numbers):")
    prompt_mapping = {
        "1": zero_shot_prompt,
        "2": one_shot_prompt,
        "3": few_shot_prompt,
        "4": chain_of_thought_prompt,
        "5": react_prompt,
        "6": self_ask_prompt,
        "7": tree_of_thought_prompt,
        "8": instruction_constraints_prompt,
        "9": persona_based_prompt_template
    }
    for key, fn in prompt_mapping.items():
        print(f"{key}. {fn.__name__.replace('_', ' ').title()}")

    choices = input("Enter prompt numbers (e.g., 1,3,6): ").strip().split(',')
    prompt_templates = {}

    for choice in choices:
        choice = choice.strip()
        if choice == "9":
            role = input("Enter persona role (e.g., detective): ").strip()
            tone = input("Enter tone (e.g., friendly, serious): ").strip()
            style = input("Enter style (e.g., concise, detailed): ").strip()
            prompt_templates[f"persona_{role}_{tone}_{style}"] = persona_based_prompt_template(role, tone, style)
        elif choice in prompt_mapping:
            fn = prompt_mapping[choice]
            prompt_templates[fn.__name__] = fn()

    return prompt_templates


def run_comparative():
    print("\n🔍 Comparative LLM Evaluation")

    print("\nSelect LLM Providers (comma-separated numbers):\n1. Groq\n2. Gemini\n3. Ollama")
    selected = input("Enter your choices (e.g., 1,3): ").strip().split(',')
    provider_models = {}

    for choice in selected:
        choice = choice.strip()
        if choice == "1":
            print("\n🔗 Groq Models: https://console.groq.com/docs/models")
            models = input("Enter Groq model IDs (comma-separated): ").strip().split(',')
            provider_models["groq"] = [m.strip() for m in models]
        elif choice == "2":
            print("\n🔗 Gemini Models: https://firebase.google.com/docs/ai-logic/models")
            models = input("Enter Gemini model names (comma-separated): ").strip().split(',')
            provider_models["gemini"] = [m.strip() for m in models]
        elif choice == "3":
            see_local = input("See local Ollama models? (y/n): ").lower()
            if see_local == "y":
                try:
                    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
                    print(result.stdout)
                except subprocess.CalledProcessError:
                    print("⚠️ Failed to list local models.")
            models = input("Enter Ollama model names (comma-separated): ").strip().split(',')
            provider_models["ollama"] = [m.strip() for m in models]

    prompt_templates = select_prompt_templates()
    user_input = input("\n🧠 Enter your question for comparison: ").strip()
    run_comparative_evaluation(provider_models, prompt_templates, user_input)

    print("\n📘 Do you want a detailed performance report based on metrics? (y/n)")
    if input().lower() == "y":
        try:
            summary = extract_log_metrics()
            report_path = generate_report(summary, user_input)
            print(f"📥 You can download the report from: {report_path}")
        except Exception as e:
            print(f"⚠️ Report generation failed: {e}")


def main():
    print("\nChoose Mode:\n1. Single LLM Chat\n2. Comparative Evaluation (Multiple Providers)")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "2":
        run_comparative()
        return

    print("\nChoose LLM Provider:\n1. Groq\n2. Gemini\n3. Ollama (local)")
    provider_choice = input("Enter 1, 2, or 3: ").strip()

    if provider_choice == "1":
        provider = "groq"
        print("\n🔗 Check available Groq models here: https://console.groq.com/docs/models")
        model = input("Enter model ID (e.g., llama3-8b-8192): ").strip()
    elif provider_choice == "2":
        provider = "gemini"
        print("\n🔗 Check available Gemini models here: https://firebase.google.com/docs/ai-logic/models")
        model = input("Enter model name (e.g., gemini-1.5-pro): ").strip()
    elif provider_choice == "3":
        provider = "ollama"
        print("\n🔗 Browse all Ollama models here: https://ollama.com/library")
        see_local = input("Do you want to see locally installed models? (y/n): ").strip().lower()
        if see_local == "y":
            try:
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print("⚠️ Failed to list local models.")
                print(e.stderr)
        model = input("Enter model name (e.g., llama3:latest): ").strip()
    else:
        raise ValueError("❌ Invalid provider selection.")

    prompt_templates = select_prompt_templates()

    print("\n--- Conversation Started ---")
    print("Type 'exit' to quit at any time.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Goodbye! 👋")
            break

        print("\nAssistant:\n")
        prompt_template = list(prompt_templates.values())[0]

        if provider == "groq":
            response = query_groq_llm(model=model, user_input=question, prompt=prompt_template)
        elif provider == "gemini":
            response = query_gemini_llm(model=model, user_input=question, prompt=prompt_template)
        elif provider == "ollama":
            response = query_ollama_llm(model=model, user_input=question, prompt=prompt_template)
        else:
            raise ValueError("❌ Unsupported provider.")

        print(response)
        print("\n----------------------\n")


if __name__ == "__main__":
    main()
