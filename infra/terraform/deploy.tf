# 현재 프로젝트 압축(zip) -> s3 비공개 버킷 업로드 

# 버킷 생성 시 이름에 랜덤 부여 
resource "random_id" "bucket_suffix" {
  # 랜덤 값 크기 
  byte_length = 4 
}

# 버킷 생성 
resource "aws_s3_bucket" "deploy" {
  # 버킷명이 매번 생성해도 중복 x (고유한 이름 가짐)
  bucket = "${var.project_name}-deploy-${random_id.bucket_suffix.hex}"
  # 버킷이 삭제될 때 내부에 객체가 있어도 함께 삭제할 것인가? 
  force_destroy = true
  tags = { 
    Name = "${var.project_name}-deploy-s3" 
  }
}

# 버킷에 비공개 설정
resource "aws_s3_bucket_public_access_block" "deploy" {
}

# 버킷에 업로드될 리소스 암호화 처리 
resource "aws_s3_bucket_server_side_encryption_configuration" "deploy" {
}

# 업로드할 프로젝트 압축 (배제되는 파일도 존재함)
# CI/CD 사용하지 않는 구조
resource "archive_file" "source" {
}

# 버킷에 zip 파일 업로드
resource "aws_s3_object" "source" {
  
}