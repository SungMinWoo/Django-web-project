from django.shortcuts import render

from politic_info.models import Rating
from board.models import Board
from politic_info.models import Politic
from public_function.public_func import paginator_func, top_post
from public_function.decorator import block_ip
from public_function.public_data import BLOCK_TIME, IP

from django.db.models import Q, F, Count, Avg
from ratelimit.decorators import ratelimit


# 메인 페이지
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def main_page(request):
    if request.method == 'GET':
        rating_list = Rating.objects.all().order_by('-create')[:5]
        notice = Board.objects.filter(board_id='notice')[:3]
        board_free_list = top_post('free')
        board_oppo_list = top_post('oppo')
        board_rul_list = top_post('rul')
        return render(request, 'main_page/main_page.html', {'rating_list': rating_list,
                                                            'board_free_list':board_free_list,
                                                            'board_oppo_list':board_oppo_list,
                                                            'board_rul_list':board_rul_list,
                                                            'notice':notice})

# 전체 검색
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def search_all(request):
    keyword = request.GET.get('search')

    board = Board.objects.exclude(board_id='notice').filter(Q(post_title__icontains=keyword) | Q(post_content__icontains=keyword)).annotate(
        reply_count=Count(F('reply')))[::-1]
    board = paginator_func(request, board, 10)

    categories = Politic.objects.filter(Q(poli_nm__icontains=keyword))[:5]
    poli_list = list()
    for category in categories:
        politic = Rating.objects.filter(politic=category)
        count = politic.aggregate(Count('rate'))
        avg = politic.aggregate(Avg('rate'))
        poli_list.append({'list': category, 'count': count, 'avg': avg})

    return render(request, 'main_page/search.html', {'keyword':keyword, 'board':board, 'politic': poli_list})



