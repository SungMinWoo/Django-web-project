from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.db.models import Q

from public_function.public_func import paginator_func
from public_function.decorator import block_ip, login_required
from public_function.public_data import BLOCK_TIME, IP

from ratelimit.decorators import ratelimit
import json

from .models import Politic, Rating
from accounts.models import User


# 정치인 검색
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_list(request, categories, keyword): # 검색 결과 함수
    if keyword: # 키워드가 있다면
        question_list = categories.filter(
            Q(poli_nm__icontains=keyword)
        ).distinct() # 키워드에 대한 검색 결과 poli_nm이 포함된 키워드

        if len(question_list) == 0:
            message = keyword + '로 검색된 결과가 없습니다.'
            politic_list = None
        else:
            poli_list = list()
            for question in question_list:
                politic = Rating.objects.filter(politic=question)
                count = politic.aggregate(Count('rate'))
                avg = politic.aggregate(Avg('rate'))
                poli_list.append({'list': question, 'count': count, 'avg': avg})
            politic_list = paginator_func(request, poli_list)
            message = keyword + ' 검색 결과입니다.'
        poli_info = {
            'politic_list': politic_list,
            'message': message,
        }
    else: # 키워드가 없다면
        message = '검색어를 입력해주세요'
        poli_info = {
            'message': message,
        }

    return poli_info


# 여당 정치인 리스트
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def oppo_politic_list(request):
    categories = Politic.objects.filter(party_af='국민의힘').order_by('poli_nm')
    if request.method == 'GET':
        poli_list = list()
        for category in categories:
            politic = Rating.objects.filter(politic=category)
            count = politic.aggregate(Count('rate'))
            avg = politic.aggregate(Avg('rate'))
            poli_list.append({'list':category, 'count':count, 'avg':avg})

        politic_list = paginator_func(request, poli_list)
        return render(request, 'list/oppo_politic_list.html', {'politic_list': politic_list})
    elif request.method == 'POST':
        keyword = request.POST['keyword']
        return render(request, 'list/oppo_politic_list.html', post_list(request, categories, keyword))


# 야당 정치인 리스트
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def rul_politic_list(request):
    categories = Politic.objects.exclude(party_af='국민의힘').order_by('poli_nm') # 최대한 적게 ORM을 쓰기 위해 미리 불러옴
    if request.method == 'GET':
        poli_list = list()
        for category in categories:
            politic = Rating.objects.filter(politic=category)
            count = politic.aggregate(Count('rate'))
            avg = politic.aggregate(Avg('rate'))
            poli_list.append({'list': category, 'count': count, 'avg': avg})
        politic_list = paginator_func(request, poli_list)
        return render(request, 'list/rul_politic_list.html', {'politic_list': politic_list})
    elif request.method == 'POST':
        keyword = request.POST['keyword']
        return render(request, 'list/rul_politic_list.html', post_list(request, categories, keyword))


# 정치인 세부 내용
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def politic_detail(request, id, politic_slug=None): # detail 페이지로 이동
    if request.method == 'GET':
        politic = get_object_or_404(Politic, id=id, politic_slug=politic_slug)
        politic_name = Politic.objects.get(poli_nm=politic_slug)
        info = Rating.objects.filter(politic=politic_name)
        list_info = paginator_func(request, info)

        count = info.aggregate(Count('rate'))
        avg = info.aggregate(Avg('rate'))

        return render(request, 'information/detail.html', {'politic':politic, 'politic_list':list_info, 'avg':avg, 'count':count})
    elif request.method == 'POST': # 평점 최신/추천/비추천순 정렬
        if request.POST.get('choice'):
            value = request.POST.get('choice')
            politic = get_object_or_404(Politic, id=id, politic_slug=politic_slug)
            politic_name = Politic.objects.get(poli_nm=politic_slug)
            if value == 'new':
                info = Rating.objects.filter(politic=politic_name)
            elif value == 'most_like':
                info = Rating.objects.filter(politic=politic_name).annotate(num_like=Count('like')).order_by('-num_like')
            elif value == 'most_dislike':
                info = Rating.objects.filter(politic=politic_name).annotate(num_dislike=Count('dislike')).order_by('-num_dislike')

            list_info = paginator_func(request, info)
            count = info.aggregate(Count('rate'))
            avg = info.aggregate(Avg('rate'))
            return render(request, 'information/detail.html', {'politic': politic, 'politic_list': list_info, 'avg': avg, 'count': count, 'select':value})
        else:
            text = request.POST.get('text_msg')
            rating = request.POST.get('rating') # .get은 여러 name의 값을 받을때 사용하면되는듯(multiple values error)
            if not rating:
                rating = 0
            user_nk = request.session.get('authUser')['nickname']

            user_nk = User.objects.get(nickname=user_nk) # fk 값을 저장할때는 그 데이터베이스에서 찾아서 저장해야되는듯
            politic_name = Politic.objects.get(poli_nm=politic_slug)

            save_rating = Rating(
                politic=politic_name,
                user_nk=user_nk,
                rate=rating,
                review=text,
            )
            save_rating.save()

            return redirect('politic:politic_detail', id, politic_slug) #페이지 redirect시 정보 넘겨주기


# 평점 남기기
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def check_value(request, id, politic_slug=None): # 평점 남기기 버튼 비활성화 기능
    if not request.session.get('authUser'):
        search = 'exist'
    elif request.session.get('authUser'):
        user_nk = request.session.get('authUser')['nickname']
        politic_name = Politic.objects.get(
            poli_nm=politic_slug)  # 그냥 pk를 검색하면 오류 걸려서 기존 필드에서 검색 후 검색해야함

        search = Rating.objects.filter(user_nk=user_nk, politic=politic_name)
        if len(search) == 0:
            search = 'success'
        else:
            search = 'exist'
    result = {
        'data': search,
    }
    return JsonResponse(result)


# 평점 좋아요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def likes(request, id, politic_slug=None):
    review_id = request.GET['review_id']

    post = Rating.objects.get(rate_num=review_id)

    if not request.session.get('authUser'):
        message = '로그인 후 이용 바랍니다.'
        context = {'like_count': post.like.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')
    else:
        user = request.session.get('authUser')['user_id']
        if post.dislike.filter(user_id=user).exists():
            post.dislike.remove(user)
            post.like.add(user)
            message = '낙선 취소'
        elif post.like.filter(user_id=user).exists():  # 이미 좋아요를 누른 유저일 때
            post.like.remove(user)  # like field에 현재 유저 추가
            message = '당선 취소'  # 화면에 띄울 메세지
        else:  # 좋아요를 누르지 않은 유저일 때
            post.like.add(user)  # like field에 현재 유저 삭제
            message = '당선!'  # 화면에 띄울 메세지
            # post.like.count() : 게시물이 받은 좋아요 수
        context = {'like_count': post.like.count(), 'dislike_count': post.dislike.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')


# 평점 실어요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def dislikes(request, id, politic_slug=None):
    review_id = request.GET['review_ids']
    print(review_id)
    post = Rating.objects.get(rate_num=review_id)

    if not request.session.get('authUser'):
        message = '로그인 후 이용 바랍니다.'
        context = {'dislike_count': post.dislike.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')
    else:
        user = request.session.get('authUser')['user_id']
        if post.like.filter(user_id=user).exists():  # 이미 좋아요를 누른 유저일 때
            post.like.remove(user)  # like field에 현재 유저 추가
            post.dislike.add(user)
            message = '당선 취소'  # 화면에 띄울 메세지
        elif post.dislike.filter(user_id=user).exists():  # 이미 좋아요를 누른 유저일 때
            post.dislike.remove(user)  # like field에 현재 유저 추가
            message = '낙선 취소'  # 화면에 띄울 메세지
        else:  # 좋아요를 누르지 않은 유저일 때
            post.dislike.add(user)  # like field에 현재 유저 삭제
            message = '낙선'  # 화면에 띄울 메세지
            # post.like.count() : 게시물이 받은 좋아요 수
        context = {'like_count': post.like.count(), 'dislike_count': post.dislike.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')


# 평점 삭제
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def delete(request, id, politic_slug=None, pk=None):
    session = request.session.get('authUser')
    rating = Rating.objects.get(rate_num=pk)
    if rating.user_nk.nickname == session['nickname']:
        rating.delete()
        return redirect('politic:politic_detail', id, politic_slug)
    else: # url을 통해 강제로 삭제 시 해당페이지로 다시 보냄
        return redirect('politic:politic_detail', id, politic_slug)