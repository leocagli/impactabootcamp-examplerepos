#!/usr/bin/env python3
"""
Script principal para automatización de deployment en Stellar Testnet

Uso:
    python main.py [archivo_env]
    
Ejemplo:
    python main.py .env
"""

import sys
import json
from config import DeploymentConfig
from stellar_utils import StellarUtils, DeployerClient, StellarExpertValidator


def print_header():
    """Imprime el encabezado del script"""
    print("=" * 70)
    print("AUTOMATIZACIÓN DE DEPLOYMENT EN STELLAR TESTNET")
    print("=" * 70)
    print()


def print_step(step_num, total_steps, description):
    """Imprime información de un paso"""
    print(f"\n[{step_num}/{total_steps}] {description}")


def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✓ {message}")


def print_error(message):
    """Imprime mensaje de error"""
    print(f"✗ {message}")


def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"⚠ {message}")


def run_deployment(config, contract_data=None):
    """
    Ejecuta el flujo completo de deployment
    
    Args:
        config: Objeto DeploymentConfig
        contract_data: Datos adicionales del contrato (dict)
        
    Returns:
        dict: Resultado del deployment
    """
    if contract_data is None:
        contract_data = {}
    
    # Inicializar clientes
    deployer = DeployerClient(config.deployer_url)
    validator = StellarExpertValidator(config.stellar_expert_url)
    
    try:
        # Paso 1: Crear payload
        print_step(1, 5, "Creando payload de deployment...")
        payload = {
            "signer": config.signer_address,
            "serviceProvider": config.service_provider,
            "platformAddress": config.platform_address,
            **contract_data
        }
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print_success("Payload creado")
        
        # Paso 2: Enviar POST al deployer
        print_step(2, 5, "Enviando solicitud al deployer service...")
        print(f"Endpoint: {config.deployer_url}/single-release")
        deployer_response = deployer.post_single_release(payload)
        
        # Extraer XDR
        xdr_string = deployer_response.get('xdr')
        if not xdr_string:
            raise Exception("La respuesta del deployer no contiene campo 'xdr'")
        
        print_success(f"XDR recibido (primeros 50 chars): {xdr_string[:50]}...")
        
        # Paso 3: Firmar XDR
        print_step(3, 5, "Firmando XDR...")
        signed_xdr = StellarUtils.sign_xdr(
            xdr_string,
            config.keypair,
            config.network_passphrase
        )
        print_success("XDR firmado exitosamente")
        
        # Paso 4: Enviar XDR firmado
        print_step(4, 5, "Enviando XDR firmado...")
        submit_response = deployer.submit_signed_xdr(signed_xdr)
        
        # Extraer transaction hash
        tx_hash = submit_response.get('hash') or submit_response.get('transaction_hash')
        if not tx_hash:
            raise Exception("La respuesta no contiene transaction hash")
        
        print_success(f"Transaction Hash: {tx_hash}")
        
        # Paso 5: Validar en Stellar Expert (opcional)
        expert_url = None
        if config.enable_expert_validation:
            print_step(5, 5, "Validando en Stellar Expert...")
            exists, expert_url = validator.validate_transaction(tx_hash)
            
            if exists:
                print_success("Transacción encontrada en Stellar Expert")
            else:
                print_warning("Transacción no encontrada aún (puede tardar unos segundos)")
            
            print(f"URL: {expert_url}")
        else:
            print_step(5, 5, "Validación en Stellar Expert deshabilitada")
        
        # Resultado
        result = {
            'success': True,
            'transaction_hash': tx_hash,
            'stellar_expert_url': expert_url,
            'deployer_response': deployer_response,
            'submit_response': submit_response
        }
        
        # Resumen final
        print("\n" + "=" * 70)
        print("✓ DEPLOYMENT COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        print(f"\nTransaction Hash: {tx_hash}")
        if expert_url:
            print(f"Stellar Expert: {expert_url}")
        
        return result
        
    except Exception as e:
        print_error(f"Error durante el deployment: {e}")
        raise


def save_result(result, filename='deployment_result.json'):
    """
    Guarda el resultado del deployment en un archivo JSON
    
    Args:
        result: Diccionario con el resultado
        filename: Nombre del archivo de salida
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print_success(f"Resultado guardado en: {filename}")
    except Exception as e:
        print_warning(f"No se pudo guardar el resultado: {e}")


def main():
    """Función principal"""
    print_header()
    
    # Obtener archivo .env desde argumentos
    env_file = sys.argv[1] if len(sys.argv) > 1 else '.env'
    print(f"Usando archivo de configuración: {env_file}\n")
    
    try:
        # Cargar configuración
        print("Cargando configuración...")
        config = DeploymentConfig(env_file=env_file)
        print_success("Configuración cargada correctamente")
        print(f"Signer: {config.signer_address}")
        print(f"Network: {config.network_passphrase}")
        
        # Datos del contrato (personalizar según necesidad)
        contract_data = {
            # Agregar datos específicos del contrato aquí
            # Ejemplo:
            # "contractName": "example-contract",
            # "wasmHash": "abc123...",
            # "initArgs": {...}
        }
        
        # Ejecutar deployment
        result = run_deployment(config, contract_data)
        
        # Guardar resultado
        save_result(result)
        
        return 0
        
    except ValueError as e:
        print_error(f"Error de configuración: {e}")
        print("\nAsegúrate de tener un archivo .env válido.")
        print("Puedes copiar .env.example y configurarlo con tus valores.")
        return 1
        
    except Exception as e:
        print_error(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
