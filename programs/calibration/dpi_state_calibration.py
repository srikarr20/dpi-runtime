import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import extract_observables

# ----------------------------------------
# CALIBRATION STATES
# ----------------------------------------

states = {

    "coherent": {
        "noise_strength": 0.00,
        "modulation_strength": 1.00
    },

    "noisy": {
        "noise_strength": 0.15,
        "modulation_strength": 1.00
    },

    "decoherent": {
        "noise_strength": 0.35,
        "modulation_strength": 0.50
    },

    "collapsed": {
        "noise_strength": 0.60,
        "modulation_strength": 0.10
    }
}

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(-20, 20, 3000)

# ----------------------------------------
# RESULTS STORAGE
# ----------------------------------------

calibration_results = {}

# ----------------------------------------
# PROCESS STATES
# ----------------------------------------

for state_name, config in states.items():

    print(f"\nProcessing state: {state_name}")

    # ----------------------------------------
    # SOURCE FIELD
    # ----------------------------------------

    source_field = np.exp(-(detector_x)**2 / 20)

    # ----------------------------------------
    # COHERENCE MODULATION
    # ----------------------------------------

    coherence_pattern = (
        np.cos(detector_x * 2)
        * config["modulation_strength"]
    )

    # ----------------------------------------
    # NOISE
    # ----------------------------------------

    noise = np.random.normal(
        0,
        config["noise_strength"],
        size=len(detector_x)
    )

    # ----------------------------------------
    # OBSERVABILITY FIELD
    # ----------------------------------------

    field = source_field * coherence_pattern

    field += noise

    # ----------------------------------------
    # DETECTOR INTENSITY
    # ----------------------------------------

    intensity = np.abs(field)**2

    intensity /= np.max(intensity)

    # ----------------------------------------
    # EXTRACT OBSERVABLES
    # ----------------------------------------

    observables = extract_observables(
        detector_x,
        intensity
    )

    calibration_results[state_name] = observables

    # ----------------------------------------
    # VISUALIZATION
    # ----------------------------------------

    plt.figure(figsize=(14, 6))

    plt.plot(
        detector_x,
        intensity,
        label=f"{state_name} observability"
    )

    plt.title(
        f"DPI Calibration State — {state_name}"
    )

    plt.xlabel("Detector Position")

    plt.ylabel("Normalized Intensity")

    plt.grid(True)

    # ----------------------------------------
    # OVERLAY METRICS
    # ----------------------------------------

    metrics_text = (
        f"Peak Intensity: {observables['peak_intensity']:.2f}\n"
        f"Mean Intensity: {observables['mean_intensity']:.4f}\n"
        f"Variance: {observables['intensity_variance']:.4f}\n"
        f"Coherence Width: {observables['coherence_width']:.2f}\n"
        f"Peak Count: {observables['peak_count']}"
    )

    plt.text(
        0.02,
        0.95,
        metrics_text,
        transform=plt.gca().transAxes,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.legend()

    # ----------------------------------------
    # SAVE IMAGE
    # ----------------------------------------

    output_path = (
        f"outputs/images/{state_name}_calibration.png"
    )

    plt.savefig(output_path)

    print(f"Saved: {output_path}")

    plt.close()

# ----------------------------------------
# SAVE CALIBRATION RESULTS
# ----------------------------------------

with open(
    "outputs/telemetry/calibration_results.json",
    "w"
) as f:

    json.dump(
        calibration_results,
        f,
        indent=4
    )

print("\nCalibration complete.")
