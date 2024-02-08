from rest_framework import serializers
from .models import *
from datetime import datetime


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):

        # instance.car_number = validated_data.get('car_number', instance.car_number)
        instance.parking_status = validated_data.get('parking_status', instance.parking_status)
        instance.exit_date = datetime.now()
        instance.modified_user = validated_data.get('modified_user', instance.modified_user)
        instance.save()
        return instance


class TransactionDetailSerializer(serializers.ModelSerializer):
    # created_user = serializers.ReadOnlyField(source='created_user.username')
    # modified_user = serializers.ReadOnlyField(source='modified_user.username')
    parking_status = serializers.SerializerMethodField()
    created_user = serializers.SerializerMethodField()
    modified_user = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['car_number', 'parking_status', 'entry_date', 'exit_date', 'created_user', 'modified_user']

    def get_parking_status(self, obj):
        return obj.get_parking_status_display()

    def get_created_user(self, obj):
        if obj.created_user:
            return obj.created_user.username
        else:
            return None

    def get_modified_user(self, obj):
        if obj.modified_user:
            return obj.modified_user.username
        else:
            return None
