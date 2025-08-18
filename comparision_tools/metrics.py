import spacy
import textstat

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def get_text_stats(text: str) -> dict:
    doc = nlp(text)
    sentence_count = len(list(doc.sents))
    word_count = len([token for token in doc if token.is_alpha])
    syllable_count = textstat.syllable_count(text)

    return {
        "sentence_count": sentence_count,
        "word_count": word_count,
        "syllable_count": syllable_count
    }

def compute_flesch_reading_ease(sentence_count: int, word_count: int, syllable_count: int) -> float | str:
    try:
        if sentence_count > 0 and word_count > 0:
            score = (
                206.835
                - 1.015 * (word_count / sentence_count)
                - 84.6 * (syllable_count / word_count)
            )
            return round(score, 2)
        return "N/A"
    except ZeroDivisionError:
        return "N/A"
    
def get_readability_metrics(text: str) -> dict:
    stats = get_text_stats(text)
    flesch = compute_flesch_reading_ease(
        stats["sentence_count"], stats["word_count"], stats["syllable_count"]
    )
    return {
        "sentence_count": stats["sentence_count"],
        "syllable_count": stats["syllable_count"],
        "flesch_reading_ease": flesch
    }