"""RQ-backed queue adapter.

In production, run:
    rq worker drug_analysis --url redis://localhost:6379/0
"""

from __future__ import annotations

from dataclasses import dataclass

from redis import Redis
from rq import Queue

from app.core.config import settings


@dataclass
class RQConfig:
    enabled: bool = False


rq_config = RQConfig(enabled=False)


def get_queue() -> Queue:
    conn = Redis.from_url(settings.redis_url)
    return Queue("drug_analysis", connection=conn)
