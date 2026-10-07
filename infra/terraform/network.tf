# 가용 영역 조회 
data "aws_availability_zones" "available" {
  # 현재(리전 기준) 사용 가능한 availability_zone만 조회
  state = "available"
}
# VPC 생성 
resource "aws_vpc" "main" {
  # IPv4 CIDR 가용 범위
  cidr_block = var.vpc_cidr
  # DNS 기능 허용 
  enable_dns_support = true  # dns 해석 기능 활성화
  enable_dns_hostnames = true # VPC 내에서 dns_hostnames 사용 허가 
  # 태그 
  tags = { 
    Name= "{var.project_name}-vpc"
  }
}
# IGW 생성 
resource "aws_internet_gateway" "main" {}
# 서브넷 생성
resource "aws_subnet" "public" {}
# 라우트 테이블 생성
resource "aws_route_table" "public" {}
# 서브넷, IGw 연결, 라우트 할당
resource "aws_route_table_association" "public" {}