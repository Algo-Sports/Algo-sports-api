# AlgoSports Backend

알고리즘을 게임처럼 즐기면서 공부할 수 있도록 도와주는 알고리즘 게임 플랫폼 AlgoSports의 백엔드 저장소입니다.

- [AlgoSports Backend](#algosports-backend)
  - [Development](#development)
    - [브랜치 컨벤션](#브랜치-컨벤션)
    - [설치](#설치)
    - [서버 실행하기](#서버-실행하기)
    - [테스팅](#테스팅)
    - [명령어 모음 도구](#명령어-모음-도구)
  - [Build \& Deploy](#build--deploy)
    - [사전 준비물](#사전-준비물)
    - [ECS-CLI로 클러스터 생성](#ecs-cli로-클러스터-생성)
    - [Security Group 생성 및 80포트 오픈](#security-group-생성-및-80포트-오픈)
    - [ECR 로그인 및 레포지토리 생성](#ecr-로그인-및-레포지토리-생성)
    - [ECR 저장소 이미지 배포](#ecr-저장소-이미지-배포)
    - [ECS Task IAM role 생성](#ecs-task-iam-role-생성)
    - [서비스 생성](#서비스-생성)
  - [Trouble shootings](#trouble-shootings)
    - [Celery Worker가 Redis를 인식하지 못함](#celery-worker가-redis를-인식하지-못함)
    - [RDS 연결](#rds-연결)
    - [Nginx와 ELB를 사용할 때 502 오류](#nginx와-elb를-사용할-때-502-오류)

## Development

### 브랜치 컨벤션

[브랜치 컨벤션 참고자료](https://dev.to/couchcamote/git-branching-name-convention-cch)

1. `master`: 실제 배포에 사용되는 브랜치
2. `develop`: 개발 및 테스트에 사용되는 브랜치
3. temporary branches
   - `feat/<branch_name>`:기능 개발을 다루는 branch.
   - `bugfix/<branch_name>`: feature에서 발생한 버그를 다루는 branch.
   - `hotfix/<branch_name>`: master 브랜치에 바로 반영해야하는 버그를 다루는 branch.

### 설치

1. 가상환경 활성화

```
python -m venv venv
source venv/bin/activate
```

2. 패키지 설치

```shell
pip install -r requirements/local.txt
```

### 서버 실행하기

```shell
docker compose -f local.yml up -d
```

### 테스팅

```shell
# pytest
docker compose -f local.yml exec -T django coverage run -m pytest

# coverage
docker compose -f local.yml exec -T django coverage run -m pytest
docker compose -f local.yml exec -T django coverage report
```

### 명령어 모음 도구

아래 명령어를 통해서 사용할 수 있는 명령어 목록을 확인할 수 있습니다.

```shell
fab -l
```

## Build & Deploy

### 사전 준비물

- AWS CLI2 설치
  ```shell
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  ```
- ECS-CLI 설치
  ```shell
  sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
  sudo chmod +x /usr/local/bin/ecs-cli
  ```
- IAM 계정 생성 및 정책 연결
  ![IAM_정책](./docs/IAM_정책.png)

### ECS-CLI로 클러스터 생성

- 생성 후 만들어진 VPC, Subnets을 저장해둬야 합니다.
- key-pair를 먼저 생성하고 key-pair이름을 저장해둡니다.

```shell
# 환경변수 설정
AWS_DEFAULT_REGION=ap-northeast-2
CLUSTER_NAME=algo-cluster2
CONFIG_NAME=algo-config
PROFILE_NAME=algo-profile
INSTANCE_SIZE=3

KEY_PAIR=algo-keypair

# 클러스터 및 프로필 설정
ecs-cli configure --cluster $CLUSTER_NAME --region $AWS_DEFAULT_REGION --default-launch-type EC2 --config-name $CONFIG_NAME
ecs-cli configure profile --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY --profile-name $PROFILE_NAME
ecs-cli configure profile default --profile-name $PROFILE_NAME

# user-data 생성 (ecs-cluster에 연결하는 역할)
echo "#!/bin/bash \necho ECS_CLUSTER=jts-cluster >> /etc/ecs/ecs.config" > user_data.sh

# 클러스터 생성
ecs-cli up \
    --capability-iam \
    --keypair $KEY_PAIR \
    --size $INSTANCE_SIZE \
    --launch-type EC2 \
    --extra-user-data ./aws/user_data.sh
```

### Security Group 생성 및 80포트 오픈

```shell
VPC_ID=<Your VPC ID Here>
SG_NAME=algo-sg

# Security group 생성 및 GROUP_ID 저장
SG_GROUP_ID=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "Security Group for ECS $CLUSTER_NAME" \
    --vpc-id $VPC_ID |
    jq -r ".GroupId")

aws ec2 authorize-security-group-ingress \
    --group-id $SG_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0
```

### ECR 로그인 및 레포지토리 생성

```shell
# ECR 레포지토리 생성
aws ecr create-repository --repository-name django |
    jq ".repository | .repositoryUri"

aws ecr create-repository --repository-name nginx |
    jq ".repository | .repositoryUri"
```

### ECR 저장소 이미지 배포

```shell
# ECR, Docker 로그인
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/

docker-compose -f staging.yml -f production.yml build
docker-compose -f staging.yml -f production.yml push django nginx
```

### ECS Task IAM role 생성

```shell
# 빈 iam role 생성
aws iam create-role --role-name ecs-instance --assume-role-policy-document file://aws/assume-role.json

# 필요한 정책 추가
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role --role-name ecs-instance

# 인스턴스 프로필 생성
aws iam create-instance-profile --instance-profile-name ecs-instance-profile

# 해당 프로필에 롤 추가
aws iam add-role-to-instance-profile --instance-profile-name ecs-instance-profile --role-name ecs-instance

# instasnce profiles 출력
aws iam list-instance-profiles
```

### 서비스 생성

```shell
CONFIG_NAME=algo-config
PROJECT_NAME=algo-service

ecs-cli compose \
  --project-name $PROJECT_NAME \
  --file staging.yml \
  --file production.yml \
  --ecs-params ./aws/ecs-params.yml \
  service up \
  --create-log-groups \
  --cluster-config $CONFIG_NAME \
  --container-name nginx \
  --container-port 80 \
  --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:648240308375:targetgroup/target/e3086c4f494a30c4 \
  --launch-type EC2
```

## Trouble shootings

### Celery Worker가 Redis를 인식하지 못함

- **문제 상황**: AWS에 배포 후 로컬에서는 작동하던 Celery worker들이 Redis를 인식하지 못함
- **해결 방안**:
  - `docker-compose.yml` 파일에서 `redis`를 `links`와 `depends_on` 섹션에 모두 지정하여 문제를 해결함
  - Celery worker들이 Redis 서비스가 활성화된 후 실행되는 것을 보장함

### RDS 연결

- **문제 상황**: 애플리케이션이 RDS 인스턴스에 연결하지 못함
- **해결 방안**:
  - 애플리케이션과 RDS 인스턴스가 모두 같은 VPC 내에 있도록 설정함
  - 그럼에도 문제가 발생한다면 제대로 연결을 요청하고 있는지 확인이 필요함
  - `entrypoint.sh`에서 내보낸 환경 변수가 적용되지 않았던 것이도 문제였어서 환경 변수를 `.django` 및 `.postgres`로 분리하기 `DATABASE_URL` 환경 변수를 설정하여 문제를 해결했음

### Nginx와 ELB를 사용할 때 502 오류

- **문제 상황**: Nginx와 Elastic Load Balancer(ELB)를 통해 애플리케이션에 접근하려고 할 때 502 오류 발생
- **해결 방안**:
  - ECS tasks의 상태가 unhealthy 하여 문제가 발생함
  - ELB의 target group의 health check 설정을 변경하거나 nginx에서 200 OK 만을 반환하는 health check 라우트를 만들어 해결
