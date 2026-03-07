import os

base = "modules/eks-addons"

os.makedirs(base, exist_ok=True)

main_tf = '''
resource "aws_eks_addon" "vpc_cni" {
  cluster_name = var.cluster_name
  addon_name   = "vpc-cni"
}

resource "aws_eks_addon" "coredns" {
  cluster_name = var.cluster_name
  addon_name   = "coredns"
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = var.cluster_name
  addon_name   = "kube-proxy"
}

resource "aws_eks_addon" "ebs_csi" {
  cluster_name = var.cluster_name
  addon_name   = "aws-ebs-csi-driver"
}
'''

variables_tf = '''
variable "cluster_name" {
  type = string
}
'''

with open(f"{base}/main.tf","w") as f:
    f.write(main_tf)

with open(f"{base}/variables.tf","w") as f:
    f.write(variables_tf)

print("EKS addons module created.")