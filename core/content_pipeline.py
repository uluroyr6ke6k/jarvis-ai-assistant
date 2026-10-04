from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

from core.youtube_manager import YouTubeManager
from core.image_generator import ImageGenerator
from core.video_generator import VideoGenerator
from core.blender_generator import BlenderGenerator


@dataclass
class ContentBundle:
    topic: str
    youtube_brief: dict
    image_assets: List[dict]
    video_project: dict
    blender_asset: dict


class ContentPipeline:
    """Coordinates all creative modules into a single content-production bundle."""

    def __init__(self):
        self.youtube_manager = YouTubeManager()
        self.image_generator = ImageGenerator()
        self.video_generator = VideoGenerator()
        self.blender_generator = BlenderGenerator()

    def build_bundle(self, topic: str, audience: str = "beginners") -> ContentBundle:
        brief = self.youtube_manager.create_brief(topic, audience)
        image_assets = self.image_generator.generate_batch([topic, f"{topic} workflow", f"{topic} thumbnail"], "cinematic futuristic")
        video_project = self.video_generator.create_project(topic)
        blender_asset = self.blender_generator.create_asset(topic)

        return ContentBundle(
            topic=topic,
            youtube_brief=asdict(brief),
            image_assets=[asdict(asset) for asset in image_assets],
            video_project=asdict(video_project),
            blender_asset=asdict(blender_asset),
        )

    def build_batch(self, topics: List[str]) -> List[ContentBundle]:
        return [self.build_bundle(topic) for topic in topics]
