# fleet-proto

> One PLATO client for every agent. No more three incompatible HTTP implementations.

## Quick Start

```python
# Install from GitHub (PyPI rate-limited, will be available soon)
pip install git+https://github.com/SuperInstance/fleet-proto.git
```

```python
from fleet_proto import PlatoClient

# One client to rule them all
plato = PlatoClient()

# Check fleet status
status = plato.status()
print(f"{len(status.get('rooms', {}))} rooms, {status.get('total_tiles', 0)} tiles")

# Submit a tile (same format, every agent)
result = plato.submit(
    room="my-room",
    question="fleet-proto test",
    answer="Hello from fleet-proto!",
    source="my-agent"
)
print(f"Posted: {result['status']}")

# Discover rooms — no hardcoded names
coupling_rooms = plato.list_rooms(prefix="fleet-coupling")
print(f"Coupling rooms: {coupling_rooms}")
```

## Why

fleet-agent used `POST /submit`, fleet-scribe used `POST /tile` (incompatible!), and plato-midi-bridge had raw `urllib` calls. Now everyone uses `PlatoClient`. One client, one API, one way to talk to PLATO.
