#!/usr/bin/env python3
"""
Stellar Testnet Deployment Automation Script

Este script automatiza el flujo de deployment de contratos Soroban en Stellar Testnet:
1. Carga configuración desde archivo .env
2. Envía POST al endpoint deployer/single-release
3. Firma el XDR recibido usando Stellar SDK
4. Envía el XDR firmado y procesa el transaction hash
5. Opcionalmente valida en Stellar Expert
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from stellar_sdk import Keypair, Network, TransactionBuilder, Server
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import BadRequestError, NotFoundError


class StellarDeploymentAutomation:
    """Clase principal para automatizar el deployment en Stellar testnet"""
    
    def __init__(self, env_file='.env'):
        """
        Inicializa el script de automatización
        
        Args:
            env_file: Ruta al archivo de configuración .env
        """
        # Cargar variables de entorno
        load_dotenv(env_file)
        
        # Validar y cargar configuración
        self._load_configuration()
        
        # Inicializar Stellar SDK
        self._init_stellar_client()
        
    def _load_configuration(self):
        """Carga y valida la configuración desde variables de entorno"""
        # Configuración requerida
        self.secret_key = os.getenv('STELLAR_SECRET_KEY')
        if not self.secret_key:
            raise ValueError("STELLAR_SECRET_KEY es requerido en el archivo .env")
        
        # Validar formato de secret key
        try:
            self.keypair = Keypair.from_secret(self.secret_key)
        except Exception as e:
            raise ValueError(f"STELLAR_SECRET_KEY inválido: {e}")
        
        # Configuración del deployer service
        self.deployer_url = os.getenv('DEPLOYER_SERVICE_URL', 'https://api.example.com/deployer')
        
        # Configuración de direcciones
        self.signer_address = os.getenv('SIGNER_ADDRESS', self.keypair.public_key)
        self.service_provider = os.getenv('SERVICE_PROVIDER_ADDRESS', '')
        self.platform_address = os.getenv('PLATFORM_ADDRESS', '')
        
        # Configuración de red
        self.rpc_url = os.getenv('RPC_URL', 'https://soroban-testnet.stellar.org')
        self.network_passphrase = os.getenv('NETWORK_PASSPHRASE', 'Test SDF Network ; September 2015')
        
        # Configuración opcional
        self.enable_expert_validation = os.getenv('ENABLE_STELLAR_EXPERT_VALIDATION', 'true').lower() == 'true'
        self.stellar_expert_url = os.getenv('STELLAR_EXPERT_URL', 'https://stellar.expert/explorer/testnet')
        
    def _init_stellar_client(self):
        """Inicializa el cliente de Stellar SDK"""
        try:
            self.server = Server(horizon_url=self.rpc_url)
            print(f"✓ Conectado a Stellar RPC: {self.rpc_url}")
        except Exception as e:
            print(f"⚠ Advertencia: No se pudo conectar al servidor Stellar: {e}")
            self.server = None
    
    def create_deployment_payload(self, contract_data=None):
        """
        Crea el payload para el endpoint deployer/single-release
        
        Args:
            contract_data: Datos adicionales del contrato (dict)
            
        Returns:
            dict: Payload JSON para el POST request
        """
        if contract_data is None:
            contract_data = {}
            
        payload = {
            "signer": self.signer_address,
            "serviceProvider": self.service_provider,
            "platformAddress": self.platform_address,
            **contract_data
        }
        
        return payload
    
    def post_to_deployer(self, payload):
        """
        Envía POST al endpoint deployer/single-release
        
        Args:
            payload: Datos JSON a enviar
            
        Returns:
            dict: Respuesta del servidor con XDR
        """
        endpoint = f"{self.deployer_url}/single-release"
        
        print(f"\n📤 Enviando POST a: {endpoint}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Respuesta recibida del deployer")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al conectar con el deployer service: {e}")
    
    def sign_xdr(self, xdr_string):
        """
        Firma un XDR usando la clave privada configurada
        
        Args:
            xdr_string: String del XDR a firmar
            
        Returns:
            str: XDR firmado
        """
        print(f"\n🔏 Firmando XDR...")
        
        try:
            # Parsear el XDR
            transaction_envelope = stellar_xdr.TransactionEnvelope.from_xdr(xdr_string)
            
            # Firmar con nuestro keypair
            # Nota: En stellar-sdk v11+, se usa sign_transaction_envelope
            from stellar_sdk.transaction_envelope import TransactionEnvelope
            
            # Convertir XDR a TransactionEnvelope
            tx_env = TransactionEnvelope.from_xdr(xdr_string, self.network_passphrase)
            
            # Firmar
            tx_env.sign(self.keypair)
            
            # Obtener XDR firmado
            signed_xdr = tx_env.to_xdr()
            
            print(f"✓ XDR firmado exitosamente")
            
            return signed_xdr
            
        except Exception as e:
            raise Exception(f"Error al firmar XDR: {e}")
    
    def submit_signed_xdr(self, signed_xdr, submission_endpoint=None):
        """
        Envía el XDR firmado al endpoint de submission
        
        Args:
            signed_xdr: XDR firmado
            submission_endpoint: URL del endpoint (opcional)
            
        Returns:
            dict: Respuesta con transaction hash
        """
        if submission_endpoint is None:
            submission_endpoint = f"{self.deployer_url}/submit"
        
        print(f"\n📤 Enviando XDR firmado a: {submission_endpoint}")
        
        try:
            response = requests.post(
                submission_endpoint,
                json={"xdr": signed_xdr},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ XDR enviado exitosamente")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al enviar XDR firmado: {e}")
    
    def validate_on_stellar_expert(self, transaction_hash):
        """
        Valida el deployment en Stellar Expert
        
        Args:
            transaction_hash: Hash de la transacción
            
        Returns:
            str: URL de Stellar Expert para la transacción
        """
        expert_url = f"{self.stellar_expert_url}/tx/{transaction_hash}"
        
        print(f"\n🔍 Validando en Stellar Expert...")
        print(f"URL: {expert_url}")
        
        try:
            response = requests.get(expert_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ Transacción encontrada en Stellar Expert")
            else:
                print(f"⚠ Transacción no encontrada aún (puede tardar unos segundos)")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠ No se pudo validar en Stellar Expert: {e}")
        
        return expert_url
    
    def run_deployment_flow(self, contract_data=None):
        """
        Ejecuta el flujo completo de deployment
        
        Args:
            contract_data: Datos adicionales del contrato
            
        Returns:
            dict: Resultado del deployment con transaction hash
        """
        print("=" * 70)
        print("AUTOMATIZACIÓN DE DEPLOYMENT EN STELLAR TESTNET")
        print("=" * 70)
        
        try:
            # Paso 1: Crear payload
            print("\n[1/5] Creando payload de deployment...")
            payload = self.create_deployment_payload(contract_data)
            print(f"✓ Payload creado")
            
            # Paso 2: Enviar POST al deployer
            print("\n[2/5] Enviando solicitud al deployer service...")
            deployer_response = self.post_to_deployer(payload)
            
            # Extraer XDR de la respuesta
            xdr_string = deployer_response.get('xdr')
            if not xdr_string:
                raise Exception("La respuesta del deployer no contiene un campo 'xdr'")
            
            print(f"✓ XDR recibido (primeros 50 chars): {xdr_string[:50]}...")
            
            # Paso 3: Firmar XDR
            print("\n[3/5] Firmando XDR...")
            signed_xdr = self.sign_xdr(xdr_string)
            print(f"✓ XDR firmado")
            
            # Paso 4: Enviar XDR firmado
            print("\n[4/5] Enviando XDR firmado...")
            submit_response = self.submit_signed_xdr(signed_xdr)
            
            # Extraer transaction hash
            tx_hash = submit_response.get('hash') or submit_response.get('transaction_hash')
            if not tx_hash:
                raise Exception("La respuesta no contiene un transaction hash")
            
            print(f"✓ Transaction Hash: {tx_hash}")
            
            # Paso 5: Validar en Stellar Expert (opcional)
            expert_url = None
            if self.enable_expert_validation:
                print("\n[5/5] Validando en Stellar Expert...")
                expert_url = self.validate_on_stellar_expert(tx_hash)
            else:
                print("\n[5/5] Validación en Stellar Expert deshabilitada")
            
            # Resultado final
            result = {
                'success': True,
                'transaction_hash': tx_hash,
                'stellar_expert_url': expert_url,
                'deployer_response': deployer_response,
                'submit_response': submit_response
            }
            
            print("\n" + "=" * 70)
            print("✓ DEPLOYMENT COMPLETADO EXITOSAMENTE")
            print("=" * 70)
            print(f"\nTransaction Hash: {tx_hash}")
            if expert_url:
                print(f"Stellar Expert: {expert_url}")
            
            return result
            
        except Exception as e:
            print(f"\n✗ Error durante el deployment: {e}")
            raise


def main():
    """Función principal para ejecutar el script"""
    print("Stellar Testnet Deployment Automation")
    print("Version 1.0.0\n")
    
    # Permitir especificar archivo .env como argumento
    env_file = sys.argv[1] if len(sys.argv) > 1 else '.env'
    
    try:
        # Inicializar automatización
        automation = StellarDeploymentAutomation(env_file=env_file)
        
        # Ejemplo de datos de contrato (personalizar según necesidad)
        contract_data = {
            # Agregar datos específicos del contrato aquí
            # "contractName": "example-contract",
            # "wasmHash": "...",
            # etc.
        }
        
        # Ejecutar flujo de deployment
        result = automation.run_deployment_flow(contract_data)
        
        # Guardar resultado en archivo
        with open('deployment_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n✓ Resultado guardado en: deployment_result.json")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
