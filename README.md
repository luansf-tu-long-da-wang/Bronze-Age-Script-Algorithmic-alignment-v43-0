# Quantitative Morphological Isomorphism & Spatiotemporal Alignment Pipeline

## Overview
This repository contains the computational framework and quantitative methodology for evaluating the potential structural and chronological correlations between Early Bronze Age administrative systems (specifically the late Uruk/Ur III periods and the pre-dynastic Shang sequence). 

By shifting the analytical paradigm from subjective visual inspection to rigid computational morphometrics and probability modeling, this framework calculates the statistical significance of both **graphemic structural alignments** and **multi-generational historical successions**.

## Core Methodology

### 1. v43.0 Quantitative Graphemics
Evaluates script homology through two primary metrics, aiming to isolate structural patterns from stochastic visual noise:
* **Cover% (Spatial Pixel Coverage):** Measures the absolute coordinate overlap of standardized strokes within a normalized 2D matrix.
* **Topo% (Topological Node Mapping):** Evaluates the structural connectivity and hierarchical relationship of internal grapheme components.
* **Noise Calibration:** Empirical testing against a randomized control population (N=100) suggests that random morphological convergence typically peaks at `< 56%`. Alignments exceeding the **62% threshold** are analyzed as statistically notable non-random homologies.

### 2. Log-Confidence Spatiotemporal Model
Evaluates the sequential probability of the 5-generation progenitor lineage (e.g., from Xie/Ur-gigir to Bao Yi/Shulgi) using a multi-dimensional matrix:
* **NS (Iconographic-Phonological Alignment)**
* **TS (Sovereign Legitimacy Mapping)**
* **DS (Deed-Based Correlation)**


## Quick Start (Python)

Module A: Topological Alignment Matching
To explore the automated graphemic matching between the Shang (商) character and the Sumerian formula Ki-En-Gi Ki-Uri-Ke₄:

Bash
python Collison_v43_single_target.py

Module B: 5-King Spatiotemporal Matrix (Log-Confidence)
To evaluate the historical succession probability multiplier, ensure your S1 to S5 .csv datasets are placed in the Sumerian_Shang_King_Match directory and run the alignment script:

Bash
python Spatiotemporal_Alignment_Kings.py

### Dependencies
```bash
pip install opencv-python numpy matplotlib pandas

##Purpose of this Repository
This repository is maintained strictly for peer-review transparency and computational reproducibility. It provides the executable algorithms, scoring matrices, and ablation study parameters referenced in accompanying quantitative research.

##Data Availability
The full dataset, including high-resolution vector alignments, the N=100 control group matrices, and the complete S1-S5 historical matrix, is archived on Zenodo (DOI: https://doi.org/10.5281/zenodo.19347889) for permanent open-access validation.
