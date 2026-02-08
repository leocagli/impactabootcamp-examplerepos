"""
Módulo de configuración para Stellar Deployment Automation

Maneja la carga y validación de configuración desde archivo .env
"""

import os
from dotenv import load_dotenv
from stellar_sdk import Keypair


class DeploymentConfig:
    """Clase para manejar la configuración del deployment"""
    
    def __init__(self, env_file='.env'):
        """
        Inicializa la configuración desde archivo .env
        
        Args:
            env_file: Ruta al archivo .env
        """
        # Cargar variables de entorno
        if not load_dotenv(env_file):
            print(f"⚠ Advertencia: No se encontró archivo {env_file}")
        
        self._load_and_validate()
    
    def _load_and_validate(self):
        """Carga y valida todas las variables de configuración"""
        # Configuración de cuenta Stellar
        self.secret_key = self._get_required('STELLAR_SECRET_KEY')
        self.keypair = self._validate_keypair(self.secret_key)
        
        # Configuración del deployer service
        self.deployer_url = self._get_optional(
            'DEPLOYER_SERVICE_URL',
            'https://api.example.com/deployer'
        )
        
        # Configuración de direcciones
        self.signer_address = self._get_optional(
            'SIGNER_ADDRESS',
            self.keypair.public_key
        )
        self.service_provider = self._get_optional('SERVICE_PROVIDER_ADDRESS', '')
        self.platform_address = self._get_optional('PLATFORM_ADDRESS', '')
        
        # Configuración de red Stellar
        self.rpc_url = self._get_optional(
            'RPC_URL',
            'https://soroban-testnet.stellar.org'
        )
        self.network_passphrase = self._get_optional(
            'NETWORK_PASSPHRASE',
            'Test SDF Network ; September 2015'
        )
        
        # Configuración de validación
        self.enable_expert_validation = self._get_bool(
            'ENABLE_STELLAR_EXPERT_VALIDATION',
            True
        )
        self.stellar_expert_url = self._get_optional(
            'STELLAR_EXPERT_URL',
            'https://stellar.expert/explorer/testnet'
        )
    
    def _get_required(self, key):
        """
        Obtiene una variable de entorno requerida
        
        Args:
            key: Nombre de la variable
            
        Returns:
            str: Valor de la variable
            
        Raises:
            ValueError: Si la variable no está definida
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} es requerido en el archivo .env")
        return value
    
    def _get_optional(self, key, default=''):
        """
        Obtiene una variable de entorno opcional
        
        Args:
            key: Nombre de la variable
            default: Valor por defecto
            
        Returns:
            str: Valor de la variable o default
        """
        return os.getenv(key, default)
    
    def _get_bool(self, key, default=False):
        """
        Obtiene una variable de entorno booleana
        
        Args:
            key: Nombre de la variable
            default: Valor por defecto
            
        Returns:
            bool: Valor booleano
        """
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def _validate_keypair(self, secret_key):
        """
        Valida y crea un Keypair desde una secret key
        
        Args:
            secret_key: Secret key de Stellar
            
        Returns:
            Keypair: Objeto Keypair validado
            
        Raises:
            ValueError: Si la secret key es inválida
        """
        try:
            return Keypair.from_secret(secret_key)
        except Exception as e:
            raise ValueError(f"STELLAR_SECRET_KEY inválido: {e}")
    
    def to_dict(self):
        """
        Convierte la configuración a diccionario (sin datos sensibles)
        
        Returns:
            dict: Configuración como diccionario
        """
        return {
            'signer_address': self.signer_address,
            'service_provider': self.service_provider,
            'platform_address': self.platform_address,
            'deployer_url': self.deployer_url,
            'rpc_url': self.rpc_url,
            'network_passphrase': self.network_passphrase,
            'enable_expert_validation': self.enable_expert_validation,
            'stellar_expert_url': self.stellar_expert_url
        }
    
    def __repr__(self):
        """Representación en string de la configuración"""
        config_dict = self.to_dict()
        return f"DeploymentConfig({config_dict})"
