# AWS provider의 필요한 실제 설정 
provider "aws" {
  # 리전 설정
  region = var.aws_region
}