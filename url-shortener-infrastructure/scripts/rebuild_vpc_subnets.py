import os
import shutil

base = os.getcwd()
vpc_main = os.path.join(base, "modules", "vpc", "main.tf")

print("Rebuilding subnet resources safely...\n")

backup = vpc_main + ".backup"
shutil.copy(vpc_main, backup)
print("Backup created:", backup)

with open(vpc_main, "r") as f:
    content = f.read()

# Remove broken subnet resources
import re

content = re.sub(
    r'resource\s+"aws_subnet"\s+"public"\s*{[^}]*}',
    '',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'resource\s+"aws_subnet"\s+"private"\s*{[^}]*}',
    '',
    content,
    flags=re.DOTALL
)

# Correct subnet blocks
subnet_block = """

# Public Subnets
resource "aws_subnet" "public" {

  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index}"
    "kubernetes.io/role/elb" = "1"
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
    "kubernetes.io/role/internal-elb" = "1"
  }

}

"""

content += subnet_block

with open(vpc_main, "w") as f:
    f.write(content)

print("\nSubnet blocks rebuilt successfully.")
print("\nNow run:")
print("terraform fmt")
print("terraform validate")
print("terraform plan")