
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
