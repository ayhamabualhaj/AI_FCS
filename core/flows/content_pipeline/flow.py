import requests
from crewai.flow.flow import Flow, listen, start
from django.core.files.base import ContentFile

from core.crews.post_writer_crew.crew import PostWriterCrew
from core.crews.image_generation_crew.crew import ImageGenerationCrew
from core.utils import parse_json_output
from .schema import ContentPipelineState


class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def write_post(self):
        inputs = {
            "topic": self.state.topic,
            "campaign_objective": self.state.objective,
            "target_audience": self.state.target_audience,
            "tone": self.state.tone,
            "brand_voice": self.state.brand_voice,
            "keywords": self.state.keywords
        }

        result = PostWriterCrew().crew().kickoff(inputs=inputs)
        parsed_data = parse_json_output(result.raw)
        self.state.post_output = parsed_data
        return parsed_data

    @listen(write_post)
    def generate_image(self, post_data):
        inputs = {
            "image_prompt": post_data.get("image_prompt", ""),
            "caption": post_data.get("caption", "")
        }

        result = ImageGenerationCrew().crew().kickoff(inputs=inputs)
        parsed_data = parse_json_output(result.raw)
        self.state.image_output = parsed_data
        return parsed_data

    @listen(generate_image)
    def combine_results(self, image_data):
        self.state.final_output = {
            "post_content": self.state.post_output,
            "image_content": self.state.image_output
        }
        return self.state.final_output

    def kickoff(self, persist=False, **kwargs):
        if "campaign_id" in kwargs and kwargs.get("campaign_id"):
            from core.models.campaign import Campaign
            from core.models.facebook_post import FacebookPost
            from core.models.post_image import PostImage

            campaign = Campaign.objects.get(id=kwargs["campaign_id"])

            self.state.campaign_id = campaign.id
            self.state.topic = kwargs.get("topic", "")
            self.state.objective = campaign.objective
            self.state.target_audience = campaign.target_audience
            self.state.tone = campaign.tone
            self.state.brand_voice = campaign.brand.voice_guidelines
            self.state.keywords = ", ".join(campaign.keywords) if campaign.keywords else ""

            super().kickoff()

            if persist:
                post = FacebookPost.objects.create(
                    campaign=campaign,
                    topic=self.state.topic,
                    caption=self.state.post_output.get("caption", ""),
                    hashtags=self.state.post_output.get("hashtags", []),
                    call_to_action=self.state.post_output.get("call_to_action", ""),
                    image_prompt=self.state.post_output.get("image_prompt", ""),
                    raw_report=self.state.post_output
                )

                image_ref = self.state.image_output.get("image_reference", "")
                if image_ref:
                    response = requests.get(image_ref, timeout=15)
                    response.raise_for_status()

                    post_image = PostImage(
                        post=post,
                        prompt_used=self.state.image_output.get("prompt_used", ""),
                        provider="openai",
                        model="gpt-image-1"
                    )
                    file_name = f"post_{post.id}_flow_image.png"
                    post_image.image_file.save(file_name, ContentFile(response.content), save=True)

        else:
            self.state.topic = kwargs.get("topic", "")
            self.state.objective = kwargs.get("objective", "")
            self.state.target_audience = kwargs.get("target_audience", "")
            self.state.tone = kwargs.get("tone", "")
            self.state.brand_voice = kwargs.get("brand_voice", "")
            self.state.keywords = kwargs.get("keywords", "")

            super().kickoff()

        return self.state.final_output