# Kubernetes Data Engineering Infrastructure

This repository contains configuration and application code for a small
Kubernetes cluster composed of three nodes:

1. `mini-pc` – `amd64`, 16GB RAM
2. `raspberrypi` – `arm64`, 8GB RAM (x2)

The stack includes MinIO, Apache Iceberg, Apache Spark and ingress-nginx.
The Olist dataset from Kaggle is used as sample data.

The repository is organized as follows:

- `docs/` – high level guides and explanations
- `k8s/` – Kubernetes manifests and Helm notes
  - `ingress-nginx/` – installation of ingress controller
  - `minio/` – MinIO operator and tenant configuration
  - `iceberg/` – Iceberg REST catalog deployment
  - `spark/` – Spark job launch examples
- `spark/` – Dockerfile and application code for Spark

