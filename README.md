# Post Office Queue Simulation

This project is a simulation developed for a laboratory assignment in the Simulation course.

## Description

The simulation models a post office in Córdoba with two service types:

- **Package Shipping**: Served by two employees (10 clients/hour each).
- **Claims and Returns**: Served by one employee (7 clients/hour).

Clients arrive following exponential distributions:
- 25 clients/hour for Package Shipping.
- 15 clients/hour for Claims and Returns.

Each server can be an **expert** or an **apprentice**, which affects service speed (configurable). A continuous-time component is included using the equation:

```
dR/dt = C + 0.2 * T + t²
```

Where:
- `C` is the number of people in the queue,
- `T` is the total service time,
- `t` is the simulation time.

## Features

- Configurable parameters (arrival/service rates, server types).
- Run N simulation lines (e.g. 1000, 10,000, etc.).
- View any 300-line segment from the simulation.
- Display state headers and final state.
- Continuous model calculation integrated per simulation row.
- Outputs include average waiting time and server utilization.

## Objectives

- Measure wait times and occupation for each service.
- Analyze the impact of server absences.
- Apply a continuous model within a discrete simulation.

---

**Note**: Developed for Lab Work #5 - Simulation Course (2025).
