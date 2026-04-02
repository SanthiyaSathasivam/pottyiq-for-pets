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
