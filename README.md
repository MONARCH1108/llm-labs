# 📁 LLM Labs - Directory Structure


```
LLM_Labs_V1/
│
├─ comparision_tools/
│   ├─ metrics.py
│   │   ├─ get_text_stats(text: str) -> dict
│   │   ├─ compute_flesch_reading_ease(sentence_count: int, word_count: int, syllable_count: int) -> float|str
│   │   ├─ compute_smog_index(sentence_count: int, polysyllable_count: int) -> float|str
│   │   ├─ compute_coleman_liau_index(char_count: int, word_count: int, sentence_count: int) -> float|str
│   │   ├─ compute_gunning_fog_index(sentence_count: int, word_count: int, polysyllable_count: int) -> float|str
│   │   ├─ compute_automated_readability_index(char_count: int, word_count: int, sentence_count: int) -> float|str
│   │   ├─ compute_dale_chall_index(text: str) -> float
│   │   ├─ compute_forcast_index(text: str) -> float
│   │   ├─ compute_linsear_write_index(text: str) -> float
│   │   ├─ compute_lix(text: str) -> float
│   │   ├─ compute_rix(text: str) -> float
│   │   └─ get_readability_metrics(text: str) -> dict
│   │
│   ├─ prompt_classifier.py
│   │   └─ classify_prompt(prompt: str) -> str
│   │
│   └─ tokenizer.py
│       └─ count_tokens(text: str) -> int
│
├─ utils/
│   ├─ comparison.py
│   │   └─ run_comparative_evaluation(providers_models: dict, prompts: dict, user_input: str)
│   │
│   ├─ llms.py
│   │   ├─ query_groq_llm(user_input: str, model: str, prompt: str) -> str
│   │   ├─ query_gemini_llm(user_input: str, model: str, prompt: str) -> str
│   │   └─ query_ollama_llm(user_input: str, model: str, prompt: str) -> str
│   │
│   ├─ prompts.py
│   │   ├─ zero_shot_prompt() -> str
│   │   ├─ one_shot_prompt() -> str
│   │   ├─ few_shot_prompt() -> str
│   │   ├─ chain_of_thought_prompt() -> str
│   │   ├─ react_prompt() -> str
│   │   ├─ self_ask_prompt() -> str
│   │   ├─ tree_of_thought_prompt() -> str
│   │   ├─ instruction_constraints_prompt() -> str
│   │   └─ persona_based_prompt_template(role: str, tone: str = "professional", style: str = "clear and concise") -> str
│   │
│   └─ report_generator.py
│       ├─ safe_float(value: str)
│       ├─ extract_log_metrics() -> list
│       └─ generate_report(summary: list, user_question: str)
│
└─ app.py
    ├─ select_prompt_templates() -> dict
    ├─ run_comparative()
    ├─ run_single_llm_chat()
    └─ main()
```

## Key Corrections from Your Original Format:

### 1. **File Organization**:

- `metrics.py` contains all readability functions (not in `tokenizer.py`)
- `llms.py` contains all LLM query functions (separate from `comparison.py`)
- `prompts.py` contains all prompt templates (separate from `comparison.py`)

### 2. **Function Distribution**:

- **`metrics.py`**: 12 functions for text analysis and readability
- **`tokenizer.py`**: Only 1 function for token counting
- **`llms.py`**: 3 LLM provider functions
- **`prompts.py`**: 9 prompting strategy functions
- **`comparison.py`**: 1 main orchestration function
- **`report_generator.py`**: 3 functions for report generation

### 3. **Missing Functions Added**:

- `safe_float()` in `report_generator.py`
- All individual readability metric functions in `metrics.py`
- Proper parameter types and return types specified

### 4. **Accurate File Count**:

- **Total Files**: 7 Python files
- **Total Functions**: 30 functions
- **Modules**: 2 main directories (`comparision_tools/`, `utils/`)