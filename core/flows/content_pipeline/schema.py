from pydantic import BaseModel
from typing import Dict, Any, Optional


class ContentPipelineState(BaseModel):
    # Inputs
    campaign_id: Optional[int] = None
    topic: str = ""
    objective: str = ""
    target_audience: str = ""
    tone: str = ""
    brand_voice: str = ""
    keywords: str = ""

    # Intermediate
    refined_prompt: str = ""

    # Outputs
    post_output: Dict[str, Any] = {}
    image_output: Dict[str, Any] = {}
    final_output: Dict[str, Any] = {}
