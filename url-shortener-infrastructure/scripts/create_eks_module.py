import os

base_dir = "modules/eks"

files = {
    "main.tf": '''
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
''',

    "variables.tf": '''
variable "cluster_name" {
  type = string
}

variable "cluster_version" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "environment" {
  type = string
}

variable "project_name" {
  type = string
}
''',

    "outputs.tf": '''
output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
'''
}

os.makedirs(base_dir, exist_ok=True)

for filename, content in files.items():
    with open(os.path.join(base_dir, filename), "w") as f:
        f.write(content)

print("EKS Terraform module created successfully.")