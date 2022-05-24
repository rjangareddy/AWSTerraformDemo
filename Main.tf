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
        organization = "AWSTerraformDemo"
   workspaces {
         name = "example-workspace"
     }
  }
}
