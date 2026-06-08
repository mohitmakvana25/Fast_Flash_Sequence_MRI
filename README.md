````markdown
# Fastest FLASH MRI with Extended Trapezoid Gradient

**Developed by Mohit Makvana**  
*Faculty of Engineering (Technische Fakultät)*  
*August 2024*

This project presents a highly optimised implementation of a **2D FLASH (Fast Low Angle Shot Imaging)** MRI sequence. By introducing an **Extended Trapezoid Gradient** along the frequency-encoding (Gx) axis, the sequence minimizes hardware dead-time between gradient transitions and significantly reduces total acquisition time.

---

# 🚀 Performance Optimisation

The conventional FLASH sequence contains inactive intervals between gradient switching events. By redesigning the readout gradient as a continuous extended trapezoid waveform, these delays are largely eliminated.

## Acquisition Time Comparison

| Sequence | Acquisition Time |
|-----------|----------------|
| Standard FLASH | ~0.80 s |
| Optimized FLASH | ~0.175 s |

This represents a reduction of more than **75% in total acquisition time** while maintaining image quality and sequence stability.

<p align="center">
  <img src="images/adc_signals_comparison.png" alt="ADC Signal Comparison" width="800">
</p>

---

# 📖 Sequence Overview

FLASH (Fast Low Angle Shot Imaging) is a Gradient Recalled Echo (GRE) sequence that combines:

- Low flip-angle RF excitation
- Gradient echo signal formation
- RF spoiling for steady-state stabilisation
- Rapid image acquisition

## Key Characteristics

| Property | Description |
|----------|-------------|
| Acquisition Speed | Faster than RARE, slower than EPI |
| Spatial Resolution | Higher than EPI-based methods |
| SAR | Low |
| SNR | Moderate |
| Clinical Utility | Dynamic and angiographic imaging |

---

# 🎯 Contrast Weighting Options

By adjusting sequence parameters, different tissue contrasts can be achieved.

## Proton Density (PD) Weighting

- Small flip angle
- Long TR
- Short TE

## T1 Weighting

- Large flip angle (~70°)
- Short TR (< 50 ms)
- Short TE

## T2* Weighting

- Small flip angle
- Long TR (~100 ms)
- Long TE (~20 ms)

---

# 🏥 Clinical Applications

### Magnetic Resonance Angiography (MRA)

Non-invasive visualization of blood vessels.

### Vascular Imaging

Suitable for imaging:

- Cerebral vasculature
- Neck vessels
- Peripheral arteries

### Dynamic Contrast-Enhanced MRI (DCE-MRI)

Used for monitoring contrast-agent uptake and washout over time.

### Perfusion Assessment

Evaluation of tissue perfusion before, during, and after contrast administration.

### Abdominal Imaging

Fast acquisition reduces motion artifacts and improves imaging efficiency in abdominal examinations.

---

# ⚙️ Technical Specifications

| Parameter | Value |
|------------|------------|
| Field of View (FOV) | 220 mm × 220 mm |
| Slice Thickness | 8.0 mm |
| Matrix Size | 32 × 32 |
| Reconstructed Resolution | 64 × 64 |
| Readout Samples | 64 |
| Phase-Encoding Steps | 64 |
| Flip Angle | 5° |
| RF Spoiling Increment | 117° |
| Maximum Gradient Strength | 28 mT/m |
| Maximum Slew Rate | 150 T/m/s |

---

# 🔬 Extended Trapezoid Gradient Concept

The key innovation of this work is the replacement of conventional trapezoidal readout gradients with a continuous extended trapezoid design.

## Advantages

- Reduced gradient switching overhead
- Elimination of unnecessary dead-time
- Improved acquisition efficiency
- Faster k-space traversal
- Reduced overall scan duration

The Optimisation enables significantly faster imaging while remaining within scanner hardware limits.

---

# 📊 Results

The optimised implementation demonstrates:

- More than **75% reduction** in acquisition time
- Stable gradient behavior
- Hardware-compliant operation
- Efficient k-space coverage
- Preservation of FLASH image characteristics

---

# 📁 Project Structure

```text
fast-flash-mri/
│
├── images/
│   └── adc_signals_comparison.png
│
├── seq/
│   ├── flash_extended_trapezoid.py
│   └── helper_functions.py
│
├── documentation/
│
├── README.md
│
└── results/
```

---

# 💻 Getting Started

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fast-flash-mri.git
cd fast-flash-mri
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Sequence

```bash
python flash_extended_trapezoid.py
```

---

# 🎓 Research Contributions

This work demonstrates that substantial reductions in FLASH acquisition time can be achieved through gradient waveform Optimisation without exceeding scanner hardware constraints.

### Contributions

- Design of an Extended Trapezoid Readout Gradient
- Elimination of Gradient Dead-Time
- Hardware-Constrained Optimisation
- High-Speed FLASH MRI Implementation
- Experimental Validation of Acquisition-Time Reduction

---

# 📌 Highlights

✅ FLASH MRI Sequence Implementation  
✅ Extended Trapezoid Gradient Design  
✅ RF Spoiling Support  
✅ Hardware-Constrained Optimisation  
✅ GRE-Based Imaging  
✅ >75% Reduction in Acquisition Time  
✅ Research-Oriented Open Implementation

---

# 📄 License

This project is intended for academic and research purposes.

If this work contributes to your research, please consider citing the repository.

---

# 👨‍💻 Author

**Mohit Makvana**  
M.Sc. Computational Engineering  
Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU)

Research Interests:

- Magnetic Resonance Imaging (MRI)
- Pulse Sequence Development
- Fast Imaging Techniques
- Medical Image Reconstruction
- Deep Learning for Medical Imaging
````
