
module "vpc" {

  source = "../../modules/vpc"

  vpc_cidr = var.vpc_cidr

  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs

  azs = var.availability_zones
}

module "eks" {

  source = "../../modules/eks/eks"

  cluster_name    = "url-shortener-dev"
  cluster_version = "1.29"

  vpc_id = module.vpc.vpc_id

  private_subnet_ids = module.vpc.private_subnet_ids

  environment  = "dev"
  project_name = "url-shortener"

}
