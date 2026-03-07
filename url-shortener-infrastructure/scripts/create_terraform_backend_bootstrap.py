import os

base_path = "bootstrap/terraform-backend"

os.makedirs(base_path, exist_ok=True)

main_tf = """
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "terraform_state" {

  bucket = var.bucket_name

  tags = {
    Name = "terraform-state-bucket"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {

  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {

  bucket = aws_s3_bucket.terraform_state.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {

  name = var.dynamodb_table

  billing_mode = "PAY_PER_REQUEST"

  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "terraform-lock-table"
  }
}
"""

variables_tf = """
variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "bucket_name" {
  description = "Terraform state bucket"
  type        = string
}

variable "dynamodb_table" {
  description = "Terraform lock table"
  type        = string
}
"""

tfvars = """
aws_region      = "ap-south-1"
bucket_name     = "url-shortener-terraform-state-wasim"
dynamodb_table  = "terraform-state-lock"
"""

files = {
    "main.tf": main_tf,
    "variables.tf": variables_tf,
    "terraform.tfvars": tfvars
}

for filename, content in files.items():
    path = os.path.join(base_path, filename)

    with open(path, "w") as f:
        f.write(content)

    print(f"Created {path}")

print("\nTerraform backend bootstrap created successfully.")