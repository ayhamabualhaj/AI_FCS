import requests
from django.core.files.base import ContentFile
from core.models.post_image import PostImage
from core.crews.image_generation_crew.crew import ImageGenerationCrew
from core.utils import parse_json_output


class ImageGenerationService:
    @staticmethod
    def run(post) -> PostImage:

        if not post.image_prompt:
            raise ValueError("The post does not have an image_prompt to generate an image.")

        inputs = {
            "image_prompt": post.image_prompt,
            "caption": post.caption
        }

        try:
            result = ImageGenerationCrew().crew().kickoff(inputs=inputs)
            parsed_data = parse_json_output(result.raw)

            image_reference = parsed_data.get("image_reference", "")
            if not image_reference:
                raise ValueError("Agent 2 did not return a valid image URL.")

            response = requests.get(image_reference, timeout=15)
            response.raise_for_status()

            post_image = PostImage(
                post=post,
                prompt_used=parsed_data.get("prompt_used", ""),
                provider="openai",
                model="gpt-image-1"
            )

            file_name = f"post_{post.id}_agent2_image.png"
            post_image.image_file.save(file_name, ContentFile(response.content), save=True)

            return post_image

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Image download failed. Ensure you have internet/valid API keys: {str(e)}")
        except Exception as e:
            raise ValueError(f"Agent 2 failed to generate the image: {str(e)}")