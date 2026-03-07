import os

path = "modules/monitoring"

os.makedirs(path, exist_ok=True)

main = """
resource "helm_release" "kube_prometheus_stack" {

  name       = "kube-prometheus-stack"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"

  namespace        = "monitoring"
  create_namespace = true

}

resource "helm_release" "loki" {

  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki"

  namespace        = "monitoring"
  create_namespace = true

}
"""

variables = """
variable "namespace" {
  type    = string
  default = "monitoring"
}
"""

with open(f"{path}/main.tf","w") as f:
    f.write(main)

with open(f"{path}/variables.tf","w") as f:
    f.write(variables)

print("Monitoring module created")