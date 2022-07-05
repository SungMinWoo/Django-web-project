from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Count

from ratelimit.exceptions import Ratelimited
from django.utils import timezone

from config.secret_keys import SECRET_ACCESS_KEY, ACCESS_KET_ID
from ipware.ip import get_client_ip
from datetime import timedelta
from bs4 import BeautifulSoup
import boto3

from board.models import Board


# 에러 핸들러
def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry you are blocked', status=429)
    return HttpResponseForbidden('')


def handler500(request, *args, **argv):
    return HttpResponseForbidden('<h3>잘못된 요청입니다.</h3><h6>자세한 사항은 문의바랍니다.</h6>')


def handler400(request, *args, **argv):
    return HttpResponseForbidden('<h3>잘못된 요청입니다.</h3><h6>자세한 사항은 문의바랍니다.</h6>')


def handler404(request, *args, **argv):
    return HttpResponseForbidden('<h3>없는 페이지 입니다.</h3>')


# 창이면 앞에 값을 넣고 뒷 값을 가져옴
def divide_board(value, bool):
    new_value = str()
    type_dict = {'rul_free': '여당-자유게시판', 'rul_politic': '여당-정치게시판', 'rul_issue': '여당-시사,이슈게시판'
        , 'oppo_free': '야당-자유게시판', 'oppo_politic': '야당-정치게시판', 'oppo_issue': '야당-시사,이슈게시판'
        , 'free_free': '자유-자유게시판', 'free_politic': '자유-정치게시판', 'free_issue': '자유-시사,이슈게시판'
        , 'notice': '공지사항'}
    if bool:
        new_value = type_dict[value]
    elif not bool:
        new_dict = dict(map(reversed, type_dict.items()))
        new_value = new_dict[value]
    return new_value


# 좋아요 상위 5
def top_post(keyword):
    data_list = Board.objects.filter(post_create__gt=timezone.now() - timedelta(days=8)).filter(board_id__startswith=keyword).annotate(num_like=Count('post_like')).filter(num_like__gte=1).order_by('-num_like')[:5]

    count = 0
    for data in data_list:  # 게시판 이름 바꾸기
        data_list[count].board_id = divide_board(data.board_id, True)
        count += 1

    return data_list


# 페이지 함수
def paginator_func(request, data, page=10): # 페이지 기능하는 함수
    try:
        paginator = Paginator(data, page) # 페이지별로 보여줄 최대 데이터 개수
        page = request.GET.get('page')  # Get 요청시 page 파라미터를 읽음
        paginator_list = paginator.get_page(page)
    except:
        paginator_list = data
    return paginator_list


# AWS 이미지 삭제
def delete_img_s3(contents, bool=True):
    content_list = list()
    for content in contents:
        try:
            content_list.append(BeautifulSoup(content, 'html.parser').select('img'))
        except:
            content_list.append(None)
    content_list = sum(list(filter(lambda v: v, content_list)), []) # 2차원 리스트 1차원으로 변경

    img_list = list()
    if content_list:
        for content in content_list:
            img_list.append(content['src'].split('.com/')[1])  # 이미지 링크 따기

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


# AWS s3에서 전날 이미지 데이터 가지고 오기
def get_S3_image_data():
    client = boto3.client('s3', aws_access_key_id=ACCESS_KET_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)
    date = timezone.localtime() - timedelta(days=1)
    date = date.strftime('%Y-%m-%d')

    test = client.list_objects_v2(Bucket='poty', Prefix='media/django-summernote/' + date + '/') # 하루 전 파일 가져오기
    img_name_list = list()
    for content in test.get('Contents', []): # 버킷 폴더에서 파일 가져오기
        img_name_list.append(content['Key'])
    return img_name_list
