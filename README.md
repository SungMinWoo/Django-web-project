# Django-web-project

정치인 커뮤니티

URL - https://poty.co.kr

# 개발 목표 
Django의 전반적인 이해, Django ORM 기능 활용, AWS(EC2, RDS, Route53) 실 사용

# 사용 기술
* Django(summernote, crontab, storages)
* HTML, CSS, JavaScript, jQuery
* Nginx
* Gunicorn
* AWS - EC2, RDS(PostgreSql), Route53, Certificate Manager
* Gmail API

# 기능
### 회원관련
* 회원 정보 수정, 자동 로그인, 내가 쓴 글 및 댓글, 이메일 인증(Gmail api), 회원 탈퇴 기능
### 게시판관련
* 글작성, 댓글 및 대댓글 작성, 추천 기능, 유저별 게시판 권한 부여, 신고 기능, 클릭당 조회수 기능, 게시판 별 색 변환
### 정치인 정보 및 평가 관련
* 정치인 평가 별점, 평가 글자수 제한 및 실시간 글자수 세기, 정치인별 평점 평균 집계
### 그 외
* 악성 유저 ip밴, 반복 요청시 요청 제한, AWS S3 이미지 업로드

# Advenced feature
* Django summernote의 이미지 파일 관련 단점 보완

```python
def delete_img_s3(contents, bool=True):
    content_list = list()
    for content in contents:
        try:
            content_list.append(BeautifulSoup(content, 'html.parser').select('img')) # 게시글 내용에서 img 태그 추출
        except:
            content_list.append(None)
    content_list = sum(list(filter(lambda v: v, content_list)), []) # 2차원 리스트 1차원으로 변경
    img_list = list()
    if content_list:
        for content in content_list:
            img_list.append(content['src'].split('.com/')[1])  # 게시글 내용에서 이미지 링크 따기
    if bool: # 일반 이미지 삭제
        img_list = img_list
    else:
        new_list = set(get_S3_image_data()) - set(img_list)
        img_list = list(new_list) # 남는 데이터 리스트
    if len(img_list) == 0:
        pass
    else:
        try:
            client = boto3.client('s3', aws_access_key_id=ACCESS_KET_ID,
                                  aws_secret_access_key=SECRET_ACCESS_KEY)
            client.delete_objects(
                Bucket='poty',
                Delete={
                    'Objects': [{'Key': key} for key in img_list]
                })
        except Exception as e:
            print(e)
            pass
```

* Django summernote는 글을 등록하지 않아도 이미지를 올리면 바로 Rout53 이미지 서버에 올라간다. 따라서 글작성 등록이 아닌 취소시 이미지는 그대로 서버에 남아있게된다.
* 이러한 문제를 보완하기 위해 취소 버튼 클릭 시 글작성에 있는 이미지를 이미지 서버에서 찾아 삭제한다.
* 하지만 이미지를 백스페이스로 지우거나 summernote 기능으로 지우면 이미지는 서버에 그대로 남아있게 된다.
* 따라서 남아 있는 이미지를 삭제하기 위해 Django-crontab을 활용하여 매일 00시 30분에 전날 이미지 서버와 RDS의 이미지를 비교하여 삭제한다.
