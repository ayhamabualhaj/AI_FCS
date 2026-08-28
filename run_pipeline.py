import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import json
from core.flows.content_pipeline.flow import ContentPipelineFlow


def main():
    print("🚀 Starting AI-FCS Pipeline...")

    flow = ContentPipelineFlow()

    # Set inputs via state
    flow.state.topic = "A revolutionary smart coffee mug that keeps drinks hot for 12 hours"
    flow.state.objective = "Drive pre-orders for the winter launch"
    flow.state.target_audience = "Tech-savvy remote workers and coffee enthusiasts"
    flow.state.tone = "Innovative, warm, and urgent"
    flow.state.brand_voice = "Sleek, modern, and highly caffeinated."
    flow.state.keywords = "#SmartMug, #CoffeeLover, #TechGadgets"

    # Run the flow
    flow.kickoff()

    # Get results from state
    result = flow.state.final_output

    print("\n✅ Pipeline Complete!\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Verify image
    if flow.state.image_output:
        img_ref = flow.state.image_output.get("image_reference", "")
        print(f"\n🖼️  Image data starts with: {img_ref[:60]}...")
        print(f"📝 Prompt used: {flow.state.image_output.get('prompt_used', '')[:80]}...")


if __name__ == "__main__":
    main()