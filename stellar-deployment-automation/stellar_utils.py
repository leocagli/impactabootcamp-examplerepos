"""
Módulo de utilidades para interactuar con Stellar Network

Contiene funciones para firmar XDR, enviar transacciones y validar en Stellar Expert
"""

import requests
from stellar_sdk import TransactionEnvelope
from stellar_sdk.exceptions import BadRequestError


class StellarUtils:
    """Clase con utilidades para interactuar con Stellar"""
    
    @staticmethod
    def sign_xdr(xdr_string, keypair, network_passphrase):
        """
        Firma un XDR con un keypair
        
        Args:
            xdr_string: String del XDR a firmar
            keypair: Keypair para firmar
            network_passphrase: Network passphrase de Stellar
            
        Returns:
            str: XDR firmado
            
        Raises:
            Exception: Si hay error al firmar
        """
        try:
            # Convertir XDR a TransactionEnvelope
            tx_env = TransactionEnvelope.from_xdr(xdr_string, network_passphrase)
            
            # Firmar con el keypair
            tx_env.sign(keypair)
            
            # Retornar XDR firmado
            return tx_env.to_xdr()
            
        except Exception as e:
            raise Exception(f"Error al firmar XDR: {e}")
    
    @staticmethod
    def validate_xdr_format(xdr_string):
        """
        Valida que un string sea un XDR válido
        
        Args:
            xdr_string: String a validar
            
        Returns:
            bool: True si es válido
        """
        try:
            from stellar_sdk import xdr as stellar_xdr
            stellar_xdr.TransactionEnvelope.from_xdr(xdr_string)
            return True
        except Exception:
            return False


class DeployerClient:
    """Cliente para interactuar con el Deployer Service"""
    
    def __init__(self, base_url, timeout=30):
        """
        Inicializa el cliente
        
        Args:
            base_url: URL base del deployer service
            timeout: Timeout en segundos para requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def post_single_release(self, payload):
        """
        Envía POST al endpoint /single-release
        
        Args:
            payload: Datos JSON a enviar
            
        Returns:
            dict: Respuesta del servidor
            
        Raises:
            Exception: Si hay error en la petición
        """
        endpoint = f"{self.base_url}/single-release"
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error HTTP {response.status_code}: {e}")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout al conectar con {endpoint}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión: {e}")
    
    def submit_signed_xdr(self, signed_xdr, endpoint_path='/submit'):
        """
        Envía XDR firmado al endpoint de submission
        
        Args:
            signed_xdr: XDR firmado
            endpoint_path: Path del endpoint (default: /submit)
            
        Returns:
            dict: Respuesta con transaction hash
            
        Raises:
            Exception: Si hay error en la petición
        """
        endpoint = f"{self.base_url}{endpoint_path}"
        
        try:
            response = requests.post(
                endpoint,
                json={"xdr": signed_xdr},
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error HTTP {response.status_code}: {e}")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout al enviar XDR firmado")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión: {e}")


class StellarExpertValidator:
    """Validador de transacciones en Stellar Expert"""
    
    def __init__(self, base_url):
        """
        Inicializa el validador
        
        Args:
            base_url: URL base de Stellar Expert
        """
        self.base_url = base_url.rstrip('/')
    
    def get_transaction_url(self, tx_hash):
        """
        Obtiene la URL de una transacción en Stellar Expert
        
        Args:
            tx_hash: Hash de la transacción
            
        Returns:
            str: URL completa
        """
        return f"{self.base_url}/tx/{tx_hash}"
    
    def validate_transaction(self, tx_hash):
        """
        Valida si una transacción existe en Stellar Expert
        
        Args:
            tx_hash: Hash de la transacción
            
        Returns:
            tuple: (existe: bool, url: str)
        """
        url = self.get_transaction_url(tx_hash)
        
        try:
            response = requests.get(url, timeout=10)
            exists = response.status_code == 200
            return (exists, url)
            
        except requests.exceptions.RequestException:
            return (False, url)
    
    def get_contract_url(self, contract_id):
        """
        Obtiene la URL de un contrato en Stellar Expert
        
        Args:
            contract_id: ID del contrato
            
        Returns:
            str: URL completa
        """
        return f"{self.base_url}/contract/{contract_id}"
