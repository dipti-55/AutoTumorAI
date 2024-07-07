from dataclasses import dataclass
from pathlib import Path

# Configuration class for data ingestion with frozen attributes
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path 
    source_URL: str 
    local_data_file: Path 
    unzip_dir: Path 