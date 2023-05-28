from django.urls import path
from . import views
from .views import HouseList, HouseDetail, MoverList, AmenityList, AgentList, house_search, calculate_moving_charges, get_nearby_amenities, MapView, houseCreate, houseUpdate, houseDelete

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('houses/', HouseList.as_view(), name='house-list'),
    # path('', views.index, name='index'),
    path('', MapView.as_view(), name='map'),    
    path('houses/<int:pk>/', HouseDetail.as_view(), name='house-detail'),
    path('movers/', MoverList.as_view()),
    path('amenities/', AmenityList.as_view(), name='amenity-list'),
    path('agents/', AgentList.as_view(), name='agent-list'),
    path('search/', house_search, name='house-search'),
    path('calculate_moving_charges/<int:house_id>/', calculate_moving_charges, name='calculate-moving-charges'),
    path('get_nearby_amenities/', get_nearby_amenities, name='get-nearby-amenities'),
    path('house-create/', views.houseCreate, name="house-create"),
    path('house-update/<str:pk>/', views.houseUpdate, name="house-update"),
    path('house-delete/str:pk/', views.houseDelete, name="house-delete"),
    path('house-details/str:pk/', views.house_detail, name="house-details"),
    path('house-overview/', views.apiOverview, name="overview"),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
