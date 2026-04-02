# 🏗️ Architecture

## Overview

PottyIQ is designed as a **real-time, event-driven system** that processes pet activity signals to generate timely and accurate potty predictions.

The architecture separates ingestion, processing, storage, and notification into independent components to enable **scalability, resilience, and flexibility**.

---

## 🔄 End-to-End Flow

1. Pet activity events (feeding, water intake, sleep, walks, potty) are captured via mobile app or IoT devices
2. Events are ingested through APIs and validated
3. Events are published to a streaming system for decoupled processing
4. Prediction engine consumes events and evaluates recent + historical patterns
5. System computes the next probable potty window
6. Notification service sends alerts to users
7. Historical data is stored and used for analytics and ML model training

---

## 🧩 Core Components

### 1. Client Layer

* Mobile applications and IoT devices
* Capture pet activity signals in real time
* Responsible for event generation

---

### 2. API & Ingestion Layer

* API Gateway + ingestion service
* Validates incoming events
* Ensures schema consistency and authentication
* Pushes events into the streaming system

---

### 3. Event Streaming Layer

* Kafka / Kinesis
* Decouples producers from consumers
* Enables:

  * asynchronous processing
  * backpressure handling
  * event replay for recovery

---

### 4. Storage Layer

#### Hot Storage (Redis)

* Stores recent activity data
* Enables low-latency access for prediction engine

#### Durable Storage (DynamoDB / S3)

* Stores historical events
* Supports analytics and long-term learning

---

### 5. Prediction Engine

* Core decision-making component
* Processes both real-time and historical signals
* Supports:

  * rule-based logic (initial phase)
  * ML-based models (future phase)

Responsibilities:

* Maintain recent state per pet
* Evaluate behavioral patterns
* Compute next potty window

---

### 6. Notification Service

* Sends alerts via push, SMS, or email
* Operates asynchronously
* Handles retries and delivery guarantees

---

### 7. Analytics & ML Pipeline

* Processes historical data in batch
* Generates insights and trains models
* Feeds updated models back into prediction engine

---

## 📈 Scalability Design

* Partitioning by **petId** ensures even load distribution
* Stateless services allow horizontal scaling
* Streaming system handles spikes and backpressure
* Cache reduces repeated database reads

Designed to support:

* ~1M pets
* ~10–20M events/day
* ~1K events/sec peak

---

## ⚖️ Key Design Decisions

### Event-Driven Architecture

* Enables loose coupling between components
* Improves scalability and resilience

---

### Separation of Hot vs Cold Data

* Redis for low-latency access
* DynamoDB/S3 for durability

---

### Hybrid Processing Model

* Real-time for user-facing predictions
* Batch for analytics and ML training

---

## 🔁 Data Flow Considerations

* Events are processed asynchronously to reduce latency impact on ingestion
* System supports replay of events in case of failures
* Idempotent processing ensures duplicate events do not affect predictions

---

## ⚠️ Failure Handling

* Event stream acts as a durable buffer
* Consumers can reprocess events if failures occur
* Notification retries handled independently
* Fallback to last known patterns if prediction fails

---

## ⏱️ Latency Goals

* Event ingestion: < 50 ms
* Prediction: < 100 ms
* End-to-end alerting: < 1 second

---

## 🔒 Data & Privacy Considerations

* Minimal personally identifiable information stored
* Logical isolation of pet data per user
* Configurable data retention policies

---

## 🧠 Evolution Path

### Phase 1

* Rule-based prediction
* Simple ingestion and notification

### Phase 2

* Introduce streaming and caching
* Improve scalability

### Phase 3

* ML-based personalization
* Feedback-driven improvements

---

## 📌 Summary

This architecture is designed to:

* Deliver real-time predictions with low latency
* Scale horizontally with increasing data volume
* Support future ML-driven personalization
* Maintain reliability through decoupled components and durable event streams

