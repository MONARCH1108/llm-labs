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
    char_count = sum(len(token.text) for token in doc if token.is_alpha)

    return {
        "sentence_count": sentence_count,
        "word_count": word_count,
        "syllable_count": syllable_count,
        "polysyllable_count": polysyllable_count,
        "char_count": char_count
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

def compute_coleman_liau_index(char_count: int, word_count: int, sentence_count: int) -> float | str:
    try:
        if word_count > 0 and sentence_count > 0:
            L = (char_count / word_count) * 100
            S = (sentence_count / word_count) * 100
            score = (0.0588 * L) - (0.296 * S) - 15.8
            return round(score, 2)
        return "N/A"
    except ZeroDivisionError:
        return "N/A"
    
def compute_gunning_fog_index(sentence_count: int, word_count: int, polysyllable_count: int) -> float | str:
    try:
        if sentence_count > 0 and word_count > 0:
            score = 0.4 * ((word_count / sentence_count) + 100 * (polysyllable_count / word_count))
            return round(score, 2)
        return "N/A"
    except ZeroDivisionError:
        return "N/A"

def compute_automated_readability_index(char_count: int, word_count: int, sentence_count: int) -> float | str:
    try:
        if word_count > 0 and sentence_count > 0:
            score = 4.71 * (char_count / word_count) + 0.5 * (word_count / sentence_count) - 21.43
            return round(score, 2)
        return "N/A"
    except ZeroDivisionError:
        return "N/A"

def compute_dale_chall_index(text: str) -> float:
    return round(textstat.dale_chall_readability_score(text), 2)

def compute_forcast_index(text: str) -> float:
    words = [token.text for token in nlp(text) if token.is_alpha]
    sample = words[:150]  # first 150 words
    monosyllables = sum(1 for w in sample if textstat.syllable_count(w) == 1)
    score = 20 - (monosyllables / 10)
    return round(score, 2)

def compute_linsear_write_index(text: str) -> float:
    words = [token.text for token in nlp(text) if token.is_alpha]
    sentences = list(nlp(text).sents)
    sample_words = words[:100]  # first 100 words
    easy = sum(1 for w in sample_words if textstat.syllable_count(w) <= 2)
    hard = sum(1 for w in sample_words if textstat.syllable_count(w) >= 3)
    sentence_count = max(1, len(sentences))
    score = (easy + 3 * hard) / sentence_count
    if score > 20:
        score /= 2
    else:
        score -= 2
    return round(score, 2)

def compute_lix(text: str) -> float:
    doc = nlp(text)
    sentences = list(doc.sents)
    words = [token.text for token in doc if token.is_alpha]
    word_count = len(words)
    sentence_count = max(1, len(sentences))
    long_words = sum(1 for w in words if len(w) > 6)
    score = (word_count / sentence_count) + 100 * (long_words / word_count)
    return round(score, 2)

def compute_rix(text: str) -> float:
    doc = nlp(text)
    sentences = list(doc.sents)
    words = [token.text for token in doc if token.is_alpha]
    long_words = sum(1 for w in words if len(w) > 6)
    sentence_count = max(1, len(sentences))
    score = long_words / sentence_count
    return round(score, 2)

def get_readability_metrics(text: str) -> dict:
    stats = get_text_stats(text)
    flesch = compute_flesch_reading_ease(
        stats["sentence_count"], stats["word_count"], stats["syllable_count"]
    )
    smog = compute_smog_index(
        stats["sentence_count"], stats["polysyllable_count"]
    )
    coleman_liau = compute_coleman_liau_index(
        stats["char_count"], stats["word_count"], stats["sentence_count"]
    )
    gunning_fog = compute_gunning_fog_index(
        stats["sentence_count"], stats["word_count"], stats["polysyllable_count"]
    )
    ari = compute_automated_readability_index(
        stats["char_count"], stats["word_count"], stats["sentence_count"]
    )
    dale_chall = compute_dale_chall_index(
        text
    )
    forcast = compute_forcast_index(
        text
    )
    linsear_write = compute_linsear_write_index(
        text
    )
    lix = compute_lix(
        text
    )
    rix = compute_rix(
        text
    )
    return {
        "sentence_count": stats["sentence_count"],
        "word_count": stats["word_count"],
        "syllable_count": stats["syllable_count"],
        "polysyllable_count": stats["polysyllable_count"],
        "char_count": stats["char_count"],
        "flesch_reading_ease": flesch,
        "smog_index": smog,
        "coleman_liau_index": coleman_liau,
        "gunning_fog_index": gunning_fog,
        "automated_readability_index": ari,
        "dale_chall_index": dale_chall,
        "forcast_index": forcast,
        "linsear_write_index": linsear_write,
        "lix": lix,
        "rix": rix,
    }