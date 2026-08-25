import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models.facebook_post import FacebookPost
from core.serializers import WritePostActionSerializer, FacebookPostSerializer, PostImageSerializer
from core.services.post_writer_service import PostWriterService
from core.services.image_generation_service import ImageGenerationService
from core.services.pipeline_service import PipelineService

logger = logging.getLogger(__name__)


class WritePostView(APIView):
    def post(self, request):
        serializer = WritePostActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            campaign = PipelineService.resolve_campaign(campaign_id=serializer.validated_data['campaign_id'])
            post_instance = PostWriterService.run(campaign, serializer.validated_data['topic'])
            return Response(FacebookPostSerializer(post_instance).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in WritePostView: {str(e)}", exc_info=True)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateImageView(APIView):
    def post(self, request, pk):
        post_instance = get_object_or_404(FacebookPost, pk=pk)
        try:
            image_instance = ImageGenerationService.run(post_instance)
            return Response(PostImageSerializer(image_instance).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in GenerateImageView: {str(e)}", exc_info=True)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RunPipelineView(APIView):
    def post(self, request):
        serializer = WritePostActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            campaign = PipelineService.resolve_campaign(campaign_id=serializer.validated_data['campaign_id'])
            post_instance = PipelineService.run(campaign, serializer.validated_data['topic'])
            return Response(FacebookPostSerializer(post_instance).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in RunPipelineView: {str(e)}", exc_info=True)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







