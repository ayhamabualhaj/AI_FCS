from django.urls import path
from .views.crud import (
    BrandCreateView, CampaignCreateView,
    PostDetailView, PostImageDetailView
)
from .views.ai_actions import (
    WritePostView, GenerateImageView, RunPipelineView
)

urlpatterns = [
    # CRUD Endpoints
    path('brands/', BrandCreateView.as_view(), name='brand-create'),
    path('campaigns/', CampaignCreateView.as_view(), name='campaign-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-images/<int:pk>/', PostImageDetailView.as_view(), name='post-image-detail'),

    # AI Action Endpoints
    path('posts/write/', WritePostView.as_view(), name='post-write'),
    path('posts/<int:pk>/image/', GenerateImageView.as_view(), name='generate-image'),
    path('pipeline/run/', RunPipelineView.as_view(), name='run-pipeline'),
]