def update_trust_score(
    current_score,
    semantic_state
):

    if semantic_state == "stable":

        current_score += 0.05

    elif semantic_state == "transitional":

        current_score += 0.01

    else:

        current_score -= 0.03

    current_score = max(
        0.0,
        min(1.0, current_score)
    )

    return current_score
