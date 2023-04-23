"""castle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import path, include
from compass.views import HouseList, HouseDetail, AmenityList, AgentList, SearchHistoryList

urlpatterns = [
    path('houses/', HouseList.as_view(), name='house-list'),
    path('', include('compass.urls')),
    path('admin/', admin.site.urls),
    path('houses/<int:pk>/', HouseDetail.as_view(), name='house-detail'),
    path('amenities/', AmenityList.as_view(), name='amenity-list'),
    path('agents/', AgentList.as_view(), name='agent-list'),
    # path('agents/<int:pk>/', AgentDetail.as_view(), name='agent-detail'),
    path('search-history/', SearchHistoryList.as_view(), name='search-history-list'),
    # path('users/', UserList.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    
]
