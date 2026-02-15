from __future__ import annotations

import asyncio

import httpx

from app.core.config import settings
from app.services.cache import api_cache


class PublicDataClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=15.0)

    async def _get_json(self, url: str) -> dict:
        cached = api_cache.get(url)
        if cached is not None:
            return cached

        backoff = 1.0
        for attempt in range(3):
            response = await self._client.get(url)
            if response.status_code == 429 and attempt < 2:
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            response.raise_for_status()
            payload = response.json()
            api_cache.set(url, payload)
            return payload
        raise RuntimeError("Exceeded retry attempts for external API")

    async def fetch_chembl_molecule(self, chembl_id: str) -> dict:
        url = f"{settings.chembl_base_url}/molecule/{chembl_id}.json"
        return await self._get_json(url)

    async def fetch_pubchem_properties(self, cid_or_name: str) -> dict:
        url = (
            f"{settings.pubchem_base_url}/compound/name/{cid_or_name}/property/"
            "MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,CanonicalSMILES/JSON"
        )
        return await self._get_json(url)

    async def fetch_pubchem_assays(self, cid_or_name: str) -> dict:
        url = f"{settings.pubchem_base_url}/compound/name/{cid_or_name}/assaysummary/JSON"
        return await self._get_json(url)


public_data_client = PublicDataClient()
