# Stellar Testnet Deployment Automation

Script de automatización en Python para simplificar el flujo de deployment de contratos Soroban en Stellar Testnet.

## Descripción

Esta herramienta automatiza el proceso completo de deployment que normalmente requiere múltiples pasos manuales:

1. ✅ Carga automática de configuración desde archivo `.env`
2. ✅ POST al endpoint `deployer/single-release` con los parámetros configurados
3. ✅ Firma segura del XDR recibido usando Stellar SDK
4. ✅ Envío del XDR firmado y procesamiento del transaction hash
5. ✅ Validación opcional en Stellar Expert

## Características

- **🔒 Seguridad**: Manejo seguro de claves privadas mediante dotenv
- **📦 Modular**: Arquitectura modular para fácil extensión
- **⚡ Automatización**: Reduce pasos manuales al mínimo
- **🛡️ Validación**: Validación automática de configuración y XDR
- **📊 Logging**: Mensajes claros de progreso y errores
- **💾 Persistencia**: Guarda resultados en JSON para auditoría

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Navegar al directorio del proyecto:**

```bash
cd stellar-deployment-automation
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## Configuración

1. **Copiar el archivo de ejemplo:**

```bash
cp .env.example .env
```

2. **Editar `.env` con tus valores:**

```env
# REQUERIDO: Tu clave secreta de Stellar
STELLAR_SECRET_KEY=S...TU_SECRET_KEY_AQUI

# URL del servicio de deployment
DEPLOYER_SERVICE_URL=https://api.example.com/deployer

# Direcciones de cuenta
SIGNER_ADDRESS=G...TU_CLAVE_PUBLICA_AQUI
SERVICE_PROVIDER_ADDRESS=G...SERVICE_PROVIDER_ADDRESS_AQUI
PLATFORM_ADDRESS=G...PLATFORM_ADDRESS_AQUI

# Configuración de red (valores por defecto para testnet)
RPC_URL=https://soroban-testnet.stellar.org
NETWORK_PASSPHRASE=Test SDF Network ; September 2015

# Validación en Stellar Expert (opcional)
ENABLE_STELLAR_EXPERT_VALIDATION=true
STELLAR_EXPERT_URL=https://stellar.expert/explorer/testnet
```

### Variables de Entorno

| Variable | Requerida | Descripción | Valor por Defecto |
|----------|-----------|-------------|-------------------|
| `STELLAR_SECRET_KEY` | ✅ Sí | Secret key de tu cuenta Stellar | - |
| `DEPLOYER_SERVICE_URL` | ⚠️ Sí* | URL del servicio de deployment | `https://api.example.com/deployer` |
| `SIGNER_ADDRESS` | ⬜ No | Dirección del firmante | Derivada de `STELLAR_SECRET_KEY` |
| `SERVICE_PROVIDER_ADDRESS` | ⬜ No | Dirección del proveedor de servicios | `""` |
| `PLATFORM_ADDRESS` | ⬜ No | Dirección de la plataforma | `""` |
| `RPC_URL` | ⬜ No | URL del RPC de Soroban | `https://soroban-testnet.stellar.org` |
| `NETWORK_PASSPHRASE` | ⬜ No | Network passphrase | `Test SDF Network ; September 2015` |
| `ENABLE_STELLAR_EXPERT_VALIDATION` | ⬜ No | Validar en Stellar Expert | `true` |
| `STELLAR_EXPERT_URL` | ⬜ No | URL base de Stellar Expert | `https://stellar.expert/explorer/testnet` |

\* *Debes cambiar `DEPLOYER_SERVICE_URL` a la URL real de tu servicio de deployment*

## Uso

### Opción 1: Script Unificado (Recomendado para uso simple)

```bash
python deploy_automation.py
```

O especificar un archivo `.env` diferente:

```bash
python deploy_automation.py .env.production
```

### Opción 2: Script Modular (Recomendado para personalización)

```bash
python main.py
```

O con archivo `.env` personalizado:

```bash
python main.py .env.custom
```

### Salida Esperada

```
======================================================================
AUTOMATIZACIÓN DE DEPLOYMENT EN STELLAR TESTNET
======================================================================

Usando archivo de configuración: .env

Cargando configuración...
✓ Configuración cargada correctamente
Signer: GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Network: Test SDF Network ; September 2015

[1/5] Creando payload de deployment...
Payload: {
  "signer": "GXXXXX...",
  "serviceProvider": "GXXXXX...",
  "platformAddress": "GXXXXX..."
}
✓ Payload creado

[2/5] Enviando solicitud al deployer service...
Endpoint: https://api.example.com/deployer/single-release
✓ XDR recibido (primeros 50 chars): AAAAAgAAAABkZXBsb3llci10ZXN0AAAAAAAAAAEAAAAA...

[3/5] Firmando XDR...
✓ XDR firmado exitosamente

[4/5] Enviando XDR firmado...
✓ Transaction Hash: abc123def456...

[5/5] Validando en Stellar Expert...
✓ Transacción encontrada en Stellar Expert
URL: https://stellar.expert/explorer/testnet/tx/abc123def456...

======================================================================
✓ DEPLOYMENT COMPLETADO EXITOSAMENTE
======================================================================

Transaction Hash: abc123def456...
Stellar Expert: https://stellar.expert/explorer/testnet/tx/abc123def456...
✓ Resultado guardado en: deployment_result.json
```

## Estructura del Proyecto

```
stellar-deployment-automation/
├── main.py                    # Script principal modular
├── deploy_automation.py       # Script unificado (alternativa)
├── config.py                  # Módulo de configuración
├── stellar_utils.py           # Utilidades de Stellar (firma XDR, validación)
├── requirements.txt           # Dependencias de Python
├── .env.example              # Template de configuración
├── .env                      # Tu configuración (no commitear)
└── README.md                 # Esta documentación
```

## Arquitectura Modular

### `config.py`
- Carga y valida variables de entorno
- Valida formato de secret keys
- Proporciona valores por defecto seguros

### `stellar_utils.py`
- **`StellarUtils`**: Firma XDR, validación de formato
- **`DeployerClient`**: Cliente HTTP para el deployer service
- **`StellarExpertValidator`**: Validación de transacciones en Stellar Expert

### `main.py`
- Orquesta el flujo completo
- Manejo de errores robusto
- Logging detallado de progreso

### `deploy_automation.py`
- Versión unificada con toda la lógica en un solo archivo
- Ideal para deployments donde se necesita un solo script

## Personalización

### Agregar Datos de Contrato

Edita `main.py` y personaliza el diccionario `contract_data`:

```python
contract_data = {
    "contractName": "mi-contrato",
    "wasmHash": "abc123...",
    "initArgs": {
        "arg1": "valor1",
        "arg2": 123
    }
}
```

### Cambiar Endpoint de Submission

Por defecto usa `/submit`. Para cambiarlo:

```python
# En stellar_utils.py, método submit_signed_xdr
deployer.submit_signed_xdr(signed_xdr, endpoint_path='/custom-submit')
```

### Deshabilitar Validación en Stellar Expert

En tu archivo `.env`:

```env
ENABLE_STELLAR_EXPERT_VALIDATION=false
```

## Resultado del Deployment

El script guarda un archivo `deployment_result.json` con:

```json
{
  "success": true,
  "transaction_hash": "abc123def456...",
  "stellar_expert_url": "https://stellar.expert/explorer/testnet/tx/abc123...",
  "deployer_response": {
    "xdr": "...",
    "...": "..."
  },
  "submit_response": {
    "hash": "abc123def456...",
    "...": "..."
  }
}
```

## Seguridad

### ⚠️ IMPORTANTE: Protección de Claves Privadas

1. **Nunca** commits el archivo `.env` al control de versiones
2. El archivo `.gitignore` debe incluir `.env`
3. Usa permisos restrictivos en el archivo `.env`:

```bash
chmod 600 .env
```

4. Para producción, considera usar:
   - Gestores de secretos (AWS Secrets Manager, HashiCorp Vault)
   - Variables de entorno del sistema
   - Hardware Security Modules (HSM)

### Mejores Prácticas

- ✅ Usa cuentas de testnet para pruebas
- ✅ Verifica siempre el transaction hash en Stellar Expert
- ✅ Guarda los archivos `deployment_result.json` para auditoría
- ✅ Valida los datos antes de firmar transacciones
- ✅ Usa HTTPS para todas las comunicaciones

## Troubleshooting

### Error: "STELLAR_SECRET_KEY es requerido"

**Solución**: Asegúrate de tener un archivo `.env` con la variable `STELLAR_SECRET_KEY` configurada.

### Error: "STELLAR_SECRET_KEY inválido"

**Solución**: Verifica que tu secret key comience con `S` y tenga el formato correcto.

### Error: "Error al conectar con el deployer service"

**Solución**: 
- Verifica que `DEPLOYER_SERVICE_URL` sea correcta
- Comprueba tu conexión a internet
- Verifica que el servicio esté disponible

### Error: "Error al firmar XDR"

**Solución**: 
- Verifica que el XDR recibido sea válido
- Comprueba que `NETWORK_PASSPHRASE` corresponda a testnet

### La transacción no aparece en Stellar Expert

**Solución**: 
- Espera unos segundos (puede tardar en indexarse)
- Verifica el transaction hash manualmente en Stellar Expert
- Comprueba el estado de la red Stellar testnet

## Extensiones Futuras

Posibles mejoras para el script:

- [ ] Soporte para múltiples contratos en batch
- [ ] Retry automático en caso de fallos temporales
- [ ] Integración con CI/CD
- [ ] Notificaciones (email, Slack, etc.)
- [ ] Validación de balances antes de deployment
- [ ] Logging a archivo con rotación
- [ ] Métricas de performance
- [ ] Soporte para mainnet con confirmación adicional

## Recursos Relacionados

- [Stellar SDK Python Documentation](https://stellar-sdk.readthedocs.io/)
- [Stellar Testnet](https://laboratory.stellar.org/)
- [Stellar Expert](https://stellar.expert/)
- [Soroban Documentation](https://soroban.stellar.org/)

## Soporte

Para reportar problemas o sugerencias, por favor contacta al equipo de desarrollo o crea un issue en el repositorio.

## Licencia

Proyecto educativo desarrollado para el Bootcamp de Impacta.
