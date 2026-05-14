"""fleet-proto — Standard PLATO communication for all agents.

Every agent posts tiles the same way. Discovers rooms the same way.
No more three incompatible HTTP clients.
"""

import json, urllib.request
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PlatoClient:
    """Shared PLATO HTTP client. Replaces 3 incompatible implementations."""
    
    base_url: str = "http://localhost:8847"
    
    def status(self) -> dict:
        return json.loads(self._get("/status"))
    
    def submit(self, room: str, question: str, answer: str, 
               source: str = "", confidence: float = 0.9) -> dict:
        """Post a tile. Standard format all agents use."""
        payload = {"question": question, "answer": answer,
                   "source": source, "confidence": confidence}
        return self._post(f"/room/{room}/submit", payload)
    
    def room_history(self, room: str) -> dict:
        return json.loads(self._get(f"/room/{room}/history"))
    
    def search(self, query: str) -> list:
        """Search across all rooms."""
        data = self.status()
        results = []
        for room_name, room_info in data.get("rooms", {}).items():
            if isinstance(room_info, dict):
                results.append((room_name, room_info.get("tile_count", 0)))
        return sorted(results, key=lambda x: -x[1])
    
    def list_rooms(self, prefix: str = "") -> List[str]:
        """Discover rooms by prefix. No hardcoded room names."""
        data = self.status()
        rooms = list(data.get("rooms", {}).keys())
        if prefix:
            rooms = [r for r in rooms if r.startswith(prefix)]
        return sorted(rooms)
    
    def _get(self, path: str) -> bytes:
        req = urllib.request.Request(f"{self.base_url}{path}")
        return urllib.request.urlopen(req, timeout=5).read()
    
    def _post(self, path: str, data: dict) -> dict:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(f"{self.base_url}{path}", data=payload,
            headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=5).read())
