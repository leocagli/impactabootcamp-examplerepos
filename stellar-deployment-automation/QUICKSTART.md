# Guía de Inicio Rápido - Stellar Deployment Automation

Esta guía te ayudará a configurar y ejecutar la automatización de deployment en menos de 5 minutos.

## Prerrequisitos

- Python 3.8 o superior instalado
- Una cuenta de Stellar Testnet con fondos
- Secret key de tu cuenta Stellar

## Pasos de Configuración

### 1. Instalar Dependencias

```bash
cd stellar-deployment-automation
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` con tu editor favorito y configura al menos:

```env
# REQUERIDO
STELLAR_SECRET_KEY=SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# RECOMENDADO (cambiar la URL al servicio real)
DEPLOYER_SERVICE_URL=https://tu-servicio-deployer.com/deployer
```

### 3. Ejecutar el Script

#### Opción A: Script Simple (Todo en uno)

```bash
python deploy_automation.py
```

#### Opción B: Script Modular (Recomendado)

```bash
python main.py
```

## Verificación Rápida

Para verificar que todo está configurado correctamente, ejecuta los tests:

```bash
python test_automation.py
```

Deberías ver:

```
======================================================================
TESTS DE VERIFICACIÓN - Stellar Deployment Automation
======================================================================

=== Test: Módulo de Configuración ===
✓ Configuración cargada correctamente

=== Test: Utilidades de Stellar ===
✓ DeployerClient inicializado
✓ StellarExpertValidator inicializado

=== Test: Validación de Secret Key Inválida ===
✓ Secret key inválida detectada correctamente

=== Test: Configuración Requerida Faltante ===
✓ Configuración faltante detectada correctamente

Total: 4/4 tests pasaron
```

## Ejemplo de Uso

Ver ejemplos interactivos ejecutando:

```bash
python examples.py
```

## Obtener una Cuenta de Testnet

Si no tienes una cuenta de Stellar Testnet:

1. Visita [Stellar Laboratory](https://laboratory.stellar.org/#account-creator?network=test)
2. Genera un nuevo keypair
3. Fondea tu cuenta con XLM de testnet usando el botón "Fund with Friendbot"
4. Copia tu Secret Key (comienza con 'S') al archivo `.env`

## Siguiente Paso

Lee el [README.md](README.md) completo para:
- Personalizar datos del contrato
- Configurar validación en Stellar Expert
- Extender el script para tus necesidades
- Troubleshooting de problemas comunes

## Soporte

Si encuentras problemas:

1. Verifica que tu secret key comience con 'S'
2. Asegúrate de que el archivo `.env` existe y tiene permisos correctos
3. Revisa que `DEPLOYER_SERVICE_URL` apunte al servicio correcto
4. Consulta la sección de Troubleshooting en el README principal

## Seguridad

⚠️ **IMPORTANTE**: 
- Nunca compartas tu `STELLAR_SECRET_KEY`
- Nunca commits el archivo `.env` al repositorio
- Usa cuentas de testnet para pruebas
- Para producción, considera usar gestores de secretos

---

¡Listo! Ahora estás preparado para automatizar tus deployments en Stellar Testnet.
