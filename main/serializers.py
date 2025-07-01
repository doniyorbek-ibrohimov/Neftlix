from rest_framework import serializers

from main.models import *



class ActorSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    country=serializers.CharField()
    gender=serializers.CharField()
    birthdate=serializers.DateField()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields="__all__"


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscription
        fields="__all__"
