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
  # 버킷 지정 
  bucket = aws_s3_bucket.deploy.id
  # 액세스 설정 -> 모두 차단 
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 버킷에 업로드될 리소스 암호화 처리 
resource "aws_s3_bucket_server_side_encryption_configuration" "deploy" {
  bucket = aws_s3_bucket.deploy.id
  # s3 서버측 암호화 규칙 정의 
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 업로드할 프로젝트 압축 (배제되는 파일도 존재함)
# CI/CD 사용하지 않는 구조
resource "archive_file" "source" {
  # 종류
  type = "zip"
  # 소스 코드 위치 -> 현재 위치에서 2단계 위 레벨임 
  source_dir = "${path.module}/../.."
  # zip 파일 생성 -> tf 파일이 있는 곳에 생성한다 
  output_path = "${path.module}/agent-source.zip"
  # zip에 미포함 목록 
  excludes = [
    ".git",
    ".env",
    "__pycache__",
    "infra/terraform/.terraform",
    "infra/terraform/.terraform-build",
    "infra/terraform/agent-source.zip",
    "infra/terraform/terraform.tfstate",
    "infra/terraform/terraform.tfstate.backup",
    # 기타 필요 없는 파일들 포함
  ]
}

# 버킷에 zip 파일 업로드
resource "aws_s3_object" "source" {
  # 업로드할 버킷 
  bucket = aws_s3_bucket.deploy.id
  # key -> 파일명에 해시값을 적용하여 변화 감지 
  key = "releases/agent-source-${data.archive_file.source.output_md5}.zip"
  # 로컬 파일의 위치
  source = data.archive_file.output_path
  # 소스에 MD5 적용하여 파일 변경 시 s3 object 감지 
  etag = data.archive_file.source.output_md5
}