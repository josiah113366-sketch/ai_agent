# Amazon Linux 2023 ec2 구성, bootstrap.sh로 user_data 전달 처리 
# 인프라 생성 후 실제 서비스 자동 설치
# DB 초기화(sql 마이그레이션(테이블 생성 -> 데이터 삽입)) 
# 컨테이너 실행

# 리눅스 정보 획득 
data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# 인스턴스 구성 