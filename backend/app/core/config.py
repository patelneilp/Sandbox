from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Drug Feasibility Analyzer"
    api_prefix: str = "/api"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 3600
    max_entities_per_job: int = 200
    chembl_base_url: str = "https://www.ebi.ac.uk/chembl/api/data"
    pubchem_base_url: str = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


settings = Settings()
