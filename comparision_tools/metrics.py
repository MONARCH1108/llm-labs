import spacy
import textstat

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def get_text_stats(text: str) -> dict:
    doc = nlp(text)
    sentence_count = len(list(doc.sents))
    word_count = len([token for token in doc if token.is_alpha])
    syllable_count = textstat.syllable_count(text)
    polysyllable_count = 0
    for token in doc:
        if token.is_alpha and textstat.syllable_count(token.text) >= 3:
            polysyllable_count += 1

    return {
        "sentence_count": sentence_count,
        "word_count": word_count,
        "syllable_count": syllable_count,
        "polysyllable_count": polysyllable_count
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
    
def compute_smog_index(sentence_count: int, polysyllable_count: int) -> float | str:
    try:
        if sentence_count >= 3 and polysyllable_count > 0:  # SMOG is only valid if >=3 sentences
            score = 1.0430 * ((polysyllable_count * (30 / sentence_count)) ** 0.5) + 3.1291
            return round(score, 2)
        return "N/A"
    except ZeroDivisionError:
        return "N/A"
    
def get_readability_metrics(text: str) -> dict:
    stats = get_text_stats(text)
    flesch = compute_flesch_reading_ease(
        stats["sentence_count"], stats["word_count"], stats["syllable_count"]
    )
    smog = compute_smog_index(
        stats["sentence_count"], stats["polysyllable_count"]
    )
    return {
        "sentence_count": stats["sentence_count"],
        "syllable_count": stats["syllable_count"],
        "flesch_reading_ease": flesch,
        "smog_index": smog
    }