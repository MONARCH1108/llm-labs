import re
import os
from datetime import datetime
from utils.llms import query_gemini_llm


LOG_FILE = "llm_comparison.log"
REPORT_FILE = f"llm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def extract_log_metrics():
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError("Log file not found. Ensure comparison ran successfully.")

    with open(LOG_FILE, "r") as f:
        content = f.read()

    entries = content.split("--------------------------------------------------")
    summary = []

    for entry in entries:
        try:
            provider = re.search(r"Provider: (\w+)", entry).group(1)
            model = re.search(r"Model: ([\w\-\.:]+)", entry).group(1)
            prompt = re.search(r"Prompt: ([\w_]+)", entry).group(1)
            prompt_type = re.search(r"Prompt Type: ([\w\s]+)", entry).group(1)
            input_tokens, output_tokens, total_tokens = map(int, re.findall(r"Tokens \(Input/Output/Total\): (\d+)/(\d+)/(\d+)", entry)[0])
            response_time = float(re.search(r"Response Time: ([\d\.]+)s", entry).group(1))
            flesch = re.search(r"Flesch Score: ([\d\.NA]+)", entry).group(1)

            summary.append({
                "provider": provider,
                "model": model,
                "prompt": prompt,
                "prompt_type": prompt_type,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "response_time": response_time,
                "flesch_score": flesch
            })
        except Exception:
            continue

    return summary


def generate_report(summary: list, user_question: str):
    grouped = {}

    for item in summary:
        key = f"{item['provider']}::{item['model']}"
        grouped.setdefault(key, []).append(item)

    report_lines = ["# 📊 LLM Performance Report\n"]
    report_lines.append(f"**User Question:** {user_question}\n")

    for key, records in grouped.items():
        report_lines.append(f"## 🔹 {key}")
        avg_input = sum(r["input_tokens"] for r in records) / len(records)
        avg_output = sum(r["output_tokens"] for r in records) / len(records)
        avg_response_time = sum(r["response_time"] for r in records) / len(records)
        flesch_scores = [float(r["flesch_score"]) for r in records if r["flesch_score"] != "N/A"]
        avg_flesch = round(sum(flesch_scores) / len(flesch_scores), 2) if flesch_scores else "N/A"

        report_lines.append(f"- 🔢 Average Input Tokens: {avg_input:.2f}")
        report_lines.append(f"- 🔢 Average Output Tokens: {avg_output:.2f}")
        report_lines.append(f"- ⏱️ Average Response Time: {avg_response_time:.2f} sec")
        report_lines.append(f"- 📚 Avg. Flesch Reading Ease: {avg_flesch}")
        report_lines.append("")

    score_text = "\n".join(report_lines)

    # Ask Gemini to analyze based on these numbers
    gemini_summary = query_gemini_llm(
    model="gemini-2.0-flash",
    user_input=score_text,
    prompt=(
        "You are an objective evaluator. Given the performance metrics for multiple LLMs, "
        "analyze only the numeric data below without any assumptions or external context. "
        "Identify which model performs better strictly based on the following measurable factors:\n\n"
        "- Average input/output tokens (efficiency)\n"
        "- Average response time (speed)\n"
        "- Average Flesch Reading Ease (clarity/readability)\n\n"
        "DO NOT add any subjective commentary or external knowledge. "
        "Just summarize which model(s) have the strongest numeric performance for each metric, and conclude "
        "which model performed better overall—purely based on these statistics."
    )
    )
    report_lines.append("## 🧠 Gemini Insights\n")
    report_lines.append(gemini_summary)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n✅ Report generated: {REPORT_FILE}")
    return REPORT_FILE
