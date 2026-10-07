# 비밀번호 자동 생성 -> RDS 생성 -> 접속 URL 생성 -> SSM SecurityString으로 저장

# 비밀번호 생성 
resource "random_password" "database" {
  # 자동 생성할 비번의 길이 지정
  length = 24
  # DB URL에 특수 문자 포함 여부 설정 -> 비번에 특수 문자 포함 
  special = false # 배제 
}

# 서브넷 그룹 구성 
resource "aws_db_subnet_group" "main" {
  # SSM parameter의 이름
  name = "${var.project_name}-db-subnets" 
  # vpc에서 구성한 서브넷 id 세팅 
  subnet_ids = aws_subnet.public[*].id
  tags = {
    Name = "${var.project_name}-db-subnets" 
  }
}

# RDS 생성
resource "aws_db_instance" "postgres" {
}

# 접속 URL 동적 구성 SSM SecurityString으로 저장 
resource "aws_ssm_parameter" "database_url" {
  
}