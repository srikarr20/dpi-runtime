import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# DETECTOR PLANE POSITIONS
# ----------------------------------------

x = np.linspace(-10, 10, 2000)

# ----------------------------------------
# WAVE PARAMETERS
# ----------------------------------------

wavelength = 1.0

k = 2 * np.pi / wavelength

# ----------------------------------------
# DOUBLE SLIT GEOMETRY
# ----------------------------------------

d = 2.0

slit1 = -d / 2
slit2 = d / 2

# ----------------------------------------
# DETECTOR PLANE DISTANCE
# ----------------------------------------

L = 10

# ----------------------------------------
# DISTANCES TO DETECTOR PLANE
# ----------------------------------------

r1 = np.sqrt((x - slit1)**2 + L**2)
r2 = np.sqrt((x - slit2)**2 + L**2)

# ----------------------------------------
# PROPAGATED WAVES
# ----------------------------------------

wave1 = np.exp(1j * k * r1) / r1
wave2 = np.exp(1j * k * r2) / r2

# ----------------------------------------
# TOTAL FIELD
# ----------------------------------------

field = wave1 + wave2

# ----------------------------------------
# DETECTOR-PLANE INTENSITY
# ----------------------------------------

intensity = np.abs(field)**2

# Normalize intensity
intensity /= np.max(intensity)

# ----------------------------------------
# OBSERVABILITY METRICS
# ----------------------------------------

peak_intensity = np.max(intensity)

peak_count = np.sum(
    (intensity[1:-1] > intensity[:-2]) &
    (intensity[1:-1] > intensity[2:]) &
    (intensity[1:-1] > 0.1)
)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    intensity,
    label="Double-Slit Observability"
)

plt.title("Double-Slit Detector Plane")

plt.xlabel("Detector Position")

plt.ylabel("Normalized Intensity")

plt.grid(True)

# ----------------------------------------
# OVERLAY LABELS
# ----------------------------------------

metrics_text = (
    f"Peak Intensity: {peak_intensity:.2f}\n"
    f"Peak Count: {peak_count}\n"
    f"Slit Separation: {d}\n"
    f"Detector Distance: {L}"
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
# SAVE OUTPUT
# ----------------------------------------

output_path = "outputs/images/double_slit_detector_plane.png"

plt.savefig(output_path)

print(f"Detector-plane image saved to: {output_path}")

plt.close()
