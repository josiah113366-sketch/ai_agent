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
  # RDS 식별 이름 
  identifier = "${var.project_name}-postgres" 

  # 디비 엔진 지정
  engine = "postgres"
  # 제품 버전
  engine_version = var.postgre_version
  # rds 인스턴스 클래스 
  instance_class = var.db_instance_class

  # 하드웨어 
  # 생성 초기 스토리지 용량 (GB)
  allocated_storage = 20 
  # 자동 스토리지 확장 시 최대 용량 (GB)
  max_allocated_storage = 30 
  # RDS 스토리지 타입 
  storage_type = "gp3"
  # RDS 저장 데이터의 암호화 
  storage_encrypted = true

  # 초기 구성
  # 디비명 
  db_name = var.db_name
  # 사용자 -> RDS 관리자 
  username = var.db_username
  # 관리자 비밀번호 -> 24자리 (특수 문자 제외)
  password = random_password.database.result 
  # 기본 포트 
  port = 5432 
}

# 접속 URL 동적 구성 SSM SecurityString으로 저장 
resource "aws_ssm_parameter" "database_url" {
  
}