# SmartPot-Proxy (Legacy Architecture Reference)

> [!NOTE]
> **Legacy Stack A Architecture**: Deprecated and archived. Superseded in Canonical Stack B by direct MQTT TLS communication via [SmartPot-Broker](https://github.com/SmartPotTech/SmartPot-Broker) (EMQX 5.8.9) and [SmartPot-API](https://github.com/SmartPotTech/SmartPot-API) (Go 1.27.3 / Echo v4.16.3).

## Project Status

[![Build and Publish Proxy Docker Image](https://github.com/SmartPotTech/SmartPot-Proxy/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/SmartPotTech/SmartPot-Proxy/actions/workflows/build-and-publish.yml)

## Description

SmartPot-Proxy was an early prototype reverse proxy built with Python 3.10 and FastAPI that forwarded HTTP telemetry from ESP32 microcontrollers to the backend before the adoption of the unified MQTT v1 architecture.

```mermaid
flowchart LR
  subgraph legacy["Legacy Stack A · Obsolete Prototype Architecture"]
    direction TB
    client["IoT Client / Frontend Client"]
    subgraph proxy["SmartPot-Proxy · Python 3.10 · FastAPI :8092"]
      direction TB
      login["POST /api/login<br/>Authentication Forwarding"]
      record["POST /api/crops/{cropId}/records<br/>Telemetry Forwarding"]
      cors["CORS & Request Forwarder<br/>httpx.AsyncClient"]
    end
    legacy_api["SmartPot-API-Java (Spring Boot :8080)"]
    client -->|"HTTP REST :8092"| proxy
    login & record --> cors
    cors -->|"HTTP REST :8080"| legacy_api
  end

  subgraph migration["Evolution to Canonical Stack B"]
    direction TB
    note["<b>Superseded in Stack B:</b><br/>HTTP proxy bottleneck eliminated.<br/>Direct high-throughput MQTT TLS (8883)<br/>and native Go API (:8091)"]
  end

  subgraph canonical["Canonical Stack B Architecture"]
    direction TB
    iot_b["IoT Device (Rust / MicroPython)"]
    broker_b["SmartPot-Broker (EMQX 5.8.9 · TLS :8883)"]
    api_b["SmartPot-API (Go 1.27.3 · Echo v4.16.3 :8091)"]
    iot_b <-->|"MQTT over TLS :8883"| broker_b
    broker_b <-->|"Webhook Auth / Ingest"| api_b
  end

  legacy -.->|"Replaced By"| migration
  migration -.->|"Implemented As"| canonical

  classDef leaf fill:#DDF5EA,stroke:#067A52,color:#17261F
  classDef water fill:#E3F2FB,stroke:#1F6FA0,color:#17261F
  classDef clay fill:#FBE9E1,stroke:#B85A38,color:#17261F
  classDef sun fill:#FDF4DD,stroke:#C98D12,color:#17261F
  classDef core fill:#067A52,stroke:#0B3D2B,color:#FFFFFF

  class client,legacy_api,iot_b,broker_b,api_b core
  class proxy,login,record,cors clay
  class note sun
  class canonical leaf
```

## Docker Image Build (Historical)

1. Build the Docker container image:

   ```bash
   docker build -t sebastian190030/proxy-smartpot:latest .
   ```

2. Publish to container registry:

   ```bash
   docker push sebastian190030/proxy-smartpot:latest
   ```
