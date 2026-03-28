# MLOps Batch Processing Task

## Overview

This project ensures deterministic results using a fixed seed and config-driven execution.
This project implements a minimal MLOps-style batch job in Python that demonstrates:

- Reproducibility using config and seed
- Observability via logs and metrics
- Deployment readiness using Docker (optional)

---

## Project Structure

mlops-task/
│── run.py
│── config.yaml
│── data.csv
│── requirements.txt
│── Dockerfile
│── README.md
│── metrics.json
│── run.log

---

## Local Execution (Recommended)

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```
