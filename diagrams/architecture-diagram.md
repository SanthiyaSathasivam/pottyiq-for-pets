# System Architecture Diagram

This diagram illustrates the end-to-end event-driven architecture for PottyIQ, showing how pet activity signals are ingested, processed, and used to generate real-time predictions and alerts.


# System Diagram

```mermaid
flowchart LR

    subgraph Client["Client Layer"]
        A[Mobile App / IoT Device]
    end

    subgraph API["API Layer"]
        B[API Gateway]
        C[Event Ingestion Service]
    end

    subgraph Stream["Streaming Layer"]
        D[(Event Stream<br/>Kafka / Kinesis)]
    end

    subgraph Core["Core Processing"]
        E[Prediction Engine]
        F[(Event Store<br/>DynamoDB / S3)]
        G[(Hot State Cache<br/>Redis)]
    end

    subgraph Notify["Notification Layer"]
        H[Notification Service]
        I[Push / SMS / Email]
    end

    subgraph Analytics["Analytics & ML"]
        J[Analytics Pipeline]
        K[(Data Warehouse / Data Lake)]
        L[ML Training / Model Updates]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    E --> G
    E --> H
    H --> I
    F --> J
    J --> K
    K --> L
    L --> E
```
## 🔄 High-Level Flow

1. Pet activity events are captured via mobile app or IoT devices  
2. Events are ingested through API and pushed to a streaming system  
3. Prediction engine processes real-time and historical signals  
4. System computes the next probable potty window  
5. Notification service sends alerts to the user  
6. Historical data feeds into analytics and ML training
   
## 🧠 Design Principles

- **Decoupled architecture** using event streaming for scalability  
- **Separation of concerns** between ingestion, processing, and notification  
- **Real-time + batch hybrid** for responsiveness and learning  
- **Horizontal scalability** through partitioning by petId  
- **Resilience** via durable event storage and replay capability  
