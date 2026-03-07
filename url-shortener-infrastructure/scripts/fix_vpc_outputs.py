import os
import re
import shutil

BASE_DIR = os.getcwd()

VPC_MODULE = os.path.join(BASE_DIR, "modules", "vpc")
MAIN_TF = os.path.join(VPC_MODULE, "main.tf")
OUTPUTS_TF = os.path.join(VPC_MODULE, "outputs.tf")

print("\nScanning VPC module...\n")

if not os.path.exists(MAIN_TF):
    print("ERROR: main.tf not found in modules/vpc")
    exit()

with open(MAIN_TF, "r") as f:
    main_content = f.read()

# Detect subnet resource names
public_match = re.search(r'resource\s+"aws_subnet"\s+"([^"]*public[^"]*)"', main_content)
private_match = re.search(r'resource\s+"aws_subnet"\s+"([^"]*private[^"]*)"', main_content)

public_name = public_match.group(1) if public_match else None
private_name = private_match.group(1) if private_match else None

print(f"Detected public subnet resource: {public_name}")
print(f"Detected private subnet resource: {private_name}")

if not public_name or not private_name:
    print("\nERROR: Could not detect subnet resources in main.tf")
    exit()

# Backup outputs.tf
if os.path.exists(OUTPUTS_TF):
    backup = OUTPUTS_TF + ".backup"
    shutil.copy(OUTPUTS_TF, backup)
    print(f"Backup created: {backup}")

# Generate correct outputs.tf
outputs_content = f'''
output "vpc_id" {{
  value = aws_vpc.main.id
}}

output "public_subnet_ids" {{
  value = aws_subnet.{public_name}[*].id
}}

output "private_subnet_ids" {{
  value = aws_subnet.{private_name}[*].id
}}
'''

with open(OUTPUTS_TF, "w") as f:
    f.write(outputs_content)

print("\noutputs.tf successfully updated!")
print("You can now run:\n")
print("terraform validate")