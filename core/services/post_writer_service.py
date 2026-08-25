from core.models.facebook_post import FacebookPost
from core.crews.post_writer_crew.crew import PostWriterCrew
from core.utils import parse_json_output


class PostWriterService:
    @staticmethod
    def run(campaign, topic: str) -> FacebookPost:
        inputs = {
            "topic": topic,
            "campaign_objective": campaign.objective,
            "target_audience": campaign.target_audience,
            "tone": campaign.tone,
            "brand_voice": campaign.brand.voice_guidelines,
            "keywords": ", ".join(campaign.Keywords) if campaign.Keywords else ""
        }

        try:
            result = PostWriterCrew().crew().kickoff(inputs=inputs)
            parsed_data = parse_json_output(result.raw)

            post = FacebookPost.objects.create(
                campaign=campaign,
                topic=topic,
                caption=parsed_data.get("caption", ""),
                hashtags=parsed_data.get("hashtags", []),
                call_to_action=parsed_data.get("call_to_action", ""),
                image_prompt=parsed_data.get("image_prompt", ""),
                raw_report=parsed_data
            )
            return post

        except Exception as e:
            raise ValueError(f"Agent 1 failed to generate the post: {str(e)}")