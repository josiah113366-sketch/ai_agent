# EC2 -> 외부에서 8000 포트로 접근, SSH x, SSM 접근
# RDS -> EC2 Security Group 여기만 접근 가능, 5432만 허용

# EC2 시큐리티 그룹 
resource "aws_security_group" "ec2" {
  
}

# RDS 시큐리티 그룹 
resource "aws_security_group" "rds" {
  
}