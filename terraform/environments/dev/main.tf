terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "nimbus-tf-state"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "nimbus-tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "vpc" {
  source = "../../modules/vpc"

  project              = "nimbus"
  env                  = "dev"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
  availability_zones   = ["ap-south-1a", "ap-south-1b"]
}

module "ecr" {
  source = "../../modules/ecr"

  project          = "nimbus"
  repository_names = ["shortener-api", "redirect-svc", "analytics-worker", "dashboard-ui"]
  tags             = { Project = "nimbus", Environment = "dev", ManagedBy = "terraform" }
}

module "iam" {
  source = "../../modules/iam"

  project                 = "nimbus"
  env                     = "dev"
  cluster_oidc_issuer_url = module.eks.cluster_oidc_issuer_url
  tags                    = { Project = "nimbus", Environment = "dev", ManagedBy = "terraform" }
}

module "eks" {
  source = "../../modules/eks"

  project            = "nimbus"
  env                = "dev"
  public_subnet_ids  = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids
  node_role_arn      = module.iam.node_role_arn
  tags               = { Project = "nimbus", Environment = "dev", ManagedBy = "terraform" }
}
