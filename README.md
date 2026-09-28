# Quantitative Morphological Isomorphism & Spatiotemporal Alignment Pipeline (v43.0)

[![Dataset & Code DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19347889.svg)](https://doi.org/10.5281/zenodo.19347889)
[![Paper 1 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23005821.svg)](https://doi.org/10.5281/zenodo.23005821)
[![Paper 2 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23006028.svg)](https://doi.org/10.5281/zenodo.23006028)

## Overview

This repository contains the computational framework and quantitative methodology for evaluating the potential structural and chronological correlations between Early Bronze Age administrative systems (specifically the late Uruk/Ur III periods and the pre-dynastic Shang sequence).

By shifting the analytical paradigm from subjective visual inspection to rigid computational morphometrics and probability modeling, this framework calculates the statistical significance of both graphemic structural alignments and multi-generational historical successions.

## Core Methodology

### 1. v43.0 Quantitative Graphemics
Evaluates script homology through two primary metrics, aiming to isolate structural patterns from stochastic visual noise:
* **Cover% (Spatial Pixel Coverage):** Measures the absolute coordinate overlap of standardized strokes within a normalized 2D matrix.
* **Topo% (Topological Node Mapping):** Evaluates the structural connectivity and hierarchical relationship of internal grapheme components.
* **Noise Calibration:** Empirical testing against a randomized control population (N=100) suggests that random morphological convergence typically peaks at < 56%. Alignments exceeding the 62% threshold are analyzed as statistically notable non-random homologies.

### 2. Log-Confidence Spatiotemporal Model
Evaluates the sequential probability of the 5-generation progenitor lineage (e.g., from Xie/Ur-gigir to Bao Yi/Shulgi) using a multi-dimensional matrix:
* **NS** (Iconographic-Phonological Alignment)
* **TS** (Sovereign Legitimacy Mapping)
* **DS** (Deed-Based Correlation)

## Quick Start (Python)

**Module A: Topological Alignment Matching**  
To explore the automated graphemic matching between the Shang (商) character and the Sumerian formula `Ki-En-Gi Ki-Uri-Ke₄`:
```bash
python Collison_v43_single_target.py
