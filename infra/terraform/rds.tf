# 비밀번호 자동 생성 -> RDS 생성 -> 접속 URL 생성 -> SSM SecurityString으로 저장

# 비밀번호 생성 
resource "random_password" "database" {
}

# 서브넷 그룹 구성 
resource "aws_db_subnet_group" "main" {
}

# RDS 생성
resource "aws_db_instance" "postgres" {
}

# 접속 URL 동적 구성 SSM SecurityString으로 저장 
resource "aws_ssm_parameter" "database_url" {
  
}