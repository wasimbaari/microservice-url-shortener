import os

ROOT = os.getcwd()

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)
        print(f"Created: {path}")
    else:
        print(f"Skipped (already exists): {path}")


#########################################
# 1. GITHUB ACTIONS CI/CD PIPELINE
#########################################

ci_pipeline = """
name: CI Pipeline

on:
  push:
    branches: [ main ]

jobs:

  build:

    runs-on: ubuntu-latest

    steps:

    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v3
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
        aws-region: ap-south-1

    - name: Login to ECR
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build Images
      run: |
        docker build -t link-service ./services/link-service
        docker build -t redirect-service ./services/redirect-service
        docker build -t stats-service ./services/stats-service

    - name: Scan with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: link-service

    - name: Push Images to ECR
      run: |
        echo "Push commands should be added here"
"""

create_file(".github/workflows/ci.yml", ci_pipeline)


#########################################
# 2. GITOPS STRUCTURE
#########################################

gitops_readme = """
This repository folder contains GitOps deployment manifests.

ArgoCD watches this repo and automatically deploys Helm charts.
"""

create_file("gitops/README.md", gitops_readme)


#########################################
# 3. ARGOCD APPLICATION
#########################################

argocd_app = """
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: url-shortener
  namespace: argocd

spec:
  project: default

  source:
    repoURL: https://github.com/wasimbaari/url-shortener-gitops
    targetRevision: HEAD
    path: helm/url-shortener

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
"""

create_file("gitops/argocd/application.yaml", argocd_app)


#########################################
# 4. RBAC SECURITY POLICY
#########################################

rbac = """
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: url-shortener-role
  namespace: production

rules:
- apiGroups: [""]
  resources: ["pods","services"]
  verbs: ["get","list","watch"]
"""

create_file("k8s/security/rbac.yaml", rbac)


#########################################
# 5. KUBERNETES SECRET TEMPLATE
#########################################

secret = """
apiVersion: v1
kind: Secret

metadata:
  name: database-secret

type: Opaque

data:
  DB_PASSWORD: cGFzc3dvcmQ=
"""

create_file("k8s/security/secrets.yaml", secret)


#########################################
# 6. HORIZONTAL POD AUTOSCALER
#########################################

hpa = """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler

metadata:
  name: link-service-hpa

spec:

  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: link-service

  minReplicas: 2
  maxReplicas: 10

  metrics:

  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"""

create_file("k8s/autoscaling/hpa.yaml", hpa)


#########################################
# 7. CLUSTER AUTOSCALER HELM VALUES
#########################################

cluster_autoscaler = """
autoDiscovery:
  clusterName: url-shortener-eks

awsRegion: ap-south-1

rbac:
  create: true

replicaCount: 1
"""

create_file("k8s/autoscaling/cluster-autoscaler-values.yaml", cluster_autoscaler)


#########################################
# 8. ECR IMAGE REPOSITORY LIST
#########################################

ecr = """
ECR repositories required:

url-shortener/link-service
url-shortener/redirect-service
url-shortener/stats-service
url-shortener/frontend
"""

create_file("configs/ecr-repositories.txt", ecr)


print("\\nDevOps platform bootstrap completed successfully.")