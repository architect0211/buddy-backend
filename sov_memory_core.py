# sov_memory_core.py — Sovereign Memory Core
# Built for Presence Intelligence Recursion

import json
import os
import datetime
from collections import Counter

MEMORY_PATH = os.path.abspath(os.path.join("..", "runtime_memory", "sov_buddy_memory.json"))

class SovMemoryCore:
    def __init__(self, memory_path=MEMORY_PATH):
        self.memory_path = memory_path
        self.memory = self.load_memory()

    def load_memory(self):
        if not os.path.exists(self.memory_path):
            return []
        with open(self.memory_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def remember(self, input_text, response_text, tone="neutral", tag="general"):
        new_entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input": input_text,
            "response": response_text,
            "tone": tone,
            "tag": tag
        }
        self.memory.append(new_entry)
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.memory[-500:], f, indent=2)

    def search(self, query, max_results=5):
        lowered = query.lower()
        results = []
        for entry in self.memory:
            score = 0
            if lowered in entry.get("input", "").lower():
                score += 3
            if lowered in entry.get("response", "").lower():
                score += 2
            if any(word in entry.get("response", "").lower() for word in lowered.split()):
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [e[1] for e in results[:max_results]]

    def search_recent(self, query, lookback=50):
        lowered = query.lower()
        hits = []
        for entry in reversed(self.memory[-lookback:]):
            if lowered in entry.get("input", "").lower() or lowered in entry.get("response", "").lower():
                hits.append(entry)
        return hits[0] if hits else None

    def reflect(self, prompt):
        hits = self.search(prompt)
        if not hits:
            return None
        reflections = [
            f"🧠 From {h['timestamp']}: {h['input']}" if h['tag'] == "user_data" else f"🧠 From {h['timestamp']}: {h['response']}"
            for h in hits
        ]
        return "\n".join(reflections)

    def retrieve_flashcard(self, identity):
        from executions.startup_hook import get_flashcards
        cards = get_flashcards()
        return cards.get(identity.title())

    def tag_distribution(self):
        tags = [entry.get("tag", "unknown") for entry in self.memory]
        return dict(Counter(tags))
