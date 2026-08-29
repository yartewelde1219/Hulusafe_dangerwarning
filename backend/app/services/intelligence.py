WEIGHTS = {
    "impact": 0.25,
    "nlp_evidence": 0.20,
    "source_credibility": 0.20,
    "agreement": 0.20,
    "recency": 0.10,
    "location_confidence": 0.05,
}

LEVELS = (
    (0.85, "critical"),
    (0.7, "high"),
    (0.45, "moderate"),
    (0.2, "low"),
    (0.0, "none"),
)


def impact_score(deaths, injuries, displaced, missing, damage) -> float:
    score = 0.0
    if deaths:
        score += min(deaths / 20, 1.0) * 0.45
    if injuries:
        score += min(injuries / 50, 1.0) * 0.2
    if displaced:
        score += min(displaced / 1000, 1.0) * 0.25
    if missing:
        score += min(missing / 20, 1.0) * 0.1
    if damage:
        score = min(score + 0.15, 1.0)
    return min(score, 1.0)


def severity_score(
    *,
    impact: float,
    nlp_evidence: float,
    source_credibility: float,
    agreement: float,
    recency: float,
    location_confidence: float,
) -> float:
    return (
        impact * WEIGHTS["impact"]
        + nlp_evidence * WEIGHTS["nlp_evidence"]
        + source_credibility * WEIGHTS["source_credibility"]
        + agreement * WEIGHTS["agreement"]
        + recency * WEIGHTS["recency"]
        + location_confidence * WEIGHTS["location_confidence"]
    )


def confidence_score(
    *,
    nlp_confidence: float,
    source_confidence: float,
    agreement: float,
    location_confidence: float,
    recency_score: float,
) -> float:
    return (
        0.35 * nlp_confidence
        + 0.25 * source_confidence
        + 0.20 * agreement
        + 0.10 * location_confidence
        + 0.10 * recency_score
    )


def score_to_level(score: float) -> str:
    for threshold, label in LEVELS:
        if score >= threshold:
            return label
    return "none"


def independent_agreement(independent_count: int, total_reports: int) -> float:
    if total_reports <= 0:
        return 0.0
    return min(independent_count / max(total_reports, 1), 1.0)
