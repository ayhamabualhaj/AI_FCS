from django.shortcuts import get_object_or_404
from core.models.campaign import Campaign
from core.flows.content_pipeline.flow import ContentPipelineFlow


class PipelineService:
    @staticmethod
    def resolve_campaign(campaign_id=None, campaign_name=None) -> Campaign:
        if campaign_id:
            return get_object_or_404(Campaign, id=campaign_id)
        elif campaign_name:
            return get_object_or_404(Campaign, title=campaign_name)
        raise ValueError("Must provide either campaign_id or campaign_name.")

    @staticmethod
    def run(campaign, topic: str):
        """Runs the full CrewAI flow (Agent 1 -> Agent 2) and persists results."""
        try:
            flow = ContentPipelineFlow()
            # Kickoff using the database mode you set up in the flow
            flow.kickoff(campaign_id=campaign.id, topic=topic, persist=True)

            return PipelineService.latest(campaign)
        except Exception as e:
            raise ValueError(f"Full pipeline failed: {str(e)}")

    @staticmethod
    def latest(campaign):
        """Fetch the latest stored post results for this campaign."""
        return campaign.posts.order_by('-generated_at').first()