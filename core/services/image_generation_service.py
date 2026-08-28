import base64
from django.core.files.base import ContentFile
from decouple import config

from core.models.post_image import PostImage
from core.crews.image_generation_crew.crew import ImageGenerationCrew
from core.tools.image_tool import GenerateImageTool
from core.utils import parse_json_output


class ImageGenerationService:
    @staticmethod
    def run(post) -> PostImage:

        if not post.image_prompt:
            raise ValueError("The post does not have an image_prompt.")

        inputs = {
            "image_prompt": post.image_prompt,
            "caption": post.caption
        }

        # Step 1: Agent refines prompt
        result = ImageGenerationCrew().crew().kickoff(inputs=inputs)
        parsed_data = parse_json_output(result.raw)
        refined_prompt = parsed_data.get("prompt_used", "")

        if not refined_prompt:
            raise ValueError("Agent did not return a refined prompt.")

        # Step 2: Generate image directly (no LLM involved)
        tool = GenerateImageTool()
        image_result = tool._run(refined_prompt)

        if image_result.startswith("ERROR"):
            raise ValueError(f"Image generation failed: {image_result}")

        # Step 3: Save to Django
        if image_result.startswith("data:image"):
            header, b64_data = image_result.split(",", 1)
            image_bytes = base64.b64decode(b64_data)
        else:
            raise ValueError("Expected base64 data URI from gpt-image-1.")

        post_image = PostImage(
            post=post,
            prompt_used=refined_prompt,
            provider="openai",
            model=config('OPENAI_IMAGE_MODEL', default='gpt-image-1')
        )

        file_name = f"post_{post.id}_image.png"
        post_image.image_file.save(file_name, ContentFile(image_bytes), save=True)

        return post_image