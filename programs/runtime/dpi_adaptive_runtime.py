import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import (
    extract_observables
)

from core.telemetry.schema import (
    build_telemetry_event
)

from core.session.session import (
    create_runtime_session
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Adaptive Runtime Session: "
    f"{session['session_id']}"
)

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(
    -20,
    20,
    3000
)

# ----------------------------------------
# SOURCE FIELD
# ----------------------------------------

source_field = np.exp(
    -(detector_x)**2 / 20
)

# ----------------------------------------
# INITIAL CONDITIONS
# ----------------------------------------

noise_strength = 0.18

adaptation_rate = 0.015

history = []

# ----------------------------------------
# ADAPTIVE EVOLUTION LOOP
# ----------------------------------------

for step in range(20):

    coherence_pattern = np.cos(
        detector_x * 2
    )

    noise = np.random.normal(
        0,
        noise_strength,
        detector_x.shape
    )

    field = (
        source_field
        * coherence_pattern
    )

    field += noise

    intensity = np.abs(field)**2

    intensity /= np.max(intensity)

    observables = extract_observables(
        detector_x,
        intensity
    )

    peak_count = observables[
        "peak_count"
    ]

    coherence_width = observables[
        "coherence_width"
    ]

    # ----------------------------------------
    # ADAPTIVE RESPONSE
    # ----------------------------------------

    if peak_count > 180:

        noise_strength -= adaptation_rate

    else:

        noise_strength += (
            adaptation_rate * 0.25
        )

    noise_strength = max(
        0.0,
        noise_strength
    )

    observables["noise_strength"] = (
        float(noise_strength)
    )

    observables["step"] = step

    history.append(observables)

    print(
        f"Step {step} | "
        f"Noise: {noise_strength:.4f} | "
        f"Peaks: {peak_count}"
    )

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry = build_telemetry_event(
    history[-1]
)

output_path = (
    f"{session['session_path']}/"
    "adaptive_telemetry.json"
)

with open(output_path, "w") as f:

    json.dump(
        telemetry.model_dump(),
        f,
        indent=4
    )

print(
    f"\nSaved adaptive telemetry: "
    f"{output_path}"
)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

steps = [
    h["step"]
    for h in history
]

noise_history = [
    h["noise_strength"]
    for h in history
]

peak_history = [
    h["peak_count"]
    for h in history
]

plt.figure(figsize=(14, 8))

plt.plot(
    steps,
    noise_history,
    label="Adaptive Noise Strength"
)

plt.plot(
    steps,
    peak_history,
    label="Peak Count"
)

plt.title(
    "Adaptive DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Adaptive Metric")

plt.grid(True)

plt.legend()

image_output = (
    f"{session['session_path']}/"
    "adaptive_runtime.png"
)

plt.savefig(image_output)

plt.close()

print(
    f"Saved adaptive runtime: "
    f"{image_output}"
)

print(
    "\nAdaptive DPI Runtime Complete."
)
