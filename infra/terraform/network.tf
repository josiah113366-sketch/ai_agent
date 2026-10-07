# 가용 영역 조회 
data "aws_availability_zones" "available" {}
# VPC 생성 
resource "aws_vpc" "main" {}
# IGW 생성 
resource "aws_internet_gateway" "main" {}
# 서브넷 생성
resource "aws_subnet" "public" {}
# 라우트 테이블 생성
resource "aws_route_table" "public" {}
# 서브넷, IGw 연결, 라우트 할당
resource "aws_route_table_association" "public" {}