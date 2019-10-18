"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from backend import views  # Import our views.py file.
from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token

# from .views import index

urlpatterns = [
    # path('', index, name='index'),
    # path('admin/', admin.site.urls),
    # path('api/it/', csrf_exempt(views.ApiView.as_view())),

    path('api/song_search/', requires_csrf_token(views.SongView.as_view())),
    # path('api/song_search/', csrf_exempt(views.SongView.as_view())),

    path('api/song_analyze/', requires_csrf_token(views.AnalyzeView.as_view())),
    # path('api/song_analyze/', csrf_exempt(views.AnalyzeView.as_view())),
    

    url(r'^', views.FrontendAppView.as_view()) # This is a catch-all for React.
]
