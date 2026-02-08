#!/usr/bin/env python3
"""
Ejemplo de uso del script de automatización de deployment

Este script muestra cómo usar la automatización de deployment
con datos de contrato personalizados.
"""

import sys
from config import DeploymentConfig
from stellar_utils import StellarUtils, DeployerClient, StellarExpertValidator


def example_simple_deployment():
    """
    Ejemplo básico: Deployment simple sin datos adicionales
    """
    print("=== Ejemplo 1: Deployment Simple ===\n")
    
    # Cargar configuración
    config = DeploymentConfig('.env')
    
    # Crear clientes
    deployer = DeployerClient(config.deployer_url)
    
    # Payload mínimo
    payload = {
        "signer": config.signer_address,
        "serviceProvider": config.service_provider,
        "platformAddress": config.platform_address
    }
    
    print(f"Payload: {payload}")
    print("\nEjecutando deployment...")
    
    # Nota: Descomenta las siguientes líneas para ejecutar realmente
    # response = deployer.post_single_release(payload)
    # print(f"Respuesta: {response}")


def example_contract_with_metadata():
    """
    Ejemplo avanzado: Deployment con metadatos del contrato
    """
    print("=== Ejemplo 2: Deployment con Metadatos ===\n")
    
    # Cargar configuración
    config = DeploymentConfig('.env')
    
    # Crear clientes
    deployer = DeployerClient(config.deployer_url)
    
    # Payload con metadatos adicionales
    payload = {
        "signer": config.signer_address,
        "serviceProvider": config.service_provider,
        "platformAddress": config.platform_address,
        # Metadatos personalizados del contrato
        "contractName": "products-contract",
        "version": "1.0.0",
        "wasmHash": "abc123def456...",
        "initArgs": {
            "owner": config.signer_address,
            "initialSupply": 1000000
        }
    }
    
    print(f"Payload: {payload}")
    print("\nEjecutando deployment...")
    
    # Nota: Descomenta las siguientes líneas para ejecutar realmente
    # response = deployer.post_single_release(payload)
    # print(f"Respuesta: {response}")


def example_full_workflow():
    """
    Ejemplo completo: Flujo completo con firma y validación
    """
    print("=== Ejemplo 3: Flujo Completo ===\n")
    
    # Cargar configuración
    config = DeploymentConfig('.env')
    
    # Simular un XDR de ejemplo (en producción vendría del deployer)
    example_xdr = "AAAAAgAAAABkZXBsb3llci10ZXN0..."
    
    print("1. Firmar XDR:")
    # signed_xdr = StellarUtils.sign_xdr(
    #     example_xdr,
    #     config.keypair,
    #     config.network_passphrase
    # )
    # print(f"   XDR firmado: {signed_xdr[:50]}...")
    print("   (Simulado)")
    
    print("\n2. Validar en Stellar Expert:")
    validator = StellarExpertValidator(config.stellar_expert_url)
    example_hash = "abc123def456..."
    url = validator.get_transaction_url(example_hash)
    print(f"   URL: {url}")
    
    # exists, url = validator.validate_transaction(example_hash)
    # print(f"   Existe: {exists}")
    print("   (Simulado)")


def example_batch_deployment():
    """
    Ejemplo avanzado: Deployment en batch de múltiples contratos
    """
    print("=== Ejemplo 4: Deployment en Batch ===\n")
    
    # Cargar configuración
    config = DeploymentConfig('.env')
    deployer = DeployerClient(config.deployer_url)
    
    # Lista de contratos a desplegar
    contracts = [
        {
            "name": "products-contract",
            "wasmHash": "hash1...",
        },
        {
            "name": "users-contract",
            "wasmHash": "hash2...",
        },
        {
            "name": "payments-contract",
            "wasmHash": "hash3...",
        }
    ]
    
    print(f"Contratos a desplegar: {len(contracts)}")
    
    for i, contract in enumerate(contracts, 1):
        print(f"\n[{i}/{len(contracts)}] Desplegando: {contract['name']}")
        
        payload = {
            "signer": config.signer_address,
            "serviceProvider": config.service_provider,
            "platformAddress": config.platform_address,
            **contract
        }
        
        print(f"   Payload: {payload}")
        # response = deployer.post_single_release(payload)
        # ... procesar respuesta
        print("   (Simulado)")


def main():
    """Función principal con menú de ejemplos"""
    print("=" * 70)
    print("EJEMPLOS DE USO - Stellar Deployment Automation")
    print("=" * 70)
    print()
    
    examples = {
        '1': ('Deployment Simple', example_simple_deployment),
        '2': ('Deployment con Metadatos', example_contract_with_metadata),
        '3': ('Flujo Completo', example_full_workflow),
        '4': ('Deployment en Batch', example_batch_deployment),
    }
    
    print("Selecciona un ejemplo:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. Salir")
    
    choice = input("\nOpción: ").strip()
    
    if choice == 'q':
        print("Saliendo...")
        return 0
    
    if choice in examples:
        print()
        _, example_func = examples[choice]
        try:
            example_func()
            print("\n✓ Ejemplo completado")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    else:
        print("Opción inválida")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
