# 📁 LLM Labs - Directory Structure


LLM_Labs_V1 : Testing version only with FrontEnd (Error persist in JS in Html)
Basic_documentation link : https://medium.com/@abhayemani8/llm-labs-149b8174bd33

LLM_Labs_V2 : Current Version, All functions mentioned below 

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
│   │   ├─ persona_based_prompt_template(role: str, tone: str = "professional", style: str = "clear and concise") -> str
|   |   └─ custom_prompt() -> str
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



## 📄 File Details & Functions

### `app.py` - Main Application Entry Point

**Purpose**: Central application controller and user interface

#### Functions:

- **`select_prompt_templates()`**
    - Interactive prompt strategy selection
    - Handles persona-based prompts with custom parameters
    - Returns dictionary of selected prompt templates
- **`run_comparative()`**
    - Orchestrates multi-provider LLM comparison
    - Manages provider/model selection interface
    - Executes comparative evaluation and report generation
- **`run_single_llm_chat()`**
    - Single LLM interactive chat interface
    - Provider and model selection
    - Continuous conversation loop with exit functionality
- **`main()`**
    - Application entry point
    - Mode selection (Single Chat vs Comparative)
    - Route to appropriate functionality

---

### 📁 `comparision_tools/` - Core Analysis Tools

#### `metrics.py` - Text Analysis & Readability Metrics

**Purpose**: Comprehensive text analysis and readability scoring

##### Functions:

- **`get_text_stats(text: str) -> dict`**
    - Extract basic text statistics using spaCy NLP
    - Returns sentence count, word count, syllable count, etc.
- **`compute_flesch_reading_ease(sentence_count, word_count, syllable_count) -> float | str`**
    - Flesch Reading Ease score calculation
    - Score range: 0-100 (higher = easier to read)
- **`compute_smog_index(sentence_count, polysyllable_count) -> float | str`**
    - SMOG (Simple Measure of Gobbledygook) readability
    - Estimates years of education needed to understand text
- **`compute_coleman_liau_index(char_count, word_count, sentence_count) -> float | str`**
    - Coleman-Liau Index calculation
    - Grade level estimation based on character/word ratios
- **`compute_gunning_fog_index(sentence_count, word_count, polysyllable_count) -> float | str`**
    - Gunning Fog Index for readability assessment
    - Estimates years of formal education required
- **`compute_automated_readability_index(char_count, word_count, sentence_count) -> float | str`**
    - Automated Readability Index (ARI)
    - Character-based readability measurement
- **`compute_dale_chall_index(text: str) -> float`**
    - Dale-Chall Readability Score using textstat
    - Vocabulary difficulty assessment
- **`compute_forcast_index(text: str) -> float`**
    - FORCAST (FORmula for CASTing readability)
    - Technical text readability measurement
- **`compute_linsear_write_index(text: str) -> float`**
    - Linsear Write Formula
    - Military readability standard
- **`compute_lix(text: str) -> float`**
    - LIX readability index
    - Swedish-origin text density metric
- **`compute_rix(text: str) -> float`**
    - RIX readability index
    - Long words per sentence measurement
- **`get_readability_metrics(text: str) -> dict`**
    - Master function combining all readability metrics
    - Returns comprehensive analysis dictionary

#### `prompt_classifier.py` - Automatic Prompt Categorization

**Purpose**: Intelligent prompt classification system

##### Functions:

- **`classify_prompt(prompt: str) -> str`**
    - Keyword-based prompt classification
    - Categories: Math, Creative, Reasoning, Knowledge, General
    - Returns classification string

#### `tokenizer.py` - Token Counting Utilities

**Purpose**: Token usage tracking and analysis

##### Functions:

- **`count_tokens(text: str) -> int`**
    - GPT-2 tokenizer-based token counting
    - Supports truncation for long texts
    - Returns integer token count

---

### 📁 `utils/` - Utility Modules

#### `comparison.py` - Comparative Evaluation Engine

**Purpose**: Multi-provider LLM comparison orchestration

##### Functions:

- **`run_comparative_evaluation(providers_models: dict, prompts: dict, user_input: str)`**
    - Main comparison execution function
    - Iterates through all provider/model/prompt combinations
    - Captures performance metrics, readability scores, and responses
    - Logs detailed results and displays summary
    - Handles errors and edge cases gracefully

#### `llms.py` - LLM Provider API Integrations

**Purpose**: Unified interface for multiple LLM providers

##### Functions:

- **`query_groq_llm(user_input: str, model: str, prompt: str) -> str`**
    - Groq API integration with chat completions
    - Handles API key authentication
    - Returns cleaned response text
- **`query_gemini_llm(user_input: str, model: str, prompt: str) -> str`**
    - Google Gemini API integration
    - GenerativeModel interface usage
    - Returns cleaned response text
- **`query_ollama_llm(user_input: str, model: str, prompt: str) -> str`**
    - Local Ollama client integration
    - Chat interface for local models
    - Returns cleaned response text

#### `prompts.py` - Prompting Strategy Templates

**Purpose**: Collection of advanced prompting techniques

##### Functions:

- **`zero_shot_prompt() -> str`**
    - Basic zero-shot prompting template
    - Direct task completion without examples
- **`one_shot_prompt() -> str`**
    - Single example-guided prompting
    - Pattern-following instruction template
- **`few_shot_prompt() -> str`**
    - Multiple example-based learning template
    - Consistent style guidance
- **`chain_of_thought_prompt() -> str`**
    - Step-by-step reasoning template
    - Logical problem decomposition
- **`react_prompt() -> str`**
    - Reasoning + Action framework template
    - Thought-Action-Observation cycle
- **`self_ask_prompt() -> str`**
    - Self-questioning methodology template
    - Sub-question decomposition approach
- **`tree_of_thought_prompt() -> str`**
    - Multiple reasoning path exploration
    - Path evaluation and selection
- **`instruction_constraints_prompt() -> str`**
    - Precise output control template
    - Clear instructions with strict constraints
- **`persona_based_prompt_template(role: str, tone: str, style: str) -> str`**
    - Dynamic persona-based prompting
    - Customizable role, tone, and style parameters

#### `report_generator.py` - Performance Report Generation

**Purpose**: Automated analysis and reporting system

##### Functions:

- **`safe_float(value: str)`**
    - Safe string-to-float conversion
    - Handles "N/A" and invalid values gracefully
- **`extract_log_metrics()`**
    - Parse execution logs for performance data
    - Regex-based metric extraction
    - Returns structured summary list
- **`generate_report(summary: list, user_question: str)`**
    - Generate comprehensive performance report
    - Statistical analysis and interpretation guides
    - Gemini AI-powered insights generation
    - Markdown format output with timestamps

---

## 🔧 Configuration Files

### `requirements.txt` - Python Dependencies

```
groq>=0.4.1
google-generativeai>=0.3.0
ollama>=0.1.7
python-dotenv>=0.19.0
spacy>=3.4.0
textstat>=0.7.3
transformers>=4.21.0
```

### `.env` - Environment Variables (User-Created)

env

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📊 Auto-Generated Files

### `llm_comparison.log` - Execution Logs

- Detailed execution traces
- Performance metrics logging
- Error tracking and debugging info
- Timestamp-based entries

### `llm_report_YYYYMMDD_HHMMSS.txt` - Performance Reports

- Comprehensive analysis reports
- Statistical summaries
- AI-generated insights
- Export-ready format

---

## 🚀 Key Features by Module

### 📈 Analytics & Metrics

- **10+ Readability Indices**: Comprehensive text analysis
- **Token Usage Tracking**: Input/output/total consumption
- **Response Time Metrics**: Performance benchmarking
- **Prompt Classification**: Automatic categorization

### 🤖 LLM Integration

- **Multi-Provider Support**: Groq, Gemini, Ollama
- **Unified API**: Consistent interface across providers
- **Error Handling**: Graceful failure management
- **Model Flexibility**: Support for various model architectures

### 💡 Prompting Strategies

- **9 Advanced Techniques**: From zero-shot to persona-based
- **Dynamic Templates**: Customizable parameters
- **Best Practices**: Industry-standard implementations
- **Scalable Framework**: Easy addition of new strategies

### 📊 Reporting System

- **Automated Analysis**: AI-powered insights
- **Statistical Summaries**: Comprehensive metrics
- **Export Formats**: Multiple output options
- **Visual Interpretations**: Clear metric explanations