from __future__ import annotations

from typing import Any, Dict, List

from core.session_memory import SessionMemory


class ReflectionEngine:
    """Tracks outcomes and lets the assistant improve future behavior based on observed results."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()

    def score_result(self, task: str, result: Dict[str, Any]) -> float:
        status = str(result.get("status", "unknown")).lower()
        if status in {"ok", "success", "completed"}:
            score = 1.0
        elif status in {"unsupported", "empty", "error"}:
            score = 0.2
        else:
            score = 0.5

        if result.get("type") == "unsupported":
            score -= 0.4
        if result.get("result") and isinstance(result.get("result"), str):
            if "not supported" in result["result"].lower():
                score -= 0.3

        return max(0.0, min(1.0, score))

    def record(self, task: str, result: Dict[str, Any]) -> Dict[str, Any]:
        score = self.score_result(task, result)
        entry = {
            "task": task,
            "status": result.get("status", "unknown"),
            "score": score,
            "type": result.get("type", "unknown"),
            "result": result,
        }
        self.memory.log("reflection_record", entry)
        return {"status": "ok", "score": score, "task": task}

    def get_patterns(self) -> Dict[str, Any]:
        history = self.memory.get_recent(50)
        records = [item for item in history if item.get("action") == "reflection_record"]
        payloads = [item.get("payload", {}) for item in records]

        if not payloads:
            return {"status": "ok", "patterns": [], "average_score": 0.0}

        scores = [float(item.get("score", 0.0)) for item in payloads]
        trend = {
            "average_score": sum(scores) / len(scores),
            "patterns": sorted(
                {item.get("task") for item in payloads if item.get("task")},
                key=lambda x: x.lower(),
            ),
        }
        return {"status": "ok", **trend}

    def suggest_improvements(self) -> List[str]:
        pattern_data = self.get_patterns()
        suggestions: List[str] = []
        avg = pattern_data.get("average_score", 0.0)

        if avg < 0.7:
            suggestions.append("Improve task parsing for unsupported commands and ambiguous requests.")
        if pattern_data.get("patterns"):
            suggestions.append("Reuse the most successful task patterns in the task planner before testing new routes.")
        suggestions.append("Add stronger validation for commands that often fail or return unsupported results.")
        suggestions.append("Record user preferences from successful interactions and prioritize them in future plans.")
        return suggestions
