# Kagent Usage Guide

## Introduction
Kagent provides AI-powered assistance for Kubernetes cluster management and troubleshooting.

## Basic Commands

### Cluster Analysis
```bash
kagent analyze
```
Provides a comprehensive analysis of your cluster's health and configuration.

### Resource Analysis
```bash
kagent analyze pods
kagent analyze deployments
kagent analyze services
```
Analyze specific resource types in your cluster.

### Troubleshooting
```bash
kagent troubleshoot <resource-type> <resource-name>
```
Get AI-powered troubleshooting advice for specific resources.

### Configuration Recommendations
```bash
kagent recommend
```
Get configuration recommendations for your cluster.

## Examples

### Analyze All Workloads
```bash
kagent analyze --namespace default
```

### Get Help on Specific Commands
```bash
kagent --help
kagent analyze --help
```

## Best Practices

1. Always run `kagent analyze` to get an overview of your cluster's health
2. Use `kagent troubleshoot` when facing specific issues with resources
3. Review recommendations during routine maintenance
4. Use with specific namespaces to focus analysis

## Security Considerations

- Kagent sends cluster information to OpenAI for analysis
- Ensure your OpenAI API key is properly secured
- Review what data is being sent before using in production