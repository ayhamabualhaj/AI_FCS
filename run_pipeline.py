import os
import django

# Initialize Django environment so we can import models and flows safely
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import json
from core.flows.content_pipeline.flow import ContentPipelineFlow


def main():
    print("🚀 Starting AI-FCS Pipeline (Raw Mode)...")

    flow = ContentPipelineFlow()

    # Passing raw string data to bypass the database for a quick terminal test
    result = flow.kickoff(
        topic="A revolutionary smart coffee mug that keeps drinks hot for 12 hours",
        objective="Drive pre-orders for the winter launch",
        target_audience="Tech-savvy remote workers and coffee enthusiasts",
        tone="Innovative, warm, and urgent",
        brand_voice="Sleek, modern, and highly caffeinated.",
        keywords="#SmartMug, #CoffeeLover, #TechGadgets"
    )

    print("\n✅ Pipeline Complete! Final Output:\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()