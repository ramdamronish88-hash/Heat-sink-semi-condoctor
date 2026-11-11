# Semiconductor Thermal Management: Generative Heat Sinks & Nanocomposites

This repository contains the SolidWorks 3D CAD models, Text-to-CAD generated geometries, and Finite Element Analysis (FEA) thermal/structural simulation data for my semiconductor thermal management research. 

This project explores how varying heat sink geometries and advanced composite materials can reduce Junction-to-Ambient thermal resistance ($\theta_{JA}$) and mitigate thermal expansion (CTE) stress in high-power microchip packages.

## Project Overview

Modern AI and 3D-stacked microchips generate massive localized heat fluxes (often exceeding $500\text{ W/cm}^2$). Traditional extruded aluminum heat sinks struggle to dissipate this heat efficiently, and the severe Coefficient of Thermal Expansion (CTE) mismatch between the silicon die and standard metal coolers causes structural failure (cracking or delamination) over time.

This research focuses on two optimization paths:
1. **Geometry:** Utilizing generative design and topology optimization to create variable-density microchannels that outperform standard straight fins.
2. **Material Science:** Simulating the structural benefits of metal-matrix nanocomposites (e.g., Cu-Diamond) that match the thermal expansion of silicon while delivering superior thermal conductivity.

## Repository Contents

*   `/CAD_Models` 
    *   `Baseline_StraightFin.SLDPRT`: Standard extruded fin geometry.
    *   `Staggered_PinFin.SLDPRT`: Pin-fin array geometry.
    *   `Generative_Microchannel.STEP`: Organic/variable-density fin design generated via the Text-to-CAD extension.
*   `/FEA_Simulations`
    *   `Thermal_Study_Results/`: Temperature contour plots showing peak junction temperatures ($T_{max}$).
    *   `Static_Stress_Results/`: Von Mises stress plots detailing structural warping caused by CTE mismatch at the die-TIM interface.
*   `/Research_Drafts`
    *   `Thermal_Resistance_Calculations.xlsx`: Analytical hand calculations for 1D thermal resistance and spreading resistance.
    *   `Draft_Paper.pdf`: Work-in-progress preprint comparing the thermal and structural performance of the three geometries and simulated composite materials.

## Methodology (SolidWorks Simulation)

The simulations within this repository utilize a standardized 3-layer semiconductor stack:
1.  **Silicon Die:** $15\text{ mm} \times 15\text{ mm} \times 0.7\text{ mm}$ ($150\text{ W}$ heat load applied to the bottom face).
2.  **Thermal Interface Material (TIM):** $0.05\text{ mm}$ layer testing standard paste vs. high-conductivity sintered silver/gold-tin eutectic solder.
3.  **Heat Sink Baseplate:** $50\text{ mm} \times 50\text{ mm}$ footprint with forced convection applied to the fins.

A steady-state **Thermal Study** computes the temperature gradients, which are then linked into a **Static Structural Study** to measure thermal expansion stress across the assembly.
