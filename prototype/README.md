# 🧪 Prototype — PottyIQ Prediction Engine

## Overview

This prototype demonstrates a **simplified version of the PottyIQ prediction system**.

It simulates how real-time pet activity events can be processed to:

* infer behavioral patterns
* predict the next likely potty window
* trigger timely alerts for pet owners

This is a **rule-based implementation** used to validate core system assumptions before introducing ML-based models.

---

## 🎯 Purpose

The prototype is designed to:

* Validate core prediction logic using real-world-like signals
* Demonstrate end-to-end flow from event ingestion → prediction → alert
* Provide a foundation for evolving toward ML-based personalization
* Serve as a lightweight proof of feasibility for the larger system design

---

## ⚙️ How It Works

### Input

The system ingests a sequence of timestamped events such as:

* Feeding
* Water intake
* Sleep / wake
* Previous potty events

Sample input is provided in:

👉 `sample_events.json`

---

### Processing Logic

The prototype applies simple behavioral rules:

* **Feed rule** → potty expected within a time window after feeding
* **Water rule** → shorter window after hydration
* **Wake rule** → immediate need after waking
* **Recent potty override** → suppress predictions if a recent potty event exists

---

### Output

The system produces:

* Predicted potty time window
* Alert time (before window starts)
* Rule used for prediction (for explainability)

---

## 📌 Example Output

```text
=== PottyIQ Prototype ===

Input signals:
- Last feeding: 08:30 AM
- Last potty: 07:45 AM

Prediction:
- Rule used: feed-rule
- Next potty window: 09:30 AM – 11:00 AM
- Alert time: 09:20 AM
```

---

## ▶️ How to Run

```bash
python predictor.py
```

---

## 🧠 How This Maps to Full System

| Prototype Component | Production Equivalent                  |
| ------------------- | -------------------------------------- |
| JSON input          | Event stream (Kafka / Kinesis)         |
| Rule engine         | Real-time prediction service           |
| Local execution     | Distributed processing (microservices) |
| Static logic        | ML-driven adaptive models              |

---

## ⚠️ Limitations

This prototype is intentionally simplified:

* Uses rule-based logic (no ML models)
* Processes small, static datasets
* No real-time streaming or distributed execution
* No personalization across multiple pets
* No feedback loop for continuous learning

---

## 🚀 Next Steps

* Introduce ML-based prediction models
* Integrate with streaming pipeline (Kafka/Kinesis)
* Add feedback loop for continuous improvement
* Support personalization per pet profile
* Expand rule engine into hybrid inference system

---

## 📌 Summary

This prototype validates the **core idea behind PottyIQ**:

> Pet behavior signals can be transformed into actionable predictions and alerts.

It serves as a stepping stone toward a **scalable, intelligent, real-time system**.
