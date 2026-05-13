import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

# ----------------------------------------
# LOAD CALIBRATION RESULTS
# ----------------------------------------

with open(
    "outputs/telemetry/calibration_results.json",
    "r"
) as f:

    calibration = json.load(f)

# ----------------------------------------
# BUILD OBSERVABILITY VECTORS
# ----------------------------------------

states = []
vectors = []

for state_name, metrics in calibration.items():

    vector = [

        metrics["peak_intensity"],
        metrics["mean_intensity"],
        metrics["intensity_variance"],
        metrics["center_of_mass"],
        metrics["coherence_width"],
        metrics["peak_count"]

    ]

    states.append(state_name)

    vectors.append(vector)

vectors = np.array(vectors)

# ----------------------------------------
# PCA PROJECTION
# ----------------------------------------

pca = PCA(n_components=2)

projection = pca.fit_transform(vectors)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(10, 8))

for i, state in enumerate(states):

    x = projection[i, 0]
    y = projection[i, 1]

    plt.scatter(x, y, s=200)

    plt.text(
        x + 0.1,
        y + 0.1,
        state,
        fontsize=12
    )

# ----------------------------------------
# LABELS
# ----------------------------------------

plt.title(
    "DPI Observability Trajectory Geometry"
)

plt.xlabel("Principal Component 1")

plt.ylabel("Principal Component 2")

plt.grid(True)

# ----------------------------------------
# SAVE OUTPUT
# ----------------------------------------

output_path = (
    "outputs/images/trajectory_geometry.png"
)

plt.savefig(output_path)

print(
    f"Saved trajectory geometry: {output_path}"
)

plt.close()
