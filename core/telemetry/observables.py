import numpy as np

def extract_observables(detector_x, intensity):

    observables = {}

    # ----------------------------------------
    # PEAK INTENSITY
    # ----------------------------------------

    observables["peak_intensity"] = float(np.max(intensity))

    # ----------------------------------------
    # MEAN INTENSITY
    # ----------------------------------------

    observables["mean_intensity"] = float(np.mean(intensity))

    # ----------------------------------------
    # INTENSITY VARIANCE
    # ----------------------------------------

    observables["intensity_variance"] = float(np.var(intensity))

    # ----------------------------------------
    # DETECTOR CENTER OF MASS
    # ----------------------------------------

    center_of_mass = np.sum(detector_x * intensity) / np.sum(intensity)

    observables["center_of_mass"] = float(center_of_mass)

    # ----------------------------------------
    # COHERENCE WIDTH
    # ----------------------------------------

    width = np.sqrt(
        np.sum((detector_x - center_of_mass)**2 * intensity)
        / np.sum(intensity)
    )

    observables["coherence_width"] = float(width)

    # ----------------------------------------
    # PEAK COUNT
    # ----------------------------------------

    threshold = 0.1

    peaks = (
        (intensity[1:-1] > intensity[:-2]) &
        (intensity[1:-1] > intensity[2:]) &
        (intensity[1:-1] > threshold)
    )

    observables["peak_count"] = int(np.sum(peaks))

    return observables
