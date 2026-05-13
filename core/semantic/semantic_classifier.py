def classify_semantic_state(
    peak_count,
    coherence_width,
    intensity_variance
):

    # ----------------------------------------
    # LOW-ORDER REGIMES
    # ----------------------------------------

    if peak_count < 120:

        return "collapsed"

    # ----------------------------------------
    # STABLE MANIFOLD
    # ----------------------------------------

    if (
        peak_count < 170
        and coherence_width < 4
    ):

        return "stable"

    # ----------------------------------------
    # TRANSITIONAL MANIFOLD
    # ----------------------------------------

    if (
        peak_count < 190
        and intensity_variance > 0.01
    ):

        return "transitional"

    # ----------------------------------------
    # EXPLORATORY MANIFOLD
    # ----------------------------------------

    if peak_count >= 190:

        return "exploratory"

    # ----------------------------------------
    # DEFAULT
    # ----------------------------------------

    return "unknown"
