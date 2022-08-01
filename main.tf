terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}



resource "aws_instance" "app_server" {
  ami           = "ami-065deacbcaac64cf2"
  instance_type = "t2.micro"

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    sudo apt update
    sudo apt install docker.io 
    sudo service docker start
    sudo usermod -a -G docker ubuntu
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    EOF

  tags = {
    Name = "CevaExemplu2"
  }
}

