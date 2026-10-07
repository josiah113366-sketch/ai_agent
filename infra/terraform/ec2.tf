# Amazon Linux 2023 ec2 구성, bootstrap.sh로 user_data 전달 처리 
# 인프라 생성 후 실제 서비스 자동 설치
# DB 초기화(sql 마이그레이션(테이블 생성 -> 데이터 삽입)) 
# 컨테이너 실행

# 리눅스 정보 획득 
data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# 인스턴스 구성 
resource "aws_instance" "agent" {
  # 이미지 -> 최신 아마존 리눅스 2023 AMI ID 사용 
  ami = data.aws_ssm_parameter.al2023_ami.value

  # ec2 인스턴스 유형 
  instance_type = var.ec2_instance_type

  # 서브넷 ID, ec2 배치 -> 0을 지정해서 사용 (설정)
  subnet_id = aws_subnet.public[0].id 

  # 보안 그룹 
  vpc_security_group_ids = [aws_security_group.ec2.id]

  # AWS 다른 서비스 api 호출 (ec2 객체 획득, bedrock 모델 호출, ssm parameter db url 획득)
  iam_instance_profile = aws_iam_instance_profile.ec2.name 

  # 사용자 데이터 구성
  user_data = templatefile("${path.module}/../scripts/bootstrap.sh", {
    # 원천 소스가 저장되어 있는 버킷 
    source_bucket = aws_s3_bucket.deploy-bucket
    # 다운로드할 소스(압축 파일)의 key 값 
    source_key  = aws_s3_object.source.key
    # 리전 
    aws_region = var.aws_region 
    # db 접속 url (동적 생성)
    database_url_parameter  = aws_ssm_parameter.database_url.name
    chat_model  = var.chat_model
    embed_model  = var.embed_model 
    # 임시용, 사용자 메모리를 위해서 고정 -> 추후 삭제, 사용자가 로그인하면 사용자별로 제공
    user_id  = var.user_id
  })
}