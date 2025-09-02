# iRoute: Local Routing Table-based Workflow Management in Serverless Computing

iRoute is a workflow orchestration and routing system designed to achieve **universal 1-hop transfers** while maintaining high resource efficiency. To address the limitations of centralized orchestration, iRoute **offloads both orchestration and routing capabilities from global to local**. It adopts a **dual-layer architecture**:

- **Local routing controllers** make routing decisions and manage direct communication between function instances.
- **Centralized coordinator** ensures global consistency by synchronizing multiple local routing tables.

iRoute runs as a set of **OpenFaaS** templates and supports **IPC**, **Socket**, and **RDMA** communication.

---

## Installation

iRoute requires the following components to be installed:

- [OpenFaaS](deploy/OpenFaaS/README.md)
- [ZooKeeper](deploy/ZooKeeper/README.md) (for global routing table storage)
- [k8s-rdma-shared-dev-plugin](deploy/k8s-rdma-shared-dev-plugin/README.md) (for RDMA support)
- [sn-db](deploy/sn-db/README.md): Database services for Social Network benchmark.

---

## Usage

### Templates Overview

| Template           | Role                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------|
| **python3-cc**     | Coordinator: assists in direct connection setup and synchronizes routing tables with ZooKeeper. |
| **python3-func**   | Function instance: performs routing and communication directly with other functions.      |
| **python3-entry**  | Workflow entry: handles service discovery and sends workflow requests.                    |

> **Note:** `python3-func` **does not support OpenFaaS Gateway invocation**. Always invoke workflows through `python3-entry`.

---

### Configuration Steps

#### 1. Coordinator (`python3-cc`)
- Define workflow structure in `workflow.json`.  
  - Function names must match the ones deployed in OpenFaaS.
- Update `handler.py` with ZooKeeper authentication credentials for accessing the global routing table.
- Modify the `get_lat_dist` function in `handler.py` to measure and report request latency distribution.

#### 2. Function Instance (`python3-func`)
- Synchronize and use the same `workflow.json`.

#### 3. Workflow Entry (`python3-entry`)
- Update `handler.py` with:
  - Coordinator function name in OpenFaaS.
  - Entry function name.
  - The `generate_data` function for test data generation.

---

## Benchmarks

The [`benchmarks`](benchmarks/) directory includes three representative applications, each implemented for **IPC**, **Socket**, and **RDMA** backends:

| Application                            | Description                                   | Path                                                      |
|---------------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| **Social Network**                    | A latency-sensitive application from [DeathstarBench](https://github.com/delimitrou/DeathStarBench/tree/master/socialNetwork) that creates post embedded with text, media, links and user tags. | [benchmarks/sn](benchmarks/sn/)     |
| **FINRA**                             | A financial application that validates trades based on trade and market data.                    | [benchmarks/finra](benchmarks/finra/)                       |
| **ExCamera**                          | A video-processing application that encodes and processes chunks in parallel.                   | [benchmarks/excamera](benchmarks/excamera/)                 |

Each benchmark directory provides:

- A **README** with deployment and execution steps.
- Prebuilt Docker images available on Docker Hub.
- Configurations for OpenFaaS deployment.

For detailed instructions, see [Benchmark Documentation](benchmarks/).


