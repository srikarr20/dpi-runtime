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
# STORAGE
# ----------------------------------------

vectors = []

# ----------------------------------------
# EVOLUTION LOOP
# ----------------------------------------

steps = 25

for step in range(steps):

    noise_strength = step * 0.025

    modulation_strength = max(
        1.0 - (step * 0.03),
        0.05
    )

    source_field = np.exp(
        -(detector_x)**2 / 20
    )

    coherence_pattern = (
        np.cos(detector_x * 2)
        * modulation_strength
    )

    noise = np.random.normal(
        0,
        noise_strength,
        size=len(detector_x)
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

    vector = [

        observables["peak_intensity"],
        observables["mean_intensity"],
        observables["intensity_variance"],
        observables["center_of_mass"],
        observables["coherence_width"],
        observables["peak_count"]

    ]

    vectors.append(vector)

# ----------------------------------------
# PCA PROJECTION
# ----------------------------------------

vectors = np.array(vectors)

pca = PCA(n_components=2)

projection = pca.fit_transform(vectors)

x = projection[:, 0]
y = projection[:, 1]

# ----------------------------------------
# FORECAST VECTOR
# ----------------------------------------

last_dx = x[-1] - x[-2]
last_dy = y[-1] - y[-2]

forecast_steps = 5

forecast_x = []
forecast_y = []

current_x = x[-1]
current_y = y[-1]

for i in range(forecast_steps):

    current_x += last_dx
    current_y += last_dy

    forecast_x.append(current_x)
    forecast_y.append(current_y)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(12, 8))

# ----------------------------------------
# ORIGINAL TRAJECTORY
# ----------------------------------------

plt.plot(
    x,
    y,
    marker='o',
    label="Observed Trajectory"
)

# ----------------------------------------
# FORECAST TRAJECTORY
# ----------------------------------------

plt.plot(
    forecast_x,
    forecast_y,
    linestyle='--',
    marker='x',
    label="Forecast Trajectory"
)

# ----------------------------------------
# LABELS
# ----------------------------------------

plt.title(
    "DPI Trajectory Forecast"
)

plt.xlabel(
    "Principal Component 1"
)

plt.ylabel(
    "Principal Component 2"
)

plt.grid(True)

plt.legend()

# ----------------------------------------
# SAVE
# ----------------------------------------

output_path = (
    "outputs/images/trajectory_forecast.png"
)

plt.savefig(output_path)

print(
    f"Saved forecast: {output_path}"
)

plt.close()

# ----------------------------------------
# SAVE FORECAST DATA
# ----------------------------------------

forecast_data = {

    "forecast_x": forecast_x,
    "forecast_y": forecast_y

}

with open(
    "outputs/trajectories/trajectory_forecast.json",
    "w"
) as f:

    json.dump(
        forecast_data,
        f,
        indent=4
    )

print(
    "Saved forecast metadata."
)
