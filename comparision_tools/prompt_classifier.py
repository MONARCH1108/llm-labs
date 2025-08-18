def classify_prompt(prompt: str) -> str:
    prompt = prompt.lower()
    if any(word in prompt for word in ["prove", "solve", "equation", "math", "calculate"]):
        return "Math"
    elif any(word in prompt for word in ["story", "poem", "imagine", "creative"]):
        return "Creative"
    elif any(word in prompt for word in ["why", "how", "explain", "analyze", "reason"]):
        return "Reasoning"
    elif any(word in prompt for word in ["when", "where", "what", "who", "define", "describe"]):
        return "Knowledge"
    else:
        return "General"
