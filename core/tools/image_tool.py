import logging
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import openai
from decouple import config

logger = logging.getLogger(__name__)


class GenerateImageInput(BaseModel):
    """Input schema for the image generation tool."""
    prompt: str = Field(..., description="A detailed text prompt to generate an image from.")


class GenerateImageTool(BaseTool):
    name: str = "generate_image_tool"
    description: str = (
        "Generates an image using OpenAI gpt-image-1 based on a text prompt. "
        "Returns a base64 data URI string."
    )
    args_schema: Type[BaseModel] = GenerateImageInput

    def _run(self, prompt: str) -> str:
        try:
            client = openai.OpenAI(api_key=config('OPENAI_API_KEY'))
            image_model = config('OPENAI_IMAGE_MODEL', default='gpt-image-1')

            logger.info(f"[GenerateImageTool] Model: {image_model}")
            logger.info(f"[GenerateImageTool] Prompt: {prompt[:100]}...")

            # gpt-image-1 API: NO response_format, NO n, NO size
            response = client.images.generate(
                model=image_model,
                prompt=prompt[:32000],  # gpt-image-1 supports very long prompts
            )

            image_obj = response.data[0]

            # gpt-image-1 returns base64 by default
            if hasattr(image_obj, 'b64_json') and image_obj.b64_json:
                logger.info("[GenerateImageTool] Success — base64 returned.")
                return f"data:image/png;base64,{image_obj.b64_json}"

            # Fallback if URL is somehow returned
            if hasattr(image_obj, 'url') and image_obj.url:
                logger.info("[GenerateImageTool] Success — URL returned.")
                return image_obj.url

            return "ERROR: OpenAI returned no image data."

        except openai.APIError as e:
            logger.error(f"[GenerateImageTool] API Error: {e}")
            return f"ERROR: {str(e)}"
        except Exception as e:
            logger.error(f"[GenerateImageTool] Exception: {type(e).__name__}: {e}")
            return f"ERROR: {type(e).__name__} - {str(e)}"