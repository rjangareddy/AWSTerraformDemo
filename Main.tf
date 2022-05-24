terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
     random = {
       source ="hashicorp/random"
     }
  } 
   backend "remote" {
        organization = "OnixCFADemoPoc"
   workspaces {
         name = "AWSTerraformDemo"
     }
  }
}
provider "aws" {
  region = "us-east-2"
}
