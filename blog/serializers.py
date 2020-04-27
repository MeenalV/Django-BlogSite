from rest_framework import serializers
from blog.models import Blog
from django.http import Http404


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
