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


class ActorForMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        fields=("name",)


class MovieSafeSerializer(serializers.ModelSerializer):
    # actors=ActorForMovieSerializer(many=True,read_only=True)
    actors=serializers.SerializerMethodField()


    class Meta:
        model=Movie
        fields=('id','name','genre','year','actors')

    def get_actors(self,obj):
        return[actor.name for actor in obj.actors.all()]





class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscription
        fields="__all__"


class MovieStatisticsSerializer(serializers.Serializer):
    title=serializers.CharField()
    actors_amount=serializers.IntegerField()
    reviews_amount=serializers.IntegerField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"


