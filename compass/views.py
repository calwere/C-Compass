from django.shortcuts import render

# For AJAX requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse

# for distance
from geopy.distance import distance

from .models import House, Amenity, Agent, SearchHistory, Mover
from .serializers import HouseSerializer, AmenitySerializer, AgentSerializer, SearchHistorySerializer, MoverSerializer


class MapView(TemplateView):
    template_name = 'base.html'

class HouseList(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

class HouseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

class MoverList(generics.ListAPIView):
    queryset = Mover.objects.all()
    serializer_class = MoverSerializer

class AmenityList(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

class AgentList(generics.ListCreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class SearchHistoryList(generics.ListCreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


@api_view(['GET'])
def house_search(request):
    search_query = request.query_params.get('query', '')
    houses = House.objects.filter(Q(name__icontains=search_query) | Q(address__icontains=search_query))
    serializer = HouseSerializer(houses, many=True)
    SearchHistory.objects.create(user=request.user, query=search_query)
    return Response(serializer.data)

@api_view(['GET'])
def calculate_moving_charges(request, house_id):
    house = House.objects.get(id=house_id)
    # your moving charges calculation logic here
    return Response({'moving_charges': 100})

@api_view(['GET'])
def get_nearby_amenities(request):
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    amenities = Amenity.objects.filter(latitude=latitude, longitude=longitude)
    serializer = AmenitySerializer(amenities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List Movers': '/mover-list/',
        'List Agents': '/agent-list/',
        'List Amenities': '/amenity-list/',
        'List Houses': '/house-list/',
        'House Detail': '/house-detail/<str:pk>/',
        'Create House': '/house-create/',
        'Update House': '/house-update/<str:pk>/',
        'Delete House': '/house-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def houseList(request):
    houses = House.objects.all()
    serializer = HouseSerializer(houses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def houseDetail(request, pk):
    houses = House.objects.get(id=pk)
    serializer = HouseSerializer(houses, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def houseCreate(request):
    serializer = HouseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def houseUpdate(request, pk):
    house = House.objects.get(id=pk)
    serializer = HouseSerializer(instance=house, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def houseDelete(request, pk):
    house = House.objects.get(id=pk)
    house.delete()

    return Response('House deleted')

@api_view(['GET'])
def amenityList(request):
    amenities = Amenity.objects.all()
    serializer = AmenitySerializer(amenities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def agentList(request):
    agents = Agent.objects.all()
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def moverList(request):
    movers = Mover.objects.all()
    serializer = MoverSerializer(movers, many=True)
    return Response(serializer.data)



# calculating distance between current location and preferred house

def house_detail(request, pk):
    house = House.objects.get(pk=pk)
    user_location = request.GET.get('location')
    if user_location:
        # Calculate distance between user's location and house location
        house_location = (house.latitude, house.longitude)
        user_location = tuple(map(float, user_location.split(',')))
        house_distance = distance(house_location, user_location).km

        # Estimate moving charges
        movers = Mover.objects.all()
        moving_charges = []
        for mover in movers:
            distance_to_mover = distance(house_location, (mover.latitude, mover.longitude)).km
            moving_charges.append({
                'mover': mover.name,
                'charges': mover.base_charge + (distance_to_mover * mover.charge_per_km)
            })
        moving_charges = sorted(moving_charges, key=lambda x: x['charges'])

        # Link user to movers
        mover_links = []
        for mover in moving_charges:
            mover_links.append({
                'mover': mover['mover'],
                'link': mover['link']
            })

        return JsonResponse({
            'name': house.name,
            'location': house.location,
            'price': house.price,
            'description': house.description,
            'amenities': [amenity.name for amenity in house.amenities.all()],
            'distance': house_distance,
            'moving_charges': moving_charges,
            'mover_links': mover_links
        })
    else:
        return render(request, 'house_detail.html', {'house': house})
    
    