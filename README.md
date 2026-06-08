# ⚡ Fastest FLASH MRI with Extended Trapezoid Gradient

**Author:** Mohit Makvana  
**Institution:** Technische Fakultät  
**Date:** August 2024

---

## Overview

This project presents a high-speed implementation of a **2D FLASH (Fast Low Angle Shot Imaging)** MRI sequence developed using Pulseq. The primary objective is to reduce total acquisition time by redesigning the frequency-encoding gradient waveform.

Instead of using conventional trapezoidal gradients with idle switching periods, this implementation introduces an **Extended Trapezoid Gradient** along the readout axis. The modified waveform minimises gradient dead-time and improves overall sequence efficiency while remaining within scanner hardware constraints.

The result is a significantly faster FLASH acquisition without sacrificing image quality or violating gradient and slew-rate limits.

---

## Key Features

- High-speed 2D FLASH sequence
- Extended trapezoid frequency-encoding gradient
- Reduced gradient switching dead-time
- RF spoiling implementation
- Hardware-constrained design
- Pulseq compatible
- Optimised acquisition time
- Suitable for rapid dynamic imaging applications

---

# Performance Improvement

| Sequence Type | Acquisition Time |
|--------------|-----------------|
| Conventional FLASH | ~0.80 s |
| Proposed Fast FLASH | ~0.175 s |

### Speed Gain

- Approximately **78% reduction** in acquisition time
- More efficient gradient utilisation
- Improved temporal resolution

---

## Sequence Architecture

```text
RF Excitation
      │
      ▼
Slice Selection Gradient
      │
      ▼
Phase Encoding Gradient
      │
      ▼
Extended Trapezoid Readout Gradient
      │
      ▼
ADC Sampling
      │
      ▼
RF Spoiling Update
      │
      ▼
Next TR
```

---

## Extended Trapezoid Gradient Concept

Traditional FLASH sequences contain short inactive periods between gradient transitions.

### Conventional Readout

```text
      /¯¯¯¯¯\
_____/       \_____
```

### Extended Trapezoid Readout

```text
      /¯¯¯¯¯¯¯¯¯¯¯\
_____/             \_____
```

Benefits:

- Reduced dead-time
- Improved gradient duty cycle
- Faster k-space traversal
- Shorter repetition period

---

## FLASH Sequence Fundamentals

FLASH is a Gradient Recalled Echo (GRE) sequence that combines:

- Low flip-angle RF excitations
- Gradient echo formation
- RF spoiling
- Short TR and TE

### Advantages

✅ Fast acquisition

✅ Low SAR

✅ Flexible image contrast

✅ Excellent for dynamic studies

### Limitations

⚠ Lower SNR compared with spin-echo methods

⚠ Sensitive to magnetic field inhomogeneity

⚠ Susceptibility-related artifacts

---

# Tissue Contrast Configurations

## Proton Density Weighted

| Parameter | Setting |
|------------|----------|
| Flip Angle | Small |
| TR | Long |
| TE | Short |

---

## T1 Weighted

| Parameter | Setting |
|------------|----------|
| Flip Angle | Large (~70°) |
| TR | Short |
| TE | Short |

---

## T2* Weighted

| Parameter | Setting |
|------------|----------|
| Flip Angle | Small |
| TR | Longer |
| TE | Long |

---

# Clinical Applications

### Magnetic Resonance Angiography (MRA)

- Non-invasive vascular imaging
- Arterial visualisation
- Venous assessment

### Dynamic Contrast Enhanced MRI

- Contrast uptake monitoring
- Tumour characterisation
- Pharmacokinetic analysis

### Perfusion Imaging

- Tissue blood flow evaluation
- Cerebral perfusion studies
- Oncology applications

### Abdominal MRI

- Rapid breath-hold imaging
- Motion reduction
- Improved patient comfort

---

# Technical Specifications

| Parameter | Value |
|------------|---------|
| Field of View | 220 mm × 220 mm |
| Slice Thickness | 8.0 mm |
| Acquisition Matrix | 32 × 32 |
| Reconstructed Matrix | 64 × 64 |
| Readout Samples | 64 |
| Phase Encoding Steps | 64 |
| Flip Angle | 5° |
| RF Spoiling Increment | 117° |
| Maximum Gradient | 28 mT/m |
| Maximum Slew Rate | 150 T/m/s |

---

# Repository Structure

```text
fast-flash-mri/
│
├── README.md
├── seq/
│   ├── fast_flash.seq
│   └── conventional_flash.seq
│
├── scripts/
│   ├── create_sequence.py
│   ├── reconstruction.py
│   └── analysis.py
│
├── images/
│   ├── adc_signals_comparison.png
│   ├── gradient_waveforms.png
│   ├── sequence_timeline.png
│   └── reconstructed_image.png
│
└── docs/
    └── project_report.pdf
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/fast-flash-mri.git
cd fast-flash-mri
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage

Generate the sequence:

```bash
python create_sequence.py
```

Run reconstruction:

```bash
python reconstruction.py
```

Analyse timing performance:

```bash
python analysis.py
```

---

# Example Results

## Gradient Waveforms

- Slice-selection gradient
- Phase-encoding gradient
- Extended trapezoid readout gradient

## ADC Timing

Comparison of:

- Standard FLASH acquisition
- Optimised FLASH acquisition

## Image Reconstruction

- k-space generation
- Fourier reconstruction
- Image quality evaluation

---

# Future Improvements

- Parallel imaging support (GRAPPA/SENSE)
- Compressed sensing integration
- Multi-slice FLASH
- 3D FLASH implementation
- GPU-accelerated reconstruction
- Real-time imaging framework

---

# Research Contribution

This work demonstrates that intelligent gradient waveform engineering can dramatically reduce acquisition time in FLASH imaging. The proposed extended trapezoid readout strategy improves temporal efficiency while preserving compatibility with standard MRI hardware constraints.

---

# Acknowledgements

This project was developed as part of MRI sequence design and optimisation research at Technische Fakultät.

Special thanks to the Pulseq development community for providing an open framework for MRI sequence prototyping.

---

# License

This project is released under the MIT License.

```text
MIT License

Copyright (c) 2024 Mohit Makvana

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files.
```

---

