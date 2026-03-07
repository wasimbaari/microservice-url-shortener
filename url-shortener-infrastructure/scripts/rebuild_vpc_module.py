import os
import shutil

BASE = os.getcwd()
VPC_DIR = os.path.join(BASE, "modules", "vpc")

print("\nRebuilding Terraform VPC module...\n")

# Delete old module
if os.path.exists(VPC_DIR):
    shutil.rmtree(VPC_DIR)
    print("Old VPC module deleted")

# Recreate folder
os.makedirs(VPC_DIR, exist_ok=True)

# ---------- main.tf ----------

main_tf = """
resource "aws_vpc" "main" {

  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "url-shortener-vpc"
  }
}

resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "url-shortener-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public" {

  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index}"
  }
}

# Private Subnets
resource "aws_subnet" "private" {

  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.azs[count.index]

  tags = {
    Name = "private-subnet-${count.index}"
  }
}
"""

# ---------- variables.tf ----------

variables_tf = """
variable "vpc_cidr" {
  type = string
}

variable "public_subnet_cidrs" {
  type = list(string)
}

variable "private_subnet_cidrs" {
  type = list(string)
}

variable "azs" {
  type = list(string)
}
"""

# ---------- outputs.tf ----------

outputs_tf = """
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
"""

# Write files
with open(os.path.join(VPC_DIR, "main.tf"), "w") as f:
    f.write(main_tf)

with open(os.path.join(VPC_DIR, "variables.tf"), "w") as f:
    f.write(variables_tf)

with open(os.path.join(VPC_DIR, "outputs.tf"), "w") as f:
    f.write(outputs_tf)

print("New VPC module created successfully.\n")
print("Location:", VPC_DIR)