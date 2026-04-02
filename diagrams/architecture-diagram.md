
# System Diagram

```mermaid
flowchart LR

    %% Client Layer
    A[Mobile App / IoT Device] --> B[API Gateway]

    %% Ingestion Layer
    B --> C[Event Ingestion Service]

    %% Streaming Layer
    C --> D[(Event Stream<br/>Kafka / Kinesis)]

    %% Processing Layer
    D --> E[Prediction Engine]
    D --> F[(Event Store<br/>DynamoDB / S3)]

    %% Hot State / Cache
    E --> G[(Hot State Cache<br/>Redis)]

    %% Notification Layer
    E --> H[Notification Service]
    H --> I[Push / SMS / Email]

    %% Analytics / ML Layer
    F --> J[Analytics Pipeline]
    J --> K[(Data Warehouse / Data Lake)]
    K --> L[ML Training / Model Updates]
    L --> E
