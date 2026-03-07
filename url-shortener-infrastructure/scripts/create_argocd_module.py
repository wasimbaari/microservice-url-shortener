import os

path = "modules/argocd"

os.makedirs(path, exist_ok=True)

main = """
resource "helm_release" "argocd" {

  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"

  namespace        = "argocd"
  create_namespace = true

}
"""

variables = """
variable "namespace" {
  type    = string
  default = "argocd"
}
"""

with open(f"{path}/main.tf","w") as f:
    f.write(main)

with open(f"{path}/variables.tf","w") as f:
    f.write(variables)

print("ArgoCD module created successfully.")