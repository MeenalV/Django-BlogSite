from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from blog.serializers import BlogSerializer


class BlogView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_writer or request.user.is_superuser:
            serialized = BlogSerializer(data=request.data, context={'request': request})
            if serialized.is_valid(raise_exception=True):
                blog = serialized.create(validated_data=request.data)
                serialized = BlogSerializer(blog)
                return Response(serialized.data, status=201)
            raise Http404
        raise PermissionDenied
