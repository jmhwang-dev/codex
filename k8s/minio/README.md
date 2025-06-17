# MinIO deployment

1. Install the operator:

   ```bash
   helm install minio-operator minio-operator/minio-operator \
     -n minio-operator --create-namespace
   ```

2. Apply the Tenant custom resource from `tenant.yaml`.
3. Login to the console via the ingress route and create three buckets:
   `bronze`, `iceberg` and `warehouse`.
