# AlgoSports Backend

## Development

### Branch

- 아래 포스트의 convention을 일부 차용해서 사용한다.
  - https://dev.to/couchcamote/git-branching-name-convention-cch

1. master
   - 실제 배포
2. develop
   - 개발 및 테스트
3. temporary branches

   - feat/<branch_name>
     - 기능 개발을 다루는 branch.
   - bugfix/<branch_name>
     - feature에서 발생한 버그를 다루는 branch.
   - hotfix/<branch_name>
     - master 브랜치에 바로 반영해야하는 버그를 다루는 branch.
   - experimental/<branch_name>
     - 테스트하고 싶은 기능을 다루는 branch.

### Installation

1. Activate virtual environment
2. Install packages
   ```shell
   pip install -r requirements/local.txt
   ```

### Start local server

```shell
python manage.py runserver
```

### Test

```shell
pytest .
mypy .
```

## Build & Deploy
