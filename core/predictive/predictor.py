def predict_future_state(
    detector
):

    trust = detector["trust"]

    noise = detector["noise"]

    energy = detector["energy"]

    # ----------------------------------------
    # SIMPLE FUTURE HEURISTIC
    # ----------------------------------------

    future_score = (
        trust
        + energy
        - noise
    )

    # ----------------------------------------
    # FUTURE CLASSIFICATION
    # ----------------------------------------

    if future_score > 1.5:

        return "dominant"

    elif future_score > 1.0:

        return "stable"

    elif future_score > 0.7:

        return "fragile"

    else:

        return "collapse"
