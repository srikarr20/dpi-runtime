def analyze_detector_behavior(
    semantic_history
):

    stable_count = semantic_history.count(
        "stable"
    )

    transitional_count = semantic_history.count(
        "transitional"
    )

    exploratory_count = semantic_history.count(
        "exploratory"
    )

    collapsed_count = semantic_history.count(
        "collapsed"
    )

    total = len(semantic_history)

    # ----------------------------------------
    # META-CLASSIFICATION
    # ----------------------------------------

    if exploratory_count > total * 0.4:

        return "volatile"

    if stable_count > total * 0.6:

        return "stabilized"

    if transitional_count > total * 0.5:

        return "adaptive"

    if collapsed_count > total * 0.3:

        return "degraded"

    return "mixed"
