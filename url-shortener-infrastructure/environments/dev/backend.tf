
terraform {

  backend "s3" {

    bucket = "url-shortener-terraform-state-wasim"
    key    = "dev/terraform.tfstate"
    region = "ap-south-1"

    dynamodb_table = "terraform-state-lock"

    encrypt = true
  }
}