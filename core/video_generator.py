from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class VideoProject:
    script: str
    voiceover_script: str
    shot_plan: List[str]
    music_mood: str
    output_directory: str
    created_at: str


class VideoGenerator:
    """Creates a structured video project plan for AI-assisted editing or rendering."""

    def __init__(self, output_dir: str = "generated_videos"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_script(self, topic: str, angle: str = "practical workflow") -> str:
        return (
            f"This video explains {topic} from a {angle} perspective. "
            "It starts with the problem, introduces the workflow, shows a working setup, and ends with a practical action plan."
        )

    def create_voiceover(self, topic: str) -> str:
        return (
            f"Today we are looking at {topic}. We will break this down into a simple system, explain the key ideas, and show you how to apply it immediately."
        )

    def create_shot_plan(self, topic: str) -> List[str]:
        return [
            f"Opening shot: cinematic intro for {topic}",
            "B-roll: workflow overview",
            "Screen capture: setup and configuration",
            "Talking head: main explanation",
            "Motion graphics: key steps summary",
            "Closing shot: call to action and subscribe prompt",
        ]

    def create_project(self, topic: str, angle: str = "practical workflow") -> VideoProject:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = os.path.join(self.output_dir, f"video_{timestamp}")
        os.makedirs(directory, exist_ok=True)

        return VideoProject(
            script=self.create_script(topic, angle),
            voiceover_script=self.create_voiceover(topic),
            shot_plan=self.create_shot_plan(topic),
            music_mood="cinematic futuristic ambient",
            output_directory=directory,
            created_at=datetime.now().isoformat(),
        )

    def create_batch(self, topics: List[str]) -> List[VideoProject]:
        return [self.create_project(topic) for topic in topics]

    def export_summary(self, projects: List[VideoProject]) -> List[dict]:
        return [asdict(project) for project in projects]
