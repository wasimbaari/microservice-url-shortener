import os
import shutil
import re

BASE_DIR = os.getcwd()
VPC_FILE = os.path.join(BASE_DIR, "modules", "vpc", "main.tf")

print("\nFixing EKS subnet tags in Terraform VPC module...\n")

if not os.path.exists(VPC_FILE):
    print("ERROR: modules/vpc/main.tf not found")
    exit()

# Backup file
backup = VPC_FILE + ".backup"
shutil.copy(VPC_FILE, backup)
print(f"Backup created: {backup}")

with open(VPC_FILE, "r") as f:
    content = f.read()

# Remove incorrect VPC tags
content = content.replace('"kubernetes.io/role/elb" = "1"', '')
content = content.replace('"kubernetes.io/role/internal-elb" = "1"', '')

# Fix public subnet block
public_pattern = r'resource\s+"aws_subnet"\s+"public"\s*{[^}]*tags\s*=\s*{'
public_replace = '''resource "aws_subnet" "public" {

  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index}"
    "kubernetes.io/role/elb" = "1"
  }
'''

content = re.sub(public_pattern, public_replace, content, flags=re.DOTALL)

# Fix private subnet block
private_pattern = r'resource\s+"aws_subnet"\s+"private"\s*{[^}]*tags\s*=\s*{'
private_replace = '''resource "aws_subnet" "private" {

  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.azs[count.index]

  tags = {
    Name = "private-subnet-${count.index}"
    "kubernetes.io/role/internal-elb" = "1"
  }
'''

content = re.sub(private_pattern, private_replace, content, flags=re.DOTALL)

with open(VPC_FILE, "w") as f:
    f.write(content)

print("\nEKS subnet tags fixed successfully.")
print("\nNext run:")
print("terraform fmt")
print("terraform plan")
print("terraform apply -auto-approve")