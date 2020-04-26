from rest_framework import serializers
from .models import TrainingTest, TrainingApparatus, Exercise
from .helper import *
import datetime

class TrainingApparatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingApparatus
        fields = "__all__"

# class TimestampField(serializers.Field):
#     def to_native(self, value):
#         epoch = datetime.datetime(1970,1,1)
#         return int((value - epoch).total_seconds())

class ExerciseSerializer(serializers.ModelSerializer):
    spent_timestamp = serializers.IntegerField(source='get_spent_timestamp')
    class Meta:
        model = Exercise
        fields = '__all__'

class TrainingTestSerializer(serializers.ModelSerializer):
    apparatus = TrainingApparatusSerializer()
    exercises = ExerciseSerializer(many=True, read_only=True)
    # time_start = TimestampField()
    class Meta:
        model = TrainingTest
        fields = '__all__'