from dataclasses import dataclass
from pathlib import Path

# Configuration class for data ingestion with frozen attributes
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path 
    source_URL: str 
    local_data_file: Path 
    unzip_dir: Path 

# Configuration class for Preparing the base model
@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int

# Configuration class for model training
@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path  
    trained_model_path: Path  
    updated_base_model_path: Path  
    training_data: Path  
    params_learning_rate: float 
    params_epochs: int  
    params_batch_size: int  
    params_is_augmentation: bool  
    params_image_size: list 


# Configuration class for model evaluation
@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path 
    training_data: Path 
    all_params: dict 
    mlflow_uri: str 
    params_image_size: list 
    params_batch_size: int  