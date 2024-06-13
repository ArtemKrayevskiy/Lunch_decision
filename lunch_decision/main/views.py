from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, Menu, User, Vote
from .serializers import RestaurantSerializer, MenuSerializer, UserSerializer, VoteSerializer
from django.utils import timezone


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False, methods=["post"], url_path="create-restaurant")
    def create_restaurant(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


    @action(detail=False, methods=["get"], url_path="current-day-menu")
    def current_day_menu(self, request):
        today = timezone.localdate()
        menus = Menu.objects.filter(date=today)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=["post"], url_path="upload-menu")
    def upload_menu(self, request):
        data = request.data
        restaurant_id = data.get("restaurant")
        date = data.get("date")
        items = data.get("items")

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        menu_data = {
            'restaurant': restaurant_id,
            'date': date,
            'items': items
        }

        serializer = MenuSerializer(data=menu_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=["get"], url_path="current-day-votes")
    def current_day_votes(self, request):
        today = timezone.localdate()
        votes = Vote.objects.filter(menu__date=today)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="voting", url_name="menu-vote")
    def voting(self, request):
        user = request.user

        check_existance = Vote.objects.filter(user=user, vote_date=timezone.localdate()).exists()
        if check_existance:
            return Response({'error': 'You have already voted for this menu today.'}, status=status.HTTP_400_BAD_REQUEST)

        menu_pk = request.data.get('pk')
        try:
            menu = Menu.objects.get(pk=menu_pk)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
        vote = Vote.objects.create(user=user, menu= menu)
        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], url_path="create-user")
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
