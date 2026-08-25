"""DRF serializers for the FCS models and the AI action endpoints."""
from rest_framework import serializers

from core.models import (
    Brand,
    Campaign,
    FacebookPost,
    PostImage,
)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "description", "voice_guidelines", "created_at"]
        read_only_fields = ["id", "created_at"]

class CampaignSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)

    class Meta:
        model = Campaign
        fields = [
            "id",
            "brand",
            "brand_name",
            "title",
            "objective",
            "target_audience",
            "Keywords",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_Keywords(self, value):
        """Keywords must be a list of strings."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Keywords must be a list of strings.")
        return value
    def validate_keywords(self, value):
        """keywords must be a list of strings."""
        if not isinstance(value, list):
            raise serializers.ValidationError("keywords must be a list of strings.")
        return value

class FacebookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = [
            "id",
            "campaign",
            "topic",
            "caption",
            "hashtags",
            "call_to_action",
            "image_prompt",
            "raw_report",
            "generated_at",
        ]
        read_only_fields = fields

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = [
            "id",
            "post",
            "prompt_used",
            "image_file",
            "provider",
            "model",
            "generated_at",
        ]
        read_only_fields = fields

class WritePostActionSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField()
    topic = serializers.CharField(max_length=255)