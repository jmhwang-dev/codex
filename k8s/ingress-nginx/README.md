# ingress-nginx

Add the repository and install the ingress controller via Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Then install the chart:

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=30880
```

Verify that all pods are running and check health at `http://<NODE_IP>:30880/healthz`.
