from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models.facebook_post import FacebookPost
from core.models.post_image import PostImage
from core.serializers import (
    BrandSerializer,
    CampaignSerializer,
    FacebookPostSerializer,
    PostImageSerializer
)

class BrandCreateView(APIView):
    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CampaignCreateView(APIView):
    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    def get(self, request, pk):
        post_instance = get_object_or_404(FacebookPost, pk=pk)
        serializer = FacebookPostSerializer(post_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostImageDetailView(APIView):
    def get(self, request, pk):
        image_instance = get_object_or_404(PostImage, pk=pk)
        serializer = PostImageSerializer(image_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)