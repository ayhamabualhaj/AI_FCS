import logging
from crewai.tools import BaseTool
import openai
from decouple import config

logger = logging.getLogger(__name__)


class GenerateImageTool(BaseTool):
    name: str = "Generate Image Tool"
    description: str = "Generates an image using OpenAI based on a text prompt. Returns the image URL or base64 data URI."

    def _run(self, prompt: str) -> str:
        try:
            client = openai.OpenAI(api_key=config('OPENAI_API_KEY'))
            image_model = config('OPENAI_IMAGE_MODEL', default='dall-e-3')

            logger.info(f"[DEBUG] Prompt: {prompt[:100]}...")

            response = client.images.generate(
                model=image_model,
                prompt=prompt[:1000],
                n=1,
                size="1024x1024",
                response_format="url"  # <-- Explicitly demand a URL
            )

            logger.info(f"[DEBUG] Full response: {response}")
            logger.info(f"[DEBUG] Data[0]: {response.data[0]}")

            image_obj = response.data[0]

            if image_obj.url:
                logger.info(f"[DEBUG] Returning URL: {image_obj.url}")
                return image_obj.url

            if image_obj.b64_json:
                logger.info("[DEBUG] URL was None, but b64_json found")
                # Return as a data URI so it's still usable
                return f"data:image/png;base64,{image_obj.b64_json}"

            return "Error: OpenAI returned neither URL nor base64 image data."

        except Exception as e:
            logger.error(f"[DEBUG] EXCEPTION: {type(e).__name__}: {e}")
            return f"Error generating image: {str(e)}"