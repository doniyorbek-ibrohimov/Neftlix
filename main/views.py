from http.client import responses

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.generics import get_object_or_404

from .models import *
from .serializers import *

class ActorsAPIView(APIView):
    def get(self,request):
        actors=Actor.objects.all()
        serializer=ActorSerializer(actors,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ActorSerializer(data=request.data)
        if serializer.is_valid():
            Actor.objects.create(
                name=serializer.validated_data.get('name'),
                country=serializer.validated_data.get('country'),
                gender=serializer.validated_data.get('gender'),
                birthdate=serializer.validated_data.get('birthdate'),
            )
            response={
                'success':True,
                'message': 'Actor created successfully',
                'data':serializer.data
            }
            return Response(response,status=HTTP_201_CREATED)
        response={
            'success':False,
            'error':serializer.errors,
        }
        return Response(response,status=HTTP_400_BAD_REQUEST)

class ActorRetrieveAPIView(APIView):
    def get(self,request,pk):
        actor=get_object_or_404(Actor,pk=pk)
        serializer=ActorSerializer(actor)
        return Response(serializer.data)

    def put(self,request,pk):
        actor=get_object_or_404(Actor,pk=pk)
        serializer=ActorSerializer(actor,data=request.data)
        if serializer.is_valid():
            actor.name=serializer.validated_data.get('name')
            actor.country=serializer.validated_data.get('country')
            actor.gender=serializer.validated_data.get('gender')
            actor.birthdate=serializer.validated_data.get('birthdate')
            actor.save()
            response={
                'success':True,
                'message':'Update successfully',
                'data': serializer.data
            }
            return Response(response,status=HTTP_200_OK)
        response={
            'success':False,
            'error': serializer.errors
        }
        return Response(response,HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        actor=get_object_or_404(Actor,pk=pk)
        actor.delete()
        response={
            'success':True,
            'message':'Actor deleted successfully'
        }
        return Response(response,status=HTTP_204_NO_CONTENT)

class SubAPIView(APIView):
    def get(self,request):
        subs=Subscription.objects.all()
        serializer=SubSerializer(subs,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=SubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'success':True,
                'message':'Subscription added successfully',
                'data':serializer.data
            }
            return Response(response,status=HTTP_201_CREATED)
        response={
            'success':False,
            'error':serializer.errors
        }
        return Response(response,status=HTTP_400_BAD_REQUEST)

class SubRetrieveAPIView(APIView):
    def get(self,request,pk):
        sub=get_object_or_404(Subscription,pk=pk)
        serializer=SubSerializer(sub)
        return Response(serializer.data)

    def put(self,request,pk):
        sub=get_object_or_404(Subscription,pk=pk)
        serializer=SubSerializer(sub,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'success':True,
                'message':'Subscription updated successfully',
                'data': serializer.data
            }
            return Response(response,status=HTTP_200_OK)
        response={
            'success':False,
            'error':serializer.errors
        }
        return Response(response,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        sub=get_object_or_404(Subscription,pk=pk)
        sub.delete()
        response={
            'success':True,
            'message':"Subscription deleted successfully"
        }
        return Response(response,status=HTTP_204_NO_CONTENT)



