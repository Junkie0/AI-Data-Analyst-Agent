# Configuration loader for the pipeline

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Load and manage pipeline configuration"""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent / "default.yaml"
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_path: Path to YAML config file (defaults to default.yaml)
            
        Returns:
            Configuration dictionary
        """
        
        if config_path is None:
            config_path = cls.DEFAULT_CONFIG_PATH
        
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        return config
    
    @classmethod
    def load_default(cls) -> Dict[str, Any]:
        """Load default configuration"""
        return cls.load(str(cls.DEFAULT_CONFIG_PATH))
    
    @classmethod
    def merge(cls, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configurations (overrides takes precedence)
        
        Args:
            base: Base configuration
            overrides: Configuration overrides
            
        Returns:
            Merged configuration
        """
        
        result = base.copy()
        
        for key, value in overrides.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = cls.merge(result[key], value)
            else:
                result[key] = value
        
        return result
