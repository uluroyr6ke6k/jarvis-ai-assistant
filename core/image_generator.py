from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class ImageAsset:
    prompt: str
    output_path: str
    created_at: str
    model: str = "local-stable-diffusion"


class ImageGenerator:
    """Handles AI image generation workflow and prompt management."""

    def __init__(self, output_dir: str = "generated_images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_prompt(self, subject: str, style: str = "cinematic futuristic") -> str:
        return (
            f"{subject}, {style}, high detail, ultra realistic, dramatic lighting, "
            "clean composition, professional color grading, volumetric lighting"
        )

    def generate(self, subject: str, style: str = "cinematic futuristic") -> ImageAsset:
        prompt = self.create_prompt(subject, style)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"image_{timestamp}.png"
        output_path = os.path.join(self.output_dir, file_name)

        return ImageAsset(
            prompt=prompt,
            output_path=output_path,
            created_at=datetime.now().isoformat(),
            model="local-stable-diffusion",
        )

    def generate_batch(self, subjects: List[str], style: str = "cinematic futuristic") -> List[ImageAsset]:
        return [self.generate(subject, style) for subject in subjects]

    def export_summary(self, assets: List[ImageAsset]) -> List[dict]:
        return [asdict(asset) for asset in assets]
