import os

project_name = "url-shortener-infrastructure"

structure = {
    "modules": {
        "vpc": [
            "main.tf",
            "variables.tf",
            "outputs.tf",
            "locals.tf"
        ]
    },
    "environments": {
        "dev": [
            "backend.tf",
            "main.tf",
            "variables.tf",
            "terraform.tfvars"
        ]
    }
}

file_templates = {
    "modules/vpc/variables.tf": """
variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "public_subnet_cidrs" {
  type = list(string)
}

variable "private_subnet_cidrs" {
  type = list(string)
}

variable "availability_zones" {
  type = list(string)
}
""",

    "modules/vpc/locals.tf": """
locals {
  name_prefix = "${var.project_name}-${var.environment}"
}
""",

    "modules/vpc/outputs.tf": """
output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
""",

    "modules/vpc/main.tf": """
resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}
""",

    "environments/dev/backend.tf": """
terraform {
  backend "s3" {
    bucket         = "url-shortener-tf-state"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
  }
}
""",

    "environments/dev/main.tf": """
module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  environment  = var.environment

  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}
""",

    "environments/dev/variables.tf": """
variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "public_subnet_cidrs" {
  type = list(string)
}

variable "private_subnet_cidrs" {
  type = list(string)
}
""",

    "environments/dev/terraform.tfvars": """
project_name = "urlshortener"
environment  = "dev"

vpc_cidr = "10.0.0.0/16"

availability_zones = [
  "ap-south-1a",
  "ap-south-1b"
]

public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]

private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24"
]
"""
}


def create_structure(base_path, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(contents, dict):
            create_structure(folder_path, contents)
        else:
            for file in contents:
                file_path = os.path.join(folder_path, file)
                with open(file_path, "w") as f:
                    template_key = os.path.join(folder, file)
                    if template_key in file_templates:
                        f.write(file_templates[template_key])
                    else:
                        f.write("")


os.makedirs(project_name, exist_ok=True)
create_structure(project_name, structure)

for path, content in file_templates.items():
    full_path = os.path.join(project_name, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

with open(os.path.join(project_name, "README.md"), "w") as f:
    f.write("# URL Shortener Infrastructure\n\nTerraform infrastructure project.")

print("Terraform project scaffold created successfully!")