from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class VideoBrief:
    title: str
    hook: str
    outline: List[str]
    thumbnail_prompt: str
    seo_keywords: List[str]
    upload_description: str
    estimated_duration_minutes: int
    content_angle: str
    target_audience: str
    call_to_action: str


class YouTubeManager:
    """Generates YouTube-ready briefs and content flow for the Jarvis assistant."""

    def __init__(self, niche: str = "AI automation"):
        self.niche = niche

    def create_brief(self, topic: str, audience: str = "beginners") -> VideoBrief:
        title = self._build_title(topic)
        hook = self._build_hook(topic)
        outline = self._build_outline(topic)
        thumbnail_prompt = self._build_thumbnail_prompt(topic)
        seo_keywords = self._build_keywords(topic)
        upload_description = self._build_description(topic, seo_keywords)
        duration = self._estimate_duration(topic)

        return VideoBrief(
            title=title,
            hook=hook,
            outline=outline,
            thumbnail_prompt=thumbnail_prompt,
            seo_keywords=seo_keywords,
            upload_description=upload_description,
            estimated_duration_minutes=duration,
            content_angle=f"{self.niche} for {audience}",
            target_audience=audience,
            call_to_action="Subscribe for more AI automation workflows and tutorials.",
        )

    def _build_title(self, topic: str) -> str:
        clean_topic = topic.strip()
        return f"{clean_topic}: The Ultimate AI Workflow You Need to See"

    def _build_hook(self, topic: str) -> str:
        return (
            f"If you want to automate more of your workflow with {topic}, "
            "this is the fastest way to get real results without wasting hours."
        )

    def _build_outline(self, topic: str) -> List[str]:
        return [
            f"What is {topic} and why it matters",
            "The biggest mistake people make with this workflow",
            "Step-by-step setup for a working system",
            "How to automate the process without manual work",
            "Best tools and shortcuts to save time",
            "Final results and next steps",
        ]

    def _build_thumbnail_prompt(self, topic: str) -> str:
        return (
            f"A cinematic futuristic thumbnail about {topic}, glowing neon-blue UI, "
            "high contrast, bold text, clean composition, professional YouTube style"
        )

    def _build_keywords(self, topic: str) -> List[str]:
        base = [
            topic.lower(),
            self.niche.lower(),
            "automation workflow",
            "AI tutorial",
            "productivity hack",
            "smart systems",
            "workflow optimization",
        ]
        return list(dict.fromkeys(base))

    def _build_description(self, topic: str, keywords: List[str]) -> str:
        keyword_text = ", ".join(keywords)
        return (
            f"In this video, we cover {topic} in a practical way and show how to use it to save time, automate tasks, and build better systems.\n\n"
            f"Topics covered: {keyword_text}\n\n"
            "If you want more AI automation tutorials and workflow breakdowns, subscribe and turn on notifications."
        )

    def _estimate_duration(self, topic: str) -> int:
        # Simple heuristic based on topic length and complexity
        length = len(topic) // 10
        return max(6, min(18, 7 + length))

    def create_content_plan(self, topics: List[str]) -> List[VideoBrief]:
        return [self.create_brief(topic) for topic in topics]

    def export_json(self, brief: VideoBrief) -> str:
        return json.dumps(asdict(brief), indent=2)

    def export_batch(self, briefs: List[VideoBrief]) -> str:
        return json.dumps([asdict(b) for b in briefs], indent=2)

    def summarize_daily_upload_plan(self, topics: List[str]) -> Dict[str, object]:
        briefs = self.create_content_plan(topics)
        return {
            "generated_at": datetime.now().isoformat(),
            "niche": self.niche,
            "count": len(briefs),
            "titles": [brief.title for brief in briefs],
            "total_estimated_minutes": sum(b.estimated_duration_minutes for b in briefs),
        }
