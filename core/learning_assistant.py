from __future__ import annotations

from typing import Any, Dict, List

from core.reflection_engine import ReflectionEngine
from core.session_memory import SessionMemory


class LearningAssistant:
    """Coordinates reflection-based self-improvement for future assistant behavior."""

    def __init__(self):
        self.memory = SessionMemory()
        self.memory.load()
        self.reflection = ReflectionEngine()

    def evaluate_task(self, task: str, result: Dict[str, Any]) -> Dict[str, Any]:
        record = self.reflection.record(task, result)
        patterns = self.reflection.get_patterns()
        suggestions = self.reflection.suggest_improvements()

        return {
            "status": "ok",
            "task": task,
            "score": record.get("score"),
            "average_score": patterns.get("average_score"),
            "suggestions": suggestions,
        }

    def improve_plan(self, task: str, candidate_tasks: List[str]) -> List[str]:
        patterns = self.reflection.get_patterns()
        known = patterns.get("patterns", [])

        ranked = []
        for candidate in candidate_tasks:
            if candidate in known:
                ranked.insert(0, candidate)
            else:
                ranked.append(candidate)

        self.memory.log("plan_improvement", {"task": task, "candidate_tasks": candidate_tasks, "ranked": ranked})
        return ranked

    def generate_learning_summary(self) -> Dict[str, Any]:
        patterns = self.reflection.get_patterns()
        suggestions = self.reflection.suggest_improvements()
        return {
            "status": "ok",
            "average_score": patterns.get("average_score"),
            "observed_tasks": patterns.get("patterns", []),
            "suggestions": suggestions,
        }
