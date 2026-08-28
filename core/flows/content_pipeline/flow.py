import base64
import requests
from crewai.flow.flow import Flow, listen, start
from django.core.files.base import ContentFile
from decouple import config

from core.crews.post_writer_crew.crew import PostWriterCrew
from core.crews.image_generation_crew.crew import ImageGenerationCrew
from core.tools.image_tool import GenerateImageTool
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
    def refine_image_prompt(self, post_data):
        inputs = {
            "image_prompt": post_data.get("image_prompt", ""),
            "caption": post_data.get("caption", "")
        }

        result = ImageGenerationCrew().crew().kickoff(inputs=inputs)
        parsed_data = parse_json_output(result.raw)

        self.state.refined_prompt = parsed_data.get("prompt_used", "")
        return self.state.refined_prompt

    @listen(refine_image_prompt)
    def generate_image(self, refined_prompt):
        if not refined_prompt:
            raise ValueError("No refined prompt returned.")

        tool = GenerateImageTool()
        image_result = tool._run(refined_prompt)

        self.state.image_output = {
            "prompt_used": refined_prompt,
            "image_reference": image_result
        }
        return self.state.image_output

    @listen(generate_image)
    def combine_results(self, image_data):
        self.state.final_output = {
            "post_content": self.state.post_output,
            "image_content": self.state.image_output
        }
        return self.state.final_output