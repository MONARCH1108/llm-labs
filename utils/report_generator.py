import re
import os
from datetime import datetime
from utils.llms import query_gemini_llm

LOG_FILE = "llm_comparison.log"
REPORT_FILE = f"llm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def safe_float(value: str):
    """Convert metric to float if possible, else return None."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


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
            input_tokens, output_tokens, total_tokens = map(
                int,
                re.findall(r"Tokens \(Input/Output/Total\): (\d+)/(\d+)/(\d+)", entry)[0]
            )
            response_time = float(re.search(r"Response Time: ([\d\.]+)s", entry).group(1))
            flesch = re.search(r"Flesch Score: ([\d\.NA\-]+)", entry).group(1)
            smog = re.search(r"SMOG Index: ([\d\.NA\-]+)", entry).group(1)
            coleman_liau = re.search(r"Coleman-Liau Index: ([\d\.NA\-]+)", entry).group(1)
            gunning_fog = re.search(r"Gunning Fog Index: ([\d\.NA\-]+)", entry).group(1)
            ari = re.search(r"Automated Readability Index: ([\d\.NA\-]+)", entry).group(1)

            summary.append({
                "provider": provider,
                "model": model,
                "prompt": prompt,
                "prompt_type": prompt_type,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "response_time": response_time,
                "flesch_score": flesch,
                "smog_index": smog,
                "coleman_liau_index": coleman_liau,
                "gunning_fog_index": gunning_fog,
                "ari_index": ari,
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

    # Interpretations
    interpretations = {
        "flesch": (
            "Higher is better (easier to read). "
            "90–100 = Very Easy, 60–70 = Standard, 0–30 = Very Difficult."
        ),
        "smog": (
            "Lower is better (less years of education needed). "
            "Typically 7–9 = Easily understood, >12 = College-level."
        ),
        "coleman_liau": (
            "Lower is better (less grade level required). "
            "8–10 = Middle school level, >12 = High school/college level."
        ),
        "gunning_fog": (
            "Lower is better (less years of formal education required). "
            "7–8 = Near-universal readability, 12+ = College-level."
        ),
        "ari":(
            "Lower is better (grade-level readability). "
            "1–6 = Elementary, 7–12 = Middle/High school, 13+ = College-level."
        ),
    }

    for key, records in grouped.items():
        report_lines.append(f"## 🔹 {key}")
        avg_input = sum(r["input_tokens"] for r in records) / len(records)
        avg_output = sum(r["output_tokens"] for r in records) / len(records)
        avg_response_time = sum(r["response_time"] for r in records) / len(records)

        # Collect scores safely
        flesch_scores = [safe_float(r["flesch_score"]) for r in records if safe_float(r["flesch_score"]) is not None]
        smog_scores = [safe_float(r["smog_index"]) for r in records if safe_float(r["smog_index"]) is not None]
        cli_scores = [safe_float(r["coleman_liau_index"]) for r in records if safe_float(r["coleman_liau_index"]) is not None]
        gf_scores = [safe_float(r["gunning_fog_index"]) for r in records if safe_float(r["gunning_fog_index"]) is not None]
        ari_scores = [safe_float(r["ari_index"]) for r in records if safe_float(r["ari_index"]) is not None]

        # Count failures
        flesch_failures = len(records) - len(flesch_scores)
        smog_failures = len(records) - len(smog_scores)
        cli_failures = len(records) - len(cli_scores)
        gf_failures = len(records) - len(gf_scores)
        ari_failures = len(records) - len(ari_scores)

        # Averages
        avg_flesch = round(sum(flesch_scores) / len(flesch_scores), 2) if flesch_scores else "N/A"
        avg_smog = round(sum(smog_scores) / len(smog_scores), 2) if smog_scores else "N/A"
        avg_cli = round(sum(cli_scores) / len(cli_scores), 2) if cli_scores else "N/A"
        avg_gf = round(sum(gf_scores) / len(gf_scores), 2) if gf_scores else "N/A"
        avg_ari = round(sum(ari_scores) / len(ari_scores), 2) if ari_scores else "N/A"

        report_lines.append(f"- 🔢 Average Input Tokens: {avg_input:.2f}")
        report_lines.append(f"- 🔢 Average Output Tokens: {avg_output:.2f}")
        report_lines.append(f"- ⏱️ Average Response Time: {avg_response_time:.2f} sec")
        report_lines.append(f"- 📚 Avg. Flesch Reading Ease: {avg_flesch} ({interpretations['flesch']}) – ❌ Missing: {flesch_failures}")
        report_lines.append(f"- 📖 Avg. SMOG Index: {avg_smog} ({interpretations['smog']}) – ❌ Missing: {smog_failures}")
        report_lines.append(f"- ✍️ Avg. Coleman-Liau Index: {avg_cli} ({interpretations['coleman_liau']}) – ❌ Missing: {cli_failures}")
        report_lines.append(f"- 🏛 Avg. Gunning Fog Index: {avg_gf} ({interpretations['gunning_fog']}) – ❌ Missing: {gf_failures}")
        report_lines.append(f"- 📐 Avg. Automated Readability Index (ARI): {avg_ari} ({interpretations['ari']}) – ❌ Missing: {ari_failures}")

        report_lines.append("")

    score_text = "\n".join(report_lines)

    # Ask Gemini to analyze based on numbers
    gemini_summary = query_gemini_llm(
        model="gemini-2.0-flash",
        user_input=score_text,
        prompt=(
            "You are an objective evaluator. Given the performance metrics for multiple LLMs, "
            "analyze only the numeric data below without any assumptions or external context. "
            "Identify which model performs better strictly based on the following measurable factors:\n\n"
            "- Average input/output tokens (efficiency)\n"
            "- Average response time (speed)\n"
            "- Average Flesch Reading Ease (clarity/readability)\n"
            "- Average SMOG Index (education level needed)\n"
            "- Average Coleman-Liau Index (grade level)\n"
            "- Average Gunning Fog Index (long-form readability)\n\n"
            "- Average Automated Readability Index (ARI)\n\n"
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
