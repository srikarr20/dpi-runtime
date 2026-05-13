import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

from core.telemetry.observables import extract_observables

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(-20, 20, 3000)

# ----------------------------------------
# TRAJECTORY STORAGE
# ----------------------------------------

vectors = []

labels = []

# ----------------------------------------
# EVOLUTION LOOP
# ----------------------------------------

steps = 25

for step in range(steps):

    print(f"Processing step: {step}")

    # ----------------------------------------
    # EVOLVING PARAMETERS
    # ----------------------------------------

    noise_strength = step * 0.025

    modulation_strength = max(
        1.0 - (step * 0.03),
        0.05
    )

    # ----------------------------------------
    # SOURCE FIELD
    # ----------------------------------------

    source_field = np.exp(
        -(detector_x)**2 / 20
    )

    # ----------------------------------------
    # COHERENCE MODULATION
    # ----------------------------------------

    coherence_pattern = (
        np.cos(detector_x * 2)
        * modulation_strength
    )

    # ----------------------------------------
    # NOISE
    # ----------------------------------------

    noise = np.random.normal(
        0,
        noise_strength,
        size=len(detector_x)
    )

    # ----------------------------------------
    # OBSERVABILITY FIELD
    # ----------------------------------------

    field = (
        source_field
        * coherence_pattern
    )

    field += noise

    # ----------------------------------------
    # DETECTOR INTENSITY
    # ----------------------------------------

    intensity = np.abs(field)**2

    intensity /= np.max(intensity)

    # ----------------------------------------
    # OBSERVABLES
    # ----------------------------------------

    observables = extract_observables(
        detector_x,
        intensity
    )

    vector = [

        observables["peak_intensity"],
        observables["mean_intensity"],
        observables["intensity_variance"],
        observables["center_of_mass"],
        observables["coherence_width"],
        observables["peak_count"]

    ]

    vectors.append(vector)

    labels.append(step)

# ----------------------------------------
# PCA PROJECTION
# ----------------------------------------

vectors = np.array(vectors)

pca = PCA(n_components=2)

projection = pca.fit_transform(vectors)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(12, 8))

x = projection[:, 0]
y = projection[:, 1]

# ----------------------------------------
# TRAJECTORY LINE
# ----------------------------------------

plt.plot(
    x,
    y,
    alpha=0.7
)

# ----------------------------------------
# POINTS
# ----------------------------------------

plt.scatter(
    x,
    y,
    s=120
)

# ----------------------------------------
# STEP LABELS
# ----------------------------------------

for i in range(len(labels)):

    plt.text(
        x[i] + 1,
        y[i] + 1,
        str(labels[i]),
        fontsize=9
    )

# ----------------------------------------
# LABELS
# ----------------------------------------

plt.title(
    "DPI Trajectory Evolution"
)

plt.xlabel(
    "Principal Component 1"
)

plt.ylabel(
    "Principal Component 2"
)

plt.grid(True)

# ----------------------------------------
# SAVE OUTPUT
# ----------------------------------------

output_path = (
    "outputs/images/trajectory_evolution.png"
)

plt.savefig(output_path)

print(
    f"Saved trajectory evolution: {output_path}"
)

plt.close()

# ----------------------------------------
# SAVE RAW TRAJECTORY
# ----------------------------------------

with open(
    "outputs/trajectories/trajectory_vectors.json",
    "w"
) as f:

    json.dump(
        vectors.tolist(),
        f,
        indent=4
    )

print(
    "Saved trajectory vectors."
)
