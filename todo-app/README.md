# Todo App Helm Chart

This Helm chart deploys a full-stack todo application with AI chatbot functionality, consisting of a frontend (Next.js) and backend (FastAPI) service.

## Chart Structure

- `frontend`: Next.js application serving the user interface
- `backend`: FastAPI application providing the API and AI chatbot functionality

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `my-todo-app`:

```bash
helm install my-todo-app .
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

### Frontend Parameters

| Parameter                     | Description                                     | Default                            |
|-------------------------------|-------------------------------------------------|------------------------------------|
| `frontend.enabled`            | Enable frontend deployment                      | `true`                             |
| `frontend.replicaCount`       | Number of frontend pods                         | `1`                                |
| `frontend.image.repository`   | Frontend image repository                       | `todo-frontend`                    |
| `frontend.image.pullPolicy`   | Frontend image pull policy                      | `IfNotPresent`                     |
| `frontend.image.tag`          | Frontend image tag                              | `""`                               |
| `frontend.service.type`       | Frontend service type                           | `ClusterIP`                        |
| `frontend.service.port`       | Frontend service port                           | `3000`                             |
| `frontend.service.targetPort` | Frontend container port                         | `3000`                             |

### Backend Parameters

| Parameter                     | Description                                     | Default                            |
|-------------------------------|-------------------------------------------------|------------------------------------|
| `backend.enabled`             | Enable backend deployment                       | `true`                             |
| `backend.replicaCount`        | Number of backend pods                          | `1`                                |
| `backend.image.repository`    | Backend image repository                        | `todo-backend`                     |
| `backend.image.pullPolicy`    | Backend image pull policy                       | `IfNotPresent`                     |
| `backend.image.tag`           | Backend image tag                               | `""`                               |
| `backend.service.type`        | Backend service type                            | `ClusterIP`                        |
| `backend.service.port`        | Backend service port                            | `8000`                             |
| `backend.service.targetPort`  | Backend container port                          | `8000`                             |

## Customizing the Installation

You can create a custom `values.yaml` file to override the default values:

```yaml
frontend:
  replicaCount: 2
  image:
    repository: my-repo/todo-frontend
    tag: v1.0.0
  service:
    type: LoadBalancer
    port: 80

backend:
  replicaCount: 2
  image:
    repository: my-repo/todo-backend
    tag: v1.0.0
  service:
    type: ClusterIP
    port: 8000
```

Then install with:

```bash
helm install my-todo-app -f values.yaml .
```

## Uninstalling the Chart

To uninstall/delete the `my-todo-app` release:

```bash
helm delete my-todo-app
```

This will remove all the Kubernetes resources associated with the chart.