# from http.client import responses
#
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.status import *
# from rest_framework.generics import get_object_or_404
#
# from .models import *
# from .serializers import *
#
# class ActorsAPIView(APIView):
#     def get(self,request):
#         actors=Actor.objects.all()
#         serializer=ActorSerializer(actors,many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer=ActorSerializer(data=request.data)
#         if serializer.is_valid():
#             Actor.objects.create(
#                 name=serializer.validated_data.get('name'),
#                 country=serializer.validated_data.get('country'),
#                 gender=serializer.validated_data.get('gender'),
#                 birthdate=serializer.validated_data.get('birthdate'),
#             )
#             response={
#                 'success':True,
#                 'message': 'Actor created successfully',
#                 'data':serializer.data
#             }
#             return Response(response,status=HTTP_201_CREATED)
#         response={
#             'success':False,
#             'error':serializer.errors,
#         }
#         return Response(response,status=HTTP_400_BAD_REQUEST)
#
# class ActorRetrieveAPIView(APIView):
#     def get(self,request,pk):
#         actor=get_object_or_404(Actor,pk=pk)
#         serializer=ActorSerializer(actor)
#         return Response(serializer.data)
#
#     def put(self,request,pk):
#         actor=get_object_or_404(Actor,pk=pk)
#         serializer=ActorSerializer(actor,data=request.data)
#         if serializer.is_valid():
#             actor.name=serializer.validated_data.get('name')
#             actor.country=serializer.validated_data.get('country')
#             actor.gender=serializer.validated_data.get('gender')
#             actor.birthdate=serializer.validated_data.get('birthdate')
#             actor.save()
#             response={
#                 'success':True,
#                 'message':'Update successfully',
#                 'data': serializer.data
#             }
#             return Response(response,status=HTTP_200_OK)
#         response={
#             'success':False,
#             'error': serializer.errors
#         }
#         return Response(response,HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         actor=get_object_or_404(Actor,pk=pk)
#         actor.delete()
#         response={
#             'success':True,
#             'message':'Actor deleted successfully'
#         }
#         return Response(response,status=HTTP_204_NO_CONTENT)
#
# class SubAPIView(APIView):
#     def get(self,request):
#         subs=Subscription.objects.all()
#         serializer=SubSerializer(subs,many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer=SubSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response={
#                 'success':True,
#                 'message':'Subscription added successfully',
#                 'data':serializer.data
#             }
#             return Response(response,status=HTTP_201_CREATED)
#         response={
#             'success':False,
#             'error':serializer.errors
#         }
#         return Response(response,status=HTTP_400_BAD_REQUEST)
#
# class SubRetrieveAPIView(APIView):
#     def get(self,request,pk):
#         sub=get_object_or_404(Subscription,pk=pk)
#         serializer=SubSerializer(sub)
#         return Response(serializer.data)
#
#     def put(self,request,pk):
#         sub=get_object_or_404(Subscription,pk=pk)
#         serializer=SubSerializer(sub,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response={
#                 'success':True,
#                 'message':'Subscription updated successfully',
#                 'data': serializer.data
#             }
#             return Response(response,status=HTTP_200_OK)
#         response={
#             'success':False,
#             'error':serializer.errors
#         }
#         return Response(response,status=HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk):
#         sub=get_object_or_404(Subscription,pk=pk)
#         sub.delete()
#         response={
#             'success':True,
#             'message':"Subscription deleted successfully"
#         }
#         return Response(response,status=HTTP_204_NO_CONTENT)
#
#
#
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import *
from rest_framework.decorators import action

from .models import *
from .serializers import *


class ActorModelViewSet(ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    search_fields=['name']
    filterset_fields=['country','gender']
    ordering_fields=['name','birthdate']
    ordering=['name']




class MovieModelViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ['actors', 'add_actor']:
            return ActorSerializer
        elif self.action in ('list', 'retrieve'):
            return MovieSafeSerializer
        return MovieSerializer

    @action(detail=True, methods=['get'])
    def actors(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        actors = Actor.objects.filter(movie=movie)
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="add-actor")
    def add_actor(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            actor = serializer.save()
            movie.actors.add(actor)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        actors_amount = movie.actors.count()
        reviews_amount = movie.review_set.count()
        serializer = MovieStatisticsSerializer(
            {
                'title': movie.name,
                'actors_amount': actors_amount,
                'reviews_amount': reviews_amount,
            }
        )
        return Response(serializer.data)



class ReviewFilter(django_filters.FilterSet):
    min_rate=django_filters.NumberFilter(field_name='rate',lookup_expr='gte')
    max_rate=django_filters.NumberFilter(field_name='rate',lookup_expr='lte')

    class Meta:
        model=Review
        fields=['user','movie']



class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    search_fields=['user__name']
    filterset_class=ReviewFilter
    ordering_fields=['rate','created_at']

class RegisterAPIView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action=='post':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise serializers.ValidationError("You are not allowed!")
        instance.delete()




def example_view(request):
    return render(request,'example.html')


