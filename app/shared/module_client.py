"""
Generic client the Manager App uses to talk to any module over HTTP —
whether that module is a Python function running in-process or a
separate service in another language (like the Node invoice parser).

Add each external service's base URL to your .env, e.g.:
    INVOICE_PARSER_URL=http://localhost:8001
"""

import httpx


class ModuleClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> dict:
        resp = httpx.get(f"{self.base_url}/health", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def run(self, payload: dict | None = None) -> dict:
        resp = httpx.post(f"{self.base_url}/run", json=payload or {}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
