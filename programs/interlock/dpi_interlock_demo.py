import json

from core.interlock.interlock import evaluate_observability

# ----------------------------------------
# LOAD CALIBRATION RESULTS
# ----------------------------------------

with open(
    "outputs/telemetry/calibration_results.json",
    "r"
) as f:

    calibration = json.load(f)

# ----------------------------------------
# BASELINE STATE
# ----------------------------------------

baseline = calibration["coherent"]

# ----------------------------------------
# TEST STATES
# ----------------------------------------

test_states = [
    "noisy",
    "decoherent",
    "collapsed"
]

# ----------------------------------------
# EVALUATE STATES
# ----------------------------------------

for state in test_states:

    print(f"\nEvaluating state: {state}")

    current = calibration[state]

    alerts = evaluate_observability(
        baseline,
        current
    )

    if alerts:

        print("\nINTERLOCK ALERTS:")

        for alert in alerts:

            print(f"- {alert}")

    else:

        print(
            "State within observability thresholds."
        )
