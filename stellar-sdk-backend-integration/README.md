# Stellar SDK Backend Integration

Backend REST API desarrollado en Node.js/Express que se integra con un contrato inteligente Soroban en la red Stellar para la gestión de productos.

## Descripcion

Este proyecto es una API REST que actua como intermediario entre aplicaciones cliente y un smart contract desplegado en Soroban (la plataforma de contratos inteligentes de Stellar). Permite realizar operaciones CRUD sobre productos almacenados en la blockchain.

### Funcionalidades principales

- **Registrar productos**: Crear nuevos productos en el contrato con nombre, descripcion, precio y stock inicial
- **Consultar productos**: Obtener información de un producto por su ID
- **Actualizar stock**: Incrementar o decrementar el inventario de un producto
- **Actualizar precio**: Modificar el precio de un producto existente
- **Desplegar contratos**: Generar y enviar XDRs para desplegar contratos de escrow/milestone con USDC

## Tecnologias

- **Node.js** - Runtime de JavaScript
- **Express 5** - Framework web para la API REST
- **@stellar/stellar-sdk** - SDK oficial de Stellar para interactuar con Soroban
- **dotenv** - Manejo de variables de entorno

## Estructura del proyecto

```
stellar-sdk-backend-integration/
├── package.json
├── .env.example                                # Template de variables de entorno
├── .env                                         # Variables de entorno (no commitear)
├── Impacta-Bootcamp-Stellar.postman_collection.json  # Colección de Postman
└── src/
    ├── index.js                                # Punto de entrada del servidor Express
    ├── config/
    │   └── stellar.js                          # Configuracion del cliente Stellar/Soroban
    ├── routes/
    │   ├── products.js                         # Endpoints de la API de productos
    │   └── deployer.js                         # Endpoints para desplegar contratos
    └── types/
        └── product.js                          # Utilidades de formateo de productos
```

## Requisitos previos

- Node.js v18 o superior
- npm o yarn
- Una cuenta de Stellar con fondos en testnet
- Un contrato Soroban desplegado (ver proyecto `soroban-contract`)
- (Opcional) Postman para probar los endpoints más fácilmente

## Configurar Postman (Opcional)

1. Abrir Postman
2. Importar la colección: `File → Import → Seleccionar Impacta-Bootcamp-Stellar.postman_collection.json`
3. Configurar las variables de entorno:
   - `base_url`: `http://localhost:3000`
   - `signer`: Tu clave pública de Stellar
   - `serviceProvider`: Dirección del proveedor de servicio
   - `platformAddress`: Dirección de la plataforma
   - `releaseSigner`: Dirección del firmante de liberación
   - `receiver`: Dirección del receptor
4. Guardar las variables

Ahora puedes usar las requests pre-configuradas en la colección.

## Instalacion

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd stellar-sdk-backend-integration
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
```

4. Editar el archivo `.env` con tus credenciales:
```env
STELLAR_PUBLIC_KEY=tu_clave_publica
STELLAR_SECRET_KEY=tu_clave_secreta
CONTRACT_ID=id_del_contrato_desplegado
RPC_URL=https://soroban-testnet.stellar.org
NETWORK_PASSPHRASE=Test SDF Network ; September 2015
PORT=3000
```

## Ejecucion

### Modo desarrollo (con hot-reload)
```bash
npm run dev
```

### Modo produccion
```bash
npm start
```

El servidor estara disponible en `http://localhost:3000`

## Endpoints de la API

### Health Check
```
GET /health
```
Verifica que el servidor este funcionando.

**Respuesta:**
```json
{
  "status": "ok"
}
```

---

### Registrar producto
```
POST /products
```
Crea un nuevo producto en el contrato.

**Body (JSON):**
```json
{
  "name": "Laptop",
  "description": "Laptop gaming 16GB RAM",
  "price": 1500,
  "initial_stock": 10
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gaming 16GB RAM",
  "price": 1500,
  "stock": 10
}
```

---

### Obtener producto
```
GET /products/:id
```
Obtiene la informacion de un producto por su ID.

**Parametros:**
- `id` - ID numerico del producto

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gaming 16GB RAM",
  "price": 1500,
  "stock": 10
}
```

**Error (404):**
```json
{
  "error": "Producto no encontrado"
}
```

---

### Actualizar stock
```
PUT /products/:id/stock
```
Incrementa o decrementa el stock de un producto.

**Parametros:**
- `id` - ID numerico del producto

**Body (JSON):**
```json
{
  "quantity": 5,
  "operation": "add"
}
```
- `operation`: `"add"` para agregar stock, `"sub"` para restar

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gaming 16GB RAM",
  "price": 1500,
  "stock": 15
}
```

---

### Actualizar precio
```
PUT /products/:id/price
```
Modifica el precio de un producto.

**Parametros:**
- `id` - ID numerico del producto

**Body (JSON):**
```json
{
  "new_price": 1299
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gaming 16GB RAM",
  "price": 1299,
  "stock": 15
}
```

---

### Generar XDR para desplegar contrato (Bootcamp)
```
POST /deployer/single-release
```
Genera un XDR sin firmar para desplegar un contrato de escrow/milestone.

**Body (JSON):**
```json
{
  "signer": "{{signer}}",
  "engagementId": "Impacta-Bootcamp",
  "title": "Nombre: [Tu nombre aquí]",
  "description": "Descripcion personal: [Tu descripción]",
  "roles": {
    "approver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
    "serviceProvider": "{{serviceProvider}}",
    "platformAddress": "{{platformAddress}}",
    "releaseSigner": "{{releaseSigner}}",
    "disputeResolver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
    "receiver": "{{receiver}}"
  },
  "amount": 10,
  "platformFee": 1,
  "milestones": [ 
    { "description": "Meta 1" },
    { "description": "Meta 2" }
  ],
  "trustline": {
    "symbol": "USDC",
    "address": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5"
  }
}
```

**⚠️ CRÍTICO**: Las wallets `GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK` en `approver` y `disputeResolver` NO deben modificarse.

**Respuesta (200):**
```json
{
  "success": true,
  "xdr": "AAAAAgAAAAC...(XDR string)...==",
  "message": "Unsigned XDR generated successfully. Please sign it using Stellar Laboratory.",
  "details": {
    "engagementId": "Impacta-Bootcamp",
    "title": "Nombre: John Doe",
    "amount": 10,
    "platformFee": 1,
    "milestonesCount": 2,
    "network": "testnet",
    "requiresSignature": "G..."
  }
}
```

**Siguiente paso:** Ir a [Stellar Laboratory](https://laboratory.stellar.org/#txsigner?network=test), pegar el XDR y firmar con tu clave privada.

---

### Enviar XDR firmado
```
POST /deployer/submit
```
Envía el XDR firmado a la red Stellar.

**Body (JSON):**
```json
{
  "signedXdr": "AAAAAgAAAAC...(XDR firmado)...=="
}
```

**Respuesta (200):**
```json
{
  "success": true,
  "transactionHash": "abc123...",
  "status": "SUCCESS",
  "message": "Transaction submitted successfully! Verify on Stellar Expert.",
  "stellarExpertUrl": "https://stellar.expert/explorer/testnet/tx/abc123..."
}
```

**Verificación:** Usa el link de Stellar Expert para verificar que el contrato se desplegó correctamente.

---

## Ejemplos con cURL

```bash
# Health check
curl http://localhost:3000/health

# Registrar producto
curl -X POST http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Gaming laptop","price":1500,"initial_stock":10}'

# Obtener producto
curl http://localhost:3000/products/1

# Agregar stock
curl -X PUT http://localhost:3000/products/1/stock \
  -H "Content-Type: application/json" \
  -d '{"quantity":5,"operation":"add"}'

# Actualizar precio
curl -X PUT http://localhost:3000/products/1/price \
  -H "Content-Type: application/json" \
  -d '{"new_price":1299}'

# Generar XDR para desplegar contrato
curl -X POST http://localhost:3000/deployer/single-release \
  -H "Content-Type: application/json" \
  -d '{
    "signer": "TU_CLAVE_PUBLICA",
    "engagementId": "Impacta-Bootcamp",
    "title": "Nombre: Juan Perez",
    "description": "Descripcion personal: Desarrollador Stellar",
    "roles": {
      "approver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
      "serviceProvider": "TU_SERVICE_PROVIDER",
      "platformAddress": "TU_PLATFORM_ADDRESS",
      "releaseSigner": "TU_RELEASE_SIGNER",
      "disputeResolver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
      "receiver": "TU_RECEIVER"
    },
    "amount": 10,
    "platformFee": 1,
    "milestones": [
      { "description": "Meta 1" },
      { "description": "Meta 2" }
    ],
    "trustline": {
      "symbol": "USDC",
      "address": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5"
    }
  }'

# Enviar XDR firmado
curl -X POST http://localhost:3000/deployer/submit \
  -H "Content-Type: application/json" \
  -d '{"signedXdr":"TU_XDR_FIRMADO_AQUI"}'
```

## Como funciona la integracion con Stellar

1. El backend recibe una peticion HTTP
2. El route handler extrae los parametros de la peticion
3. Se obtiene el cliente de contrato Soroban (cacheado para eficiencia)
4. Se invoca el metodo correspondiente del contrato con los parametros convertidos a los tipos correctos (BigInt para numeros en blockchain)
5. La transaccion se firma y envia a la red
6. El resultado se formatea y se devuelve al cliente

## Notas importantes

- **Seguridad**: El archivo `.env` contiene claves privadas sensibles. Nunca lo subas a control de versiones.
- **Red de pruebas**: Por defecto esta configurado para la testnet de Soroban. Para produccion, cambiar `RPC_URL` y `NETWORK_PASSPHRASE`.
- **Tiempos de respuesta**: Las operaciones de blockchain pueden tomar varios segundos debido a la confirmacion de transacciones.

## Proyecto relacionado

Este backend esta disenado para trabajar con el contrato inteligente ubicado en `../soroban-contract/`. Consulta su README para instrucciones de despliegue del contrato.

---

## Guía completa del Bootcamp: Despliegue de Contratos

### Paso 1: Configurar tu wallet con USDC en Stellar Testnet

1. **Crear o usar tu wallet de Stellar testnet**:
   - Ve a [Stellar Laboratory](https://laboratory.stellar.org/#account-creator?network=test)
   - Genera un nuevo keypair o usa uno existente
   - Guarda tu clave pública (G...) y clave secreta (S...)

2. **Añadir una trustline para USDC**:
   - Ve a [Stellar Laboratory - Build Transaction](https://laboratory.stellar.org/#txbuilder?network=test)
   - Ingresa tu cuenta fuente
   - Selecciona "Change Trust"
   - Asset Code: `USDC`
   - Issuer: `GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5`
   - Firma y envía la transacción

3. **Solicitar USDC de testnet**:
   - Ve al [Stellar USDC Faucet](https://faucet.stellar.org/)
   - O envía un payment manual desde una cuenta con USDC

### Paso 2: Configurar Postman

1. Importa la colección `Impacta-Bootcamp-Stellar.postman_collection.json`
2. Configura las variables de entorno:
   - `signer`: Tu clave pública (G...)
   - `serviceProvider`: Tu dirección o la de otro participante
   - `platformAddress`: Dirección de la plataforma
   - `releaseSigner`: Dirección del firmante
   - `receiver`: Dirección que recibirá los fondos

### Paso 3: Iniciar el servidor

```bash
npm run dev
```

El servidor estará disponible en `http://localhost:3000`

### Paso 4: Llamar al endpoint deployer/single-release

Usa Postman o cURL para enviar una petición POST a `/deployer/single-release` con tus datos personales:

```json
{
  "signer": "{{signer}}",
  "engagementId": "Impacta-Bootcamp",
  "title": "Nombre: Juan Pérez",
  "description": "Descripcion personal: Desarrollador blockchain",
  "roles": {
    "approver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
    "serviceProvider": "{{serviceProvider}}",
    "platformAddress": "{{platformAddress}}",
    "releaseSigner": "{{releaseSigner}}",
    "disputeResolver": "GB6MP3L6UGIDY6O6MXNLSKHLXT2T2TCMPZIZGUTOGYKOLHW7EORWMFCK",
    "receiver": "{{receiver}}"
  },
  "amount": 10,
  "platformFee": 1,
  "milestones": [
    { "description": "Meta 1" },
    { "description": "Meta 2" }
  ],
  "trustline": {
    "symbol": "USDC",
    "address": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5"
  }
}
```

⚠️ **IMPORTANTE**: NO modifiques las direcciones de `approver` y `disputeResolver`.

El endpoint te retornará un XDR (transacción sin firmar).

### Paso 5: Firmar el XDR en Stellar Laboratory

1. Ve a [Stellar Laboratory - Transaction Signer](https://laboratory.stellar.org/#txsigner?network=test)
2. Pega el XDR recibido en el campo "Import a Transaction Envelope in XDR format"
3. Click en "Sign in Transaction Signer"
4. Ingresa tu clave secreta (S...)
5. Click en "Submit in Transaction Submitter"
6. Copia el XDR firmado

### Paso 6: Enviar el XDR firmado

Llama al endpoint `/deployer/submit` con el XDR firmado:

```json
{
  "signedXdr": "AAAAAgAAAAC... (tu XDR firmado)"
}
```

Guarda el transaction hash que recibes como respuesta.

### Paso 7: Verificar en Stellar Expert

1. Ve a [Stellar Expert Testnet](https://stellar.expert/explorer/testnet)
2. Busca tu transaction hash en el buscador
3. Verifica que la transacción se completó exitosamente
4. Copia el link de la transacción como entrega

### Entrega

- Link a tu transacción en Stellar Expert
- Formato: `https://stellar.expert/explorer/testnet/tx/[TRANSACTION_HASH]`
- Fecha límite: Domingo
