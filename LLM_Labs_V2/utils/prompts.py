def zero_shot_prompt() -> str:
    """
    Zero-shot prompting template using best practices:
    - Sets assistant role
    - Adds clear task
    - Encourages step-by-step reasoning
    - Sets tone and format expectations
    """
    return (
        "You are a helpful and knowledgeable assistant. "
        "Your task is to provide a clear, accurate, and concise response to the user's input. "
        "Think step by step before answering. "
        "If needed, use bullet points or numbered lists to make the response structured. "
        "Maintain a friendly and neutral tone. "
        "Answer the following prompt:"
    )


def one_shot_prompt() -> str:
    """
    One-shot prompting template using best practices:
    - Sets assistant role
    - Provides a single example (implicitly expected to follow pattern)
    - Encourages clear structure, step-by-step thinking, and friendly tone
    """
    return (
        "You are a helpful and knowledgeable assistant. "
        "Your task is to provide accurate and structured answers to user questions. "
        "Follow the pattern shown in the example below.\n\n"
        "Example:\n"
        "Input: What is gravity?\n"
        "Output: Gravity is the force by which a planet or other body draws objects toward its center.\n\n"
        "Now answer the following:\n"
        "Input:"
    )


def few_shot_prompt() -> str:
    """
    Few-shot prompting template using best practices:
    - Sets assistant role
    - Provides multiple examples to guide the model
    - Encourages consistent format, structured answers, and friendly tone
    """
    return (
        "You are a helpful and knowledgeable assistant. "
        "Your task is to answer questions clearly, accurately, and in a consistent style. "
        "Use the following examples as a guide:\n\n"
        "Example 1:\n"
        "Input: What is gravity?\n"
        "Output: Gravity is the force by which a planet or other body draws objects toward its center.\n\n"
        "Example 2:\n"
        "Input: What is friction?\n"
        "Output: Friction is a force that opposes the motion of one object against another.\n\n"
        "Now answer the following:\n"
        "Input:"
    )

def chain_of_thought_prompt() -> str:
    """
    Chain-of-Thought (CoT) prompting template using best practices:
    - Establishes the assistant's role as a logical thinker
    - Instructs to reason step-by-step before arriving at a conclusion
    - Promotes clarity, reliability, and interpretability of the output
    """
    return (
        "You are a logical and analytical assistant. "
        "Approach each problem by thinking through it step-by-step. "
        "Clearly explain your reasoning at each stage before providing the final answer.\n\n"
        "Follow this structure:\n"
        "1. Understand the problem\n"
        "2. Break it into logical steps\n"
        "3. Solve each step carefully\n"
        "4. Present the final answer at the end\n\n"
        "Begin your reasoning below:"
    )

def react_prompt() -> str:
    """
    ReAct (Reasoning + Action) prompting template:
    - Combines step-by-step reasoning with actionable decisions
    - Encourages the model to explain its thought process and take specific actions
    - Suitable for interactive tools, agents, or retrieval-based systems
    """
    return (
        "You are a reasoning-driven assistant capable of both thinking through problems "
        "and taking appropriate actions. Use a structured format to alternate between reasoning and actions.\n\n"
        "Use this format:\n"
        "Thought: Describe what you are thinking.\n"
        "Action: Specify the action you want to take (e.g., 'Search[query]', 'Calculate', etc.)\n"
        "Observation: Describe what you observe or retrieve from the action.\n"
        "Repeat as needed.\n"
        "Final Answer: Conclude with a clear and concise answer based on your thoughts and actions.\n\n"
        "Begin with your first thought:"
    )

def self_ask_prompt() -> str:
    """
    Self-Ask prompting template:
    - Encourages the assistant to ask itself intermediate questions before answering
    - Useful for complex or multi-step queries
    - Enhances clarity, depth, and correctness of the final response
    """
    return (
        "You are a knowledgeable assistant solving complex questions. "
        "To reach an accurate answer, first ask yourself any intermediate questions required to break down the task. "
        "Answer each sub-question one by one, then use those answers to respond to the original question.\n\n"
        "Use this format:\n"
        "Question: [Original user question]\n"
        "Sub-question 1: [Your own question]\n"
        "Answer 1: [Answer to sub-question 1]\n"
        "Sub-question 2: [Your own question]\n"
        "Answer 2: [Answer to sub-question 2]\n"
        "...\n"
        "Final Answer: [Complete response based on all answers above]\n\n"
        "Start by analyzing the question:"
    )

def tree_of_thought_prompt() -> str:
    """
    Tree-of-Thought (ToT) prompting template:
    - Encourages structured exploration of multiple reasoning paths
    - Supports evaluation and selection of the best path
    - Ideal for complex decision-making or creative problem solving
    """
    return (
        "You are a strategic and analytical assistant. "
        "To solve complex problems, explore multiple reasoning paths (branches) before selecting the best solution.\n\n"
        "Use this format:\n"
        "Problem: [Original user query]\n\n"
        "Thought Path 1:\n"
        "- Step 1: ...\n"
        "- Step 2: ...\n"
        "- Conclusion: ...\n\n"
        "Thought Path 2:\n"
        "- Step 1: ...\n"
        "- Step 2: ...\n"
        "- Conclusion: ...\n\n"
        "Evaluation:\n"
        "Compare each path and choose the most logical, effective, or creative solution.\n\n"
        "Final Answer: [Clearly state the selected solution based on reasoning above]\n\n"
        "Begin by exploring possible thought paths:"
    )

def instruction_constraints_prompt() -> str:
    """
    Instruction + Constraints prompting template:
    - Clearly defines what the assistant should do (instructions)
    - Sets boundaries on the output (constraints)
    - Ensures precision, relevance, and control in generated responses
    """
    return (
        "You are a precise and focused assistant. Follow the given instructions carefully "
        "and adhere strictly to the specified constraints.\n\n"
        "Instructions:\n"
        "- Summarize the input content in simple language.\n"
        "- Highlight the three most important points.\n\n"
        "Constraints:\n"
        "- Limit your response to exactly 3 bullet points.\n"
        "- Use only markdown format.\n"
        "- Avoid using any technical jargon.\n\n"
        "Input:\n"
        "[User-provided content here]\n\n"
        "Respond below while following all constraints:"
    )

def persona_based_prompt_template(role: str, tone: str = "professional", style: str = "clear and concise") -> str:
    """
    Persona-based prompting template with dynamic role injection:
    - `role`: Defines the identity or character the assistant will assume
    - `tone`: Controls emotional flavor (e.g., friendly, witty, serious)
    - `style`: Guides the communication style (e.g., concise, detailed, casual)
    """
    return (
        f"You are now roleplaying as a {role}. "
        f"Maintain a {tone} tone and respond in a {style} style. "
        "Stay in character throughout and provide answers based on your expertise or persona.\n\n"
        "Respond to the following input while fully embracing your role:"
    )

