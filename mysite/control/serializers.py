from rest_framework import serializers
from .models import *
from polls.serializers import TrainingApparatusSerializer


class ControlTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlTest
        fields = '__all__'


class TestGroupConstructorSerializer(serializers.ModelSerializer):
    tests = TrainingApparatusSerializer(many=True, read_only=True)
    class Meta:
        model = TestGroupConstructor
        fields = '__all__'


class UserTestGroupSerializer(serializers.ModelSerializer):
    constructor = TestGroupConstructorSerializer(read_only=True)
    is_complete = serializers.ReadOnlyField()
    class Meta:
        model = UserTestGroup
        fields = '__all__'


