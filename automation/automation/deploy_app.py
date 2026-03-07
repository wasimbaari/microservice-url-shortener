import subprocess
from pathlib import Path

# project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# correct k8s api folder
API_DIR = ROOT_DIR / "k8s" / "api"

API_DIR.mkdir(parents=True, exist_ok=True)


deployment_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener-api
  namespace: url-shortener
spec:
  replicas: 2
  selector:
    matchLabels:
      app: url-shortener-api
  template:
    metadata:
      labels:
        app: url-shortener-api
    spec:
      containers:
      - name: api
        image: ghcr.io/piyushsachdeva/url-shortener:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: postgres://admin:password@postgres:5432/urlshortener
        - name: REDIS_URL
          value: redis://redis:6379
"""

service_yaml = """
apiVersion: v1
kind: Service
metadata:
  name: url-shortener-api
  namespace: url-shortener
spec:
  selector:
    app: url-shortener-api
  ports:
  - port: 80
    targetPort: 8000
"""

ingress_yaml = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: url-shortener-ingress
  namespace: url-shortener
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: url-shortener-api
            port:
              number: 80
"""


def write_yaml(filename, content):
    file_path = API_DIR / filename
    with open(file_path, "w") as f:
        f.write(content.strip())
    print(f"Created: {file_path}")


def apply_yaml():
    for file in API_DIR.glob("*.yaml"):
        print(f"Applying {file.name}")
        subprocess.run(["kubectl", "apply", "-f", str(file)], check=True)


def main():
    print("\nGenerating Kubernetes manifests in k8s/api...\n")

    write_yaml("deployment.yaml", deployment_yaml)
    write_yaml("service.yaml", service_yaml)
    write_yaml("ingress.yaml", ingress_yaml)

    print("\nApplying manifests to cluster...\n")
    apply_yaml()

    print("\nDeployment finished.")
    print("Check status with:")
    print("kubectl get pods -n url-shortener")
    print("kubectl get ingress -n url-shortener")


if __name__ == "__main__":
    main()