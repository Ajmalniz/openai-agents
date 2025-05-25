# Dapr Intro (Hands On with Helm, Dapr State, Dapr Pub/Sub)

## Overview
This tutorial introduces **Dapr** (Distributed Application Runtime), a tool that simplifies building distributed applications like microservices. It's part of the **Dapr Agentic Cloud Ascent (DACA)** learning path, focusing on creating scalable, resilient AI systems.

## What You'll Learn
- Deploy Dapr using Helm on Kubernetes (Rancher Desktop)
- Test Dapr features with `curl`
- Explore the Dapr Dashboard
- Build a FastAPI app with hot reloading
- Use Dapr's state management and pub/sub capabilities

## What is Dapr?
Dapr is a portable, event-driven runtime that makes it easy to build resilient applications for cloud and edge environments. It works with any programming language and handles complex distributed system challenges.

### Key Features
- **Language Agnostic**: Works with Python, Go, Java, etc.
- **Sidecar Architecture**: Runs alongside your app in a separate container
- **Building Blocks**: Ready-to-use APIs for common patterns
- **Pluggable Components**: Works with multiple backends (Redis, Kafka, etc.)
- **Cloud-Native**: Perfect for Kubernetes deployments

## Dapr Architecture Explained
### Sidecar Pattern
- **Your App**: The main application (e.g., FastAPI service)
- **Dapr Sidecar**: Helper container running next to your app
- **Dapr APIs**: Your app communicates with the sidecar on port 3500
- **Components**: Sidecar connects to backends based on configuration

### Example Flow
1. Your app sends a request to the sidecar
2. Sidecar handles the request (e.g., saves data to Redis)
3. Sidecar manages retries and errors automatically

## Dapr Building Blocks
1. **Service Invocation**
   - Direct communication between services
   - Example: Chat Service → Analytics Service

2. **State Management**
   - Key-value storage for data
   - Example: Storing user sessions in Redis

3. **Pub/Sub Messaging**
   - Asynchronous communication
   - Example: Publishing "MessageSent" events

4. **Other Features**
   - Bindings (external system connections)
   - Actors (stateful object management)
   - Workflows (process orchestration)
   - Secrets (secure API key storage)
   - Configuration (feature flags)
   - Observability (monitoring and tracing)

## Learning Objectives
1. Install Dapr using Helm
2. Understand Dapr's components
3. Deploy Redis and Dapr components
4. Use Dapr's state and pub/sub APIs
5. Check data in Redis
6. Use the Dapr Dashboard
7. Create a FastAPI app with hot reloading

## Prerequisites
- **Rancher Desktop**: Running with Kubernetes
- **Helm**: Version 3
- **kubectl**: Configured for Rancher Desktop
- **nerdctl**: For container management
- **Python 3.9+**: For FastAPI
- **uv**: Python dependency manager
- **curl**: For API testing

## Tutorial Steps
1. Dapr Helm Hands On
2. Setup Dapr with FastAPI
3. Add hot reloading to FastAPI
4. Complete Cloud Native Local Development Environment setup

## Why Dapr for DACA?
- **Simplified Communication**: Easy service-to-service calls
- **State Management**: Handles data storage for stateless apps
- **Resilience**: Built-in retry and error handling
- **Scalability**: Works with Kubernetes for large deployments
- **Flexibility**: Supports free-tier services for testing

## Resources
- [Dapr Kubernetes Deployment](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/)
- [Dapr Helm Chart](https://github.com/dapr/dapr/tree/master/charts/dapr)
- [Dapr Dashboard](https://docs.dapr.io/operations/monitoring/dashboard/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [UV Documentation](https://docs.astral.sh/uv/)