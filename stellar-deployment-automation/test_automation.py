#!/usr/bin/env python3
"""
Tests básicos para verificar la funcionalidad de los módulos

Estos tests no requieren conexión a servicios externos
y verifican la lógica de configuración y utilidades.
"""

import os
import sys
import tempfile
from pathlib import Path


def test_config_module():
    """Test básico del módulo config.py"""
    print("\n=== Test: Módulo de Configuración ===")
    
    # Crear un archivo .env temporal con una secret key válida (generada para testing)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        # Esta es una secret key de prueba válida (generada aleatoriamente, no usar en producción)
        f.write("STELLAR_SECRET_KEY=SDTFMA4SJWHOCQWMGQM2YTE622P3MTOUEX4BXTYNDZW5BILJSZ4YAGS5\n")
        f.write("DEPLOYER_SERVICE_URL=https://test.example.com/deployer\n")
        f.write("ENABLE_STELLAR_EXPERT_VALIDATION=true\n")
        env_file = f.name
    
    try:
        from config import DeploymentConfig
        
        # Cargar configuración
        config = DeploymentConfig(env_file)
        
        # Verificar que se cargó correctamente
        assert config.deployer_url == "https://test.example.com/deployer"
        assert config.enable_expert_validation == True
        assert config.keypair is not None
        assert config.signer_address is not None
        
        print("✓ Configuración cargada correctamente")
        print(f"  - Deployer URL: {config.deployer_url}")
        print(f"  - Signer: {config.signer_address[:10]}...")
        print(f"  - Expert validation: {config.enable_expert_validation}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
        
    finally:
        # Limpiar archivo temporal
        os.unlink(env_file)


def test_stellar_utils():
    """Test básico del módulo stellar_utils.py"""
    print("\n=== Test: Utilidades de Stellar ===")
    
    try:
        from stellar_utils import StellarUtils, DeployerClient, StellarExpertValidator
        
        # Test DeployerClient
        client = DeployerClient("https://test.example.com/deployer")
        assert client.base_url == "https://test.example.com/deployer"
        print("✓ DeployerClient inicializado")
        
        # Test StellarExpertValidator
        validator = StellarExpertValidator("https://stellar.expert/explorer/testnet")
        url = validator.get_transaction_url("abc123")
        assert "abc123" in url
        print("✓ StellarExpertValidator inicializado")
        print(f"  - Transaction URL: {url}")
        
        # Test get_contract_url
        contract_url = validator.get_contract_url("CONTRACT123")
        assert "CONTRACT123" in contract_url
        print(f"  - Contract URL: {contract_url}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_invalid_secret_key():
    """Test que la validación de secret key funciona"""
    print("\n=== Test: Validación de Secret Key Inválida ===")
    
    # Limpiar variables de entorno para evitar caché de dotenv
    for key in ['STELLAR_SECRET_KEY', 'DEPLOYER_SERVICE_URL', 'ENABLE_STELLAR_EXPERT_VALIDATION']:
        os.environ.pop(key, None)
    
    # Crear un archivo .env con secret key inválida
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("STELLAR_SECRET_KEY=INVALID_KEY\n")
        env_file = f.name
    
    try:
        from config import DeploymentConfig
        
        # Esto debería lanzar una excepción
        exception_caught = False
        try:
            print("  Intentando crear config con secret key inválida...")
            config = DeploymentConfig(env_file)
            print(f"  Config creado: {config is not None}")
        except Exception as e:
            exception_caught = True
            # Aceptar cualquier excepción que indique secret key inválido
            error_msg = str(e).lower()
            print(f"  Excepción capturada: {type(e).__name__}")
            if "secret" in error_msg or "invalid" in error_msg or "inválido" in error_msg:
                print(f"✓ Secret key inválida detectada correctamente")
                return True
            else:
                print(f"✗ Excepción inesperada: {e}")
                return False
        
        if not exception_caught:
            print("✗ No se lanzó ninguna excepción - la validación falló")
            return False
            
    except Exception as e:
        print(f"✗ Error inesperado fuera del scope: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if os.path.exists(env_file):
            os.unlink(env_file)
        # Limpiar environment variable
        os.environ.pop('STELLAR_SECRET_KEY', None)


def test_missing_required_config():
    """Test que se detecta configuración faltante"""
    print("\n=== Test: Configuración Requerida Faltante ===")
    
    # Limpiar variables de entorno para evitar caché de dotenv
    for key in ['STELLAR_SECRET_KEY', 'DEPLOYER_SERVICE_URL', 'ENABLE_STELLAR_EXPERT_VALIDATION']:
        os.environ.pop(key, None)
    
    # Crear un archivo .env sin STELLAR_SECRET_KEY
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("DEPLOYER_SERVICE_URL=https://test.example.com\n")
        env_file = f.name
    
    try:
        from config import DeploymentConfig
        
        # Esto debería lanzar una excepción
        exception_caught = False
        try:
            print("  Intentando crear config sin STELLAR_SECRET_KEY...")
            config = DeploymentConfig(env_file)
            print(f"  Config creado: {config is not None}")
        except Exception as e:
            exception_caught = True
            # Aceptar cualquier excepción que indique configuración faltante o clave requerida
            error_msg = str(e).lower()
            print(f"  Excepción capturada: {type(e).__name__}")
            if "requerido" in error_msg or "required" in error_msg or "secret_key" in error_msg:
                print(f"✓ Configuración faltante detectada correctamente")
                return True
            else:
                print(f"✗ Excepción inesperada: {e}")
                return False
        
        if not exception_caught:
            print("✗ No se lanzó ninguna excepción - la validación falló")
            return False
            
    except Exception as e:
        print(f"✗ Error inesperado fuera del scope: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if os.path.exists(env_file):
            os.unlink(env_file)
        # No hay necesidad de limpiar STELLAR_SECRET_KEY ya que no existe


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("TESTS DE VERIFICACIÓN - Stellar Deployment Automation")
    print("=" * 70)
    
    tests = [
        ("Módulo de Configuración", test_config_module),
        ("Utilidades de Stellar", test_stellar_utils),
        ("Validación de Secret Key Inválida", test_invalid_secret_key),
        ("Configuración Requerida Faltante", test_missing_required_config),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' falló con excepción: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests pasaron")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
