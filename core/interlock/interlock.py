def evaluate_observability(
    baseline,
    current
):

    alerts = []

    # ----------------------------------------
    # COHERENCE WIDTH DRIFT
    # ----------------------------------------

    width_ratio = (
        current["coherence_width"]
        / baseline["coherence_width"]
    )

    if width_ratio > 2.0:

        alerts.append(
            "WARNING: coherence width drift detected"
        )

    # ----------------------------------------
    # PEAK COUNT INSTABILITY
    # ----------------------------------------

    peak_ratio = (
        current["peak_count"]
        / baseline["peak_count"]
    )

    if peak_ratio > 10:

        alerts.append(
            "WARNING: observability peak instability"
        )

    # ----------------------------------------
    # VARIANCE DEGRADATION
    # ----------------------------------------

    variance_ratio = (
        current["intensity_variance"]
        / baseline["intensity_variance"]
    )

    if variance_ratio < 0.5:

        alerts.append(
            "WARNING: observability variance collapse"
        )

    return alerts
