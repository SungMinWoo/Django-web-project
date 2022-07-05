from django.urls import path, include
from .views import post_write, post_list, post_detail, post_delete, post_update, post_likes, \
    post_dislikes, reply_likes, reply_dislikes, reply_delete, reply_update, post_search, check_img

app_name = 'board'

urlpatterns = [
    path('<board_type>', post_list, name='board'),
    path('board/<board_type>/search', post_search, name='post_search'),
    path('board_write/<board_type>', post_write, name='board_write'),
    path('board_detail/<int:pk>', post_detail, name='post_detail'),
    path('board_detail/<int:pk>/delete', post_delete, name='post_delete'),
    path('board_detail/<int:pk>/modify', post_update, name='post_update'),
    path('board_detail/<int:pk>/post_likes/', post_likes, name='post_likes'),
    path('board_detail/<int:pk>/post_dislikes/', post_dislikes, name='post_dislikes'),
    path('board_detail/<int:pk>/reply_delete/<int:id>', reply_delete, name='post_delete'),
    path('board_detail/<int:pk>/reply_update/<int:id>', reply_update, name='post_delete'),
    path('board_detail/<int:pk>/reply_likes/', reply_likes, name='reply_likes'),
    path('board_detail/<int:pk>/reply_dislikes/', reply_dislikes, name='reply_dislikes'),
    path('board_write/api/check-img/', check_img, name='check_value'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [path('summernote/', include('django_summernote.urls'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
