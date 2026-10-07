variable "aws_region" {
  description = "AWS 리전"
  type = string
  default = "us-east-1"
}

# AWS 리소스 간 공통 prefix 
variable "project_name" {
  description = "프로젝트별 구분 값"
  type = string
  default = "agent-de-ai-16"
}

# VPC 대역
# VPC에서 사용할 전체 IP 주소 범위
variable "vpc_cidr" {
  description = "VPC CIDR"
  type = string
  # 10.30.0.0 ~ 10.30.255.255 가용 범위 
  default = "10.30.0.0/16"
}

# EC2 관련 
# Agent/faspapi 
variable "ec2_instance_type" {
  description = "에이전트 구동용 ec2"
  type = string
  # 최소 규모로 지정
  default = "t3.micro"
}

# RDS내에 디비명 
variable "db_name" {
  description = "벡터 디비명"
  type = string
  default = "agentlab"
}

# RDS 내에 사용자명 
variable "db_username" {
  description = "벡터 디비명 접근 사용자명"
  type = string
  default = "agent"
}

# RDS 내에 비밀번호 -> rds.tf에서 랜덤으로 구성 -> SSM에서 관리 -> AWS KMS 저장

# RDS 인스턴스 사양 
variable "db_instance_class" {
  description = "RDS 인스턴스 유형"
  type = string
  # 소형 스펙
  default = "db.t4g.micro"
}

# PostgreSQL 엔진 버전 
variable "postgre_version" {
  description = "엔진 버전"
  type = string
  default = "16"
}

# Bedrock Model ID 
variable "bedrock_chat_model" {
  description = "엔트로픽 기본 모델"
  type = string
  # Agent가 사용하는 Claude 모델 ID, 리전이 변경되면 `us.` 변경됨 
  default = "us.anthropic.claude-sonnet-5"
}

# 임베딩 모델
variable "bedrock_embed_model" {
  description = "임베딩 모델"
  type = string
  # Agent가 텍스트를 토근화할 때 사용하는 모델, 필요 시 다른 토크나이저 모델 사용 가능 -> 현재 최대1024
  # 더 많은 텍스트를 관리 -> 다른 모델 사용 -> claude, gpt 등에서 제공(유료), 허깅페이스 사용(무료)
  default = "amazon.titan-embed-text-v2:0"
}

# Agent Memory에 대한 기본 사용자 ID 
variable "user_id" {
  description = "임시 사용자 ID"
  type = string
  default = "demo_user-16"
}

# SSH 관련 (키 페어 등)
# SSH 접근 IP 대역  -> 자기 자신 IP 