import os
import shutil

BASE_DIR = os.getcwd()
VPC_MAIN = os.path.join(BASE_DIR, "modules", "vpc", "main.tf")

print("\nAdding EKS subnet tags to VPC module...\n")

if not os.path.exists(VPC_MAIN):
    print("ERROR: modules/vpc/main.tf not found")
    exit()

# Backup original file
backup_file = VPC_MAIN + ".backup"
shutil.copy(VPC_MAIN, backup_file)
print(f"Backup created: {backup_file}")

with open(VPC_MAIN, "r") as f:
    content = f.read()

# Public subnet tag
public_tag = '"kubernetes.io/role/elb" = "1"'

# Private subnet tag
private_tag = '"kubernetes.io/role/internal-elb" = "1"'

if public_tag in content and private_tag in content:
    print("Tags already exist. No changes needed.")
    exit()

# Add tags inside public subnet block
content = content.replace(
    'tags = {',
    'tags = {\n    "kubernetes.io/role/elb" = "1"',
    1
)

# Add tags inside private subnet block
content = content.replace(
    'tags = {',
    'tags = {\n    "kubernetes.io/role/internal-elb" = "1"',
    1
)

with open(VPC_MAIN, "w") as f:
    f.write(content)

print("\nSubnet tags successfully added.")
print("Now run:\n")
print("terraform plan")
print("terraform apply -auto-approve")