
# Panic Simulation

## Introduction
Ensuring the safe evacuation of individuals during emergencies, like fires, is crucial for public safety. Agent-Based Models (ABMs) provide a powerful tool for simulating complex systems by representing individual decision-making units, or agents, and their interactions within dynamic environments. In this simulation, we focus on modeling panic-induced evacuations from a building under fire conditions.

## Simulation Overview
Agents: The simulation comprises "Worker" agents representing individuals evacuating and "Fire" agents simulating the spreading fire hazard.
Agent Behavior: Worker agents dynamically assess their surroundings, adjust their panic level, and make decisions regarding movement and escape routes based on factors like fire presence and nearby panic states.
Fire Spread: The fire hazard expands over time, potentially blocking escape routes and endangering worker agents.
Parameter Control: Various parameters, including building layout, panic behaviors, and fire properties, can be adjusted to explore different evacuation scenarios.
Data Visualization: Simulation results, such as the number of escaped workers, remaining panicked workers, and casualties, are visualized through graphs to analyze evacuation effectiveness.

## Requirement
Python libraries:
- `tkinter`
- `matplotlib`
- `seaborn`

## Getting Started
- Ensure that python and the relevant above libraries are installed
- Clone and run the following commands:

```
git clone https://gitlab.computing.dcu.ie/bolgee25/ca4021_agent_based_model_assignment
cd ca4021_agent_based_model_assignment
python abm_evacuation_simulation.py
```
- Use the provided GUI interface to adjust parameters such as cell size, door width, panic thresholds, and fire spread characteristics.
- Click the "Submit" button to apply the configured settings.
- Choose between continuous or step-by-step simulation execution using the provided buttons.
- Analyze plotted results to understand the effectiveness of evacuation strategies under different conditions.

[Pycxsimulator](https://github.com/hsayama/PyCX) does not seem to work on linux and as a result we used tkinter as a GUI instead.

![Example Simulation](/Images/Experiment_5.png)