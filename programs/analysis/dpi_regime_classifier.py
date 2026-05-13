import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

# ----------------------------------------
# LOAD PHASE-SPACE DATA
# ----------------------------------------

with open(
    "outputs/telemetry/phase_space_map.json",
    "r"
) as f:

    phase_data = json.load(f)

# ----------------------------------------
# FEATURES
# ----------------------------------------

coherence_widths = np.array(
    phase_data["coherence_widths"]
)

peak_counts = np.array(
    phase_data["peak_counts"]
)

variance_values = np.array(
    phase_data["variance_values"]
)

noise_levels = np.array(
    phase_data["noise_levels"]
)

# ----------------------------------------
# FEATURE MATRIX
# ----------------------------------------

X = np.column_stack([
    coherence_widths,
    peak_counts,
    variance_values
])

# ----------------------------------------
# K-MEANS CLUSTERING
# ----------------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)

labels = kmeans.fit_predict(X)

# ----------------------------------------
# REGIME LABELING
# ----------------------------------------

regime_names = {
    0: "stable",
    1: "transitional",
    2: "unstable"
}

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

scatter = plt.scatter(
    noise_levels,
    peak_counts,
    c=labels,
    s=80
)

for i in range(len(noise_levels)):

    plt.text(
        noise_levels[i],
        peak_counts[i],
        regime_names[labels[i]],
        fontsize=8
    )

plt.title(
    "DPI Coherence Regime Classification"
)

plt.xlabel("Noise Strength")

plt.ylabel("Peak Count")

plt.grid(True)

output_path = (
    "outputs/images/"
    "regime_classification.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"Saved regime classification: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE REGIME DATA
# ----------------------------------------

regime_output = []

for i in range(len(noise_levels)):

    regime_output.append({
        "noise_strength": float(
            noise_levels[i]
        ),
        "coherence_width": float(
            coherence_widths[i]
        ),
        "peak_count": int(
            peak_counts[i]
        ),
        "variance": float(
            variance_values[i]
        ),
        "regime": regime_names[
            labels[i]
        ]
    })

with open(
    "outputs/telemetry/regime_map.json",
    "w"
) as f:

    json.dump(
        regime_output,
        f,
        indent=4
    )

print(
    "Saved regime telemetry: "
    "outputs/telemetry/regime_map.json"
)

# ----------------------------------------
# REGIME SUMMARY
# ----------------------------------------

print("\n--- REGIME SUMMARY ---\n")

for regime in regime_names.values():

    count = sum(
        1
        for r in regime_output
        if r["regime"] == regime
    )

    print(f"{regime}: {count}")
