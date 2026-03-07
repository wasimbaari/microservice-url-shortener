import os

path = "modules/alb-controller"

os.makedirs(path, exist_ok=True)

main = """
resource "helm_release" "aws_load_balancer_controller" {

  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"

  namespace = "kube-system"

  set {
    name  = "clusterName"
    value = var.cluster_name
  }

}
"""

variables = """
variable "cluster_name" {
  type = string
}
"""

with open(f"{path}/main.tf","w") as f:
    f.write(main)

with open(f"{path}/variables.tf","w") as f:
    f.write(variables)

print("ALB controller module created")