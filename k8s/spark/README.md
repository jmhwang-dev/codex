# Spark jobs on Kubernetes

Example command to run a Spark job that converts CSV files in MinIO to
Iceberg tables.

```bash
kubectl run spark-driver --restart=Never \
  --image=ghcr.io/<USER>/spark:4.0.0 -- \
  spark-submit \
  --master k8s://https://$KUBERNETES_SERVICE_HOST:443 \
  --name csv2iceberg \
  --conf spark.kubernetes.container.image=ghcr.io/<USER>/spark:4.0.0 \
  local:///opt/spark/work-dir/convert_csv_to_iceberg.py
```
