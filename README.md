# Bronze-Age-Script-Algorithmic-alignment-v43-0
Topological alignment algorithms for morphological analysis.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19347889.svg)](https://doi.org/10.5281/zenodo.19347889)

##Quick Start (Python)
To reproduce the automated matching between the Shang (商) character and Ki-En-Gi Ki-Uri-Ke₄:

Install dependencies: pip install opencv-python numpy matplotlib

Run the matching script: python Collison_v43_single_target.py


## Overview
This repository contains the computational framework and quantitative methodology for **v43.0 Quantitative Graphemics**, an algorithmic tool designed to measure the topological isomorphism between isolated Early Bronze Age administrative logograms. 

By shifting the analytical paradigm from subjective visual inspection to rigid computational morphometrics, this framework calculates the exact statistical probability of structural alignment across divergent writing systems.

## Core Methodology
The v43.0 algorithm evaluates script homology through two primary metrics, rigorously excluding stochastic visual noise:
* **Cover% (Spatial Pixel Coverage):** Measures the absolute coordinate overlap of standardized strokes within a normalized 2D matrix.
* **Topo% (Topological Node Mapping):** Evaluates the structural connectivity and hierarchical relationship of internal grapheme components.

### Statistical Baseline and Noise Calibration
To ensure maximum analytical rigor, the system was calibrated against a randomized control population of unstructured geometric marks (N=100).
* **Stochastic Noise Floor:** Empirical testing establishes that random morphological convergence peaks at **< 56%**.
* **High-Confidence Threshold:** Alignment scores exceeding **62%** are mathematically classified as non-random structural homologies, representing intentional systemic transmission rather than coincidental evolution.

## Purpose of this Repository
This repository is maintained strictly for **peer-review transparency and reproducibility**. It provides the pseudocode, scoring matrices, and ablation study parameters referenced in upcoming academic publications. 


## Data Availability
The full dataset, including high-resolution vector alignments and the full N=100 control group matrices, is concurrently archived on Zenodo (DOI pending publication) for permanent open-access validation.

---
*Maintainer: Tony (Shaofeng) Luan*
*Focus: Computational Morphometrics & Early Administrative Topologies*


