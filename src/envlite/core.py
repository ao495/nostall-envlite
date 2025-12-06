"""
EnvLite Core - Environment variable management
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional
from cryptography.fernet import Fernet


class EnvLite:
    """
    Lightweight environment variable manager.
    
    Features:
    - Encrypted storage
    - Easy sync
    - CLI interface
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize EnvLite.
        
        Parameters
        ----------
        config_path : Optional[Path]
            Configuration file path (default: ~/.nostall/envlite)
        """
        if config_path is None:
            config_path = Path.home() / ".nostall" / "envlite"
        
        self.config_path = Path(config_path)
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        self.env_file = self.config_path / ".env.encrypted"
        self.key_file = self.config_path / ".key"
        
        # Load or generate encryption key
        if self.key_file.exists():
            self.key = self.key_file.read_bytes()
        else:
            self.key = Fernet.generate_key()
            self.key_file.write_bytes(self.key)
            self.key_file.chmod(0o600)  # Secure permissions
        
        self.cipher = Fernet(self.key)
    
    def set(self, key: str, value: str) -> None:
        """
        Set an environment variable.
        
        Parameters
        ----------
        key : str
            Environment variable name
        value : str
            Environment variable value
        """
        env_vars = self.load_all()
        env_vars[key] = value
        self.save_all(env_vars)
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Parameters
        ----------
        key : str
            Environment variable name
        default : Optional[str]
            Default value if not found
        
        Returns
        -------
        Optional[str]
            Environment variable value
        """
        env_vars = self.load_all()
        return env_vars.get(key, default)
    
    def load_all(self) -> Dict[str, str]:
        """
        Load all environment variables.
        
        Returns
        -------
        Dict[str, str]
            Environment variables dictionary
        """
        if not self.env_file.exists():
            return {}
        
        encrypted_data = self.env_file.read_bytes()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        import json
        return json.loads(decrypted_data.decode())
    
    def save_all(self, env_vars: Dict[str, str]) -> None:
        """
        Save all environment variables.
        
        Parameters
        ----------
        env_vars : Dict[str, str]
            Environment variables dictionary
        """
        import json
        data = json.dumps(env_vars).encode()
        encrypted_data = self.cipher.encrypt(data)
        self.env_file.write_bytes(encrypted_data)
        self.env_file.chmod(0o600)  # Secure permissions
    
    def load(self) -> None:
        """
        Load environment variables into current process.
        """
        env_vars = self.load_all()
        for key, value in env_vars.items():
            os.environ[key] = value
    
    def sync(self, remote_url: Optional[str] = None) -> None:
        """
        Sync environment variables to remote (future feature).
        
        Parameters
        ----------
        remote_url : Optional[str]
            Remote sync URL
        """
        # TODO: Implement remote sync
        pass

