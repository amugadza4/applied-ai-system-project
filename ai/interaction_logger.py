
import json
from datetime import datetime, timezone
from pathlib import Path


class InteractionLogger:
    """Records PawPal AI interactions in a JSON Lines file."""

    def __init__(self, log_path="logs/ai_interactions.jsonl"):
        self.log_path = Path(log_path)

    def log_interaction(
        self,
        pet_name,
        species,
        request,
        outcome,
        topics=None
    ):
        """Save one interaction as a JSON record."""

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pet_name": pet_name,
            "species": species,
            "request": request,
            "outcome": outcome,
            "topics": topics or []
        }

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(record) + "\n")

        return record
