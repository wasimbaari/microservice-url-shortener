import os

base = os.getcwd()

vpc_main = os.path.join(base, "modules", "vpc", "main.tf")

print("Updating VPC module with routing and NAT gateway...")

routing_block = """

# Elastic IP for NAT
resource "aws_eip" "nat" {
  domain = "vpc"
}

# NAT Gateway
resource "aws_nat_gateway" "nat" {

  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "url-shortener-nat"
  }

}

# Public Route Table
resource "aws_route_table" "public" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.igw.id
  }

}

# Private Route Table
resource "aws_route_table" "private" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block     = "0.0.0.0/0"

    nat_gateway_id = aws_nat_gateway.nat.id
  }

}

# Public Subnet Associations
resource "aws_route_table_association" "public" {

  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id

  route_table_id = aws_route_table.public.id

}

# Private Subnet Associations
resource "aws_route_table_association" "private" {

  count = length(aws_subnet.private)

  subnet_id      = aws_subnet.private[count.index].id

  route_table_id = aws_route_table.private.id

}
"""

with open(vpc_main, "a") as f:
    f.write(routing_block)

print("Routing configuration added successfully.")