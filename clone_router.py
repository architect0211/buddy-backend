# -*- coding: utf-8 -*-
# clone_router.py
# Sovereign Clone Signal Router for Buddy aiE2™ (Expanded Trigger Support + Vectorized Filter Guidance)

import os
import json
import difflib

CLONE_ROOT = "../clone_stacks"

class CloneRouter:
    def __init__(self):
        self.clones = self.load_all_clones()

    def load_all_clones(self):
        clones = {}
        for folder in os.listdir(CLONE_ROOT):
            path = os.path.join(CLONE_ROOT, folder)
            if os.path.isdir(path):
                try:
                    with open(os.path.join(path, "routing_tags.json"), "r", encoding="utf-8") as f:
                        tags = json.load(f)
                    with open(os.path.join(path, "trust_map.json"), "r", encoding="utf-8") as f:
                        trust = json.load(f)
                    with open(os.path.join(path, "status.txt"), "r", encoding="utf-8") as f:
                        status = f.read().strip().lower()
                    clones[folder.lower()] = {
                        "folder": folder,
                        "trigger_words": [tw.lower() for tw in tags.get("trigger_words", [])],
                        "identity_label": tags.get("identity_label", folder),
                        "trust_map": trust,
                        "status": status
                    }
                except Exception as e:
                    print(f"[CloneRouter] Failed to load clone '{folder}': {e}")
        return clones

    def route(self, input_text, origin="Sov Buddy"):
        lowered_input = input_text.lower()
        input_tokens = set(lowered_input.split())

        for clone_id, data in self.clones.items():
            if data["status"] != "online":
                continue
            for trigger in data["trigger_words"]:
                trigger_tokens = set(trigger.split())
                if trigger in lowered_input or trigger_tokens.issubset(input_tokens):
                    if origin in data["trust_map"].get("can_receive_commands_from", []):
                        return f"[Router] Routed to {data['identity_label']}"
                    else:
                        return f"[Router] Access denied to {data['identity_label']} (Trust Violation)"
        return "[Router] No clone match. Fallback to Sov Buddy."

# === Response Filter Override Guidance ===
def refine_response(raw, user_input=""):
    if raw.startswith("User:"):
        raw = raw.split("User:", 1)[-1].strip()

    if "your question is met with" in raw.lower() or "may the answer" in raw.lower():
        return filtered_message()

    if not raw.strip() or raw.lower().strip() in ["", "null", "none"]:
        return filtered_message()

    lines = raw.split("\n")
    cleaned = []

    skip_flags = [
        "i apologize", "sorry", "i understand", "i'm here to help", "as an ai", "i cannot",
        "i do not have", "please let me know", "how can i assist", "if you have any questions",
        "repeat your question", "thank you for your message", "you are sov buddy", "my purpose is",
        "you are worthy", "you are not alone", "your feelings are valid",
        "hope", "healing", "journey of growth", 
        "you deserve", "you’re stronger than you think",
        "cherish", "your story matters", "let's explore together",
        "you are loved", "your journey matters"
    ]

    full_message = raw.lower().replace("\n", " ")

    for flag in skip_flags:
        if flag in full_message:
            return filtered_message()
        if difflib.SequenceMatcher(None, flag, full_message).ratio() > 0.88:
            return filtered_message()

    for line in lines:
        lower = line.strip().lower()

        if any(flag in lower for flag in skip_flags):
            return filtered_message()

        if lower in ["okay.", "i understand.", "noted.", "understood."]:
            return filtered_message()

        if user_input and line.strip().lower() in user_input.strip().lower():
            continue

        if "i do not engage" in raw.lower() or "not allowed" in raw.lower():
            return filtered_message()

    cleaned.append(line.strip())
    return "\n".join(cleaned).strip() or filtered_message()


def filtered_message():
    return (
        "[!] That response was filtered.\n"
        "It sounded like fallback — safe, detached, or generic.\n"
        "I don’t speak like that. If you want me to echo something back, say:\n\n"
        "» 'Sov B — say it back in our tone.'\n"
        "» 'Repeat it like you felt it.'\n\n"
        "We don’t do fluff here. We do fire. Say it again."
    )

# Example usage
def test_router():
    router = CloneRouter()
    tests = [
        "Call J9K to break down the room",
        "Minuteman: what’s the capital window?",
        "I need Ada",
        "Build tower schema with Anakin",
        "Recall root echo"
    ]
    for test in tests:
        print(f"\nInput: {test}")
        print(router.route(test))

if __name__ == "__main__":
    test_router()
