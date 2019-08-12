"""chart_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chart'
urlpatterns = [
     # ex: /polls/
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('home', views.home, name='home'),
    path('success/', views.success, name='success'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('chart/<int:file_id>/<str:type>', views.chart, name='chart'),
    path('data/<int:file_id>/', views.chart_data, name='data'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
