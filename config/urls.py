"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from public_function.public_func import handler403, handler500, handler400, handler404
from public_function.decorator import block_ip


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('politic/', include('politic_info.urls')),
    path('board/', include('board.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('main_page.urls')),
    path('robots.txt',  TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    # path('/$', block_ip(), 'name_of_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler403 = handler403
handler404 = handler404
handler500 = handler500
handler400 = handler400

