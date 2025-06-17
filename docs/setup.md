# Cluster Setup Guide

This guide outlines the steps required to bootstrap the three-node Kubernetes cluster and deploy the data engineering stack.

## 0. Cluster baseline

1. Check node architecture labels:

   ```bash
   kubectl get nodes -L kubernetes.io/arch
   ```

   The output should show `mini-pc=amd64` and each `raspberrypi=arm64`.
2. Ensure the control-plane node retains the `NoSchedule` taint.

## 1. Ingress-nginx installation

First add the repository and install using Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Install the chart:

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=30880
```

Verify:

```bash
kubectl -n ingress-nginx get pods
curl http://<NODE_IP>:30880/healthz
```

## 2. MinIO operator and tenant

Add the repository and deploy the operator:

```bash
helm repo add minio-operator https://operator.min.io/
helm repo update
helm install minio-operator minio-operator/minio-operator \
  -n minio-operator --create-namespace
```

Next apply the Tenant custom resource configured for four nodes with `requestAutoCert: false` and create the buckets `bronze`, `iceberg` and `warehouse` via the console.

The console is available at `http://<NODE_IP>:30880/minio`.

## 3. Iceberg REST catalog

Deploy the Iceberg REST container with environment variable `CATALOG_WAREHOUSE=s3://warehouse` and add an ingress path `/iceberg`.
Validate with:

```bash
curl http://<NODE_IP>:30880/iceberg/v1/config
```

A successful response returns HTTP status 200.

## 4. Spark 4.0 multi-arch image

Build and push a multi-architecture image to GHCR:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/<USER>/spark:4.0.0 . \
  --push
```

Check the manifest on GHCR to confirm that both `amd64` and `arm64` architectures are present.

## 5. First Spark job — CSV to Iceberg

Run the job inside the cluster:

```bash
kubectl run spark-driver --restart=Never \
  --image=ghcr.io/<USER>/spark:4.0.0 -- \
  spark-submit \
  --master k8s://https://$KUBERNETES_SERVICE_HOST:443 \
  --name csv2iceberg \
  --conf spark.kubernetes.container.image=ghcr.io/<USER>/spark:4.0.0 \
  local:///opt/spark/work-dir/convert_csv_to_iceberg.py
```

The job should complete successfully. After completion check that `iceberg/db/orders/metadata` exists in MinIO and run:

```bash
spark-sql "SELECT count(*) FROM iceberg.db.orders"
```

The count should be greater than zero.
