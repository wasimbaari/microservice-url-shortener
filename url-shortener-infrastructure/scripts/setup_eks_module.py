import os

BASE = os.getcwd()

ENV_MAIN = os.path.join(BASE, "environments", "dev", "main.tf")
EKS_DIR = os.path.join(BASE, "modules", "eks", "eks")

variables_file = os.path.join(EKS_DIR, "variables.tf")
outputs_file = os.path.join(EKS_DIR, "outputs.tf")

print("\nSetting up EKS module integration...\n")

# -----------------------------
# Create variables.tf
# -----------------------------

variables_content = """
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
"""

with open(variables_file, "w") as f:
    f.write(variables_content)

print("variables.tf created")

# -----------------------------
# Ensure outputs.tf exists
# -----------------------------

outputs_content = """
output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
"""

with open(outputs_file, "w") as f:
    f.write(outputs_content)

print("outputs.tf ensured")

# -----------------------------
# Add module to environment
# -----------------------------

eks_block = """

module "eks" {

  source = "../../modules/eks/eks"

  cluster_name    = "url-shortener-dev"
  cluster_version = "1.29"

  vpc_id = module.vpc.vpc_id

  private_subnet_ids = module.vpc.private_subnet_ids

  environment  = "dev"
  project_name = "url-shortener"

}
"""

with open(ENV_MAIN, "r") as f:
    main_content = f.read()

if 'module "eks"' not in main_content:
    with open(ENV_MAIN, "a") as f:
        f.write(eks_block)
    print("EKS module added to environments/dev/main.tf")
else:
    print("EKS module already exists, skipping")

print("\nEKS setup completed successfully.")
print("\nNext run:")
print("terraform fmt")
print("terraform validate")
print("terraform plan")