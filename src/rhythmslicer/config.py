# src/rhythmslicer/config.py

import os
import yaml
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class AppConfig:
    """
    A singleton class to manage application configuration from a YAML file.
    """
    _instance = None
    _config_data: Dict[str, Any] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def load_config(self, config_path: str = "config/defaults.yml") -> None:
        """
        Loads configuration from a YAML file if not already loaded.

        Args:
            config_path: The path to the configuration file.
        
        Raises:
            FileNotFoundError: If the configuration file cannot be found.
            ValueError: If there is an error parsing the YAML file.
        """
        if self._config_data:
            return  # Prevent reloading

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        logger.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, 'r') as f:
                self._config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value using dot notation.

        Example: config.get('beat_tracker.tightness')

        Args:
            key: The key of the configuration value, using dots for nesting.
            default: The default value to return if the key is not found.

        Returns:
            The configuration value or the default.
        """
        keys = key.split('.')
        value = self._config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# Global instance to be imported by other modules
config = AppConfig()