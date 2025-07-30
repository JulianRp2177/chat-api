# Propuesta de Infraestructura como Código (IaC)

## 🧭 Contexto

Esta propuesta describe la infraestructura actual usada en desarrollo y una opción equivalente para producción en AWS. La API está contenida en Docker, desplegada en Kubernetes (GKE) usando Skaffold, y diseñada para ser portable y segura.

---

## ⚙️ Stack Actual de Desarrollo y Despliegue

| Componente         | Tecnología                       |
|--------------------|----------------------------------|
| Contenedores       | Docker                           |
| Orquestación       | Kubernetes (GKE)                 |
| Despliegue         | Skaffold                         |
| Cloud Provider     | Google Cloud Platform (GCP)      |
| CI/CD              | GitHub Actions + Skaffold        |
| Secrets            | GCP Secret Manager               |
| Observabilidad     | Cloud Monitoring / Logging       |

---

## 🧩 Infraestructura en GCP

### Arquitectura

- **GKE (Google Kubernetes Engine)** para orquestar contenedores
- **Cloud SQL (PostgreSQL)** para base de datos gestionada
- **Cloud Storage / Secret Manager** para configuración sensible
- **Skaffold** para desarrollo local y despliegue automatizado
- **GitHub Actions** para integración y despliegue continuo
- **Cloud Logging / Monitoring** para trazabilidad y métricas

---

## 📂 Estructura del proyecto

```plaintext
.
├── app/                    # Código de la API FastAPI
├── Dockerfile              # Imagen de la aplicación
├── skaffold.yaml           # Configuración de despliegue local/prod
├── k8s/
│   ├── deployment.yaml     # Despliegue en GKE
│   ├── service.yaml        # Servicio de Kubernetes
│   └── ingress.yaml        # Ingreso para dominios / TLS
