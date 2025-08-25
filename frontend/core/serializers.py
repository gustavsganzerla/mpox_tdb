from rest_framework import serializers
from .models import CSSR, ISSR, SSR, VNTR

class CSSRModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSSR
        fields = '__all__'


class ISSRModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISSR
        fields = '__all__'


class SSRModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSR
        fields = '__all__'

class VNTRModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VNTR
        fields = '__all__'
