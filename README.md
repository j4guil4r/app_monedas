# API de Conversión y Transferencia de Monedas

API REST para conversión de divisas y transferencias entre usuarios, con soporte para tres proveedores de tasas de cambio.

## 🚀 Tecnologías

- **FastAPI** (Backend)
- **PostgreSQL** (Base de datos)
- **Docker**

## 🔌 APIs de Tasa de Cambio
| Proveedor | Requiere API Key |
|-----------|------------------|
| [ExchangeRate-API](https://www.exchangerate-api.com) | ❌ |
| [Frankfurter](https://www.frankfurter.dev) | ❌ |
| [MoneyMorph](https://moneymorph.dev) | ❌ |

## 📦 Instalación

   ```bash
   git clone https://github.com/j4guil4r/app_monedas.git
   cd app_monedas

   # docker: 
   # base de datos:
   docker compose -f 'docker-compose.yml' up -d --build 'db' 
   # API de monedas:
   docker compose -f 'docker-compose.yml' up -d --build 'app' 
   
   ```
   la app estará corriendo en este [enlace](http://localhost:8000)