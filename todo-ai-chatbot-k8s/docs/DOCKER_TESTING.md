# Docker Image Testing Guide

## Test Categories

### 1. Container Startup and Health
- Verify containers start without errors
- Check health endpoints are responsive
- Validate proper initialization

### 2. Environment Variable Injection
- Test all required environment variables are loaded
- Verify sensitive data is handled securely
- Check configuration values are applied

### 3. Service Connectivity
- Test inter-service communication
- Verify network connectivity between containers
- Validate service discovery mechanisms

### 4. Database Connectivity
- Confirm database connections work
- Test read/write operations
- Verify connection pooling

### 5. API Functionality
- Test all API endpoints
- Validate request/response handling
- Check error handling

### 6. Frontend Rendering
- Verify UI renders correctly
- Test client-side functionality
- Validate asset loading

## Test Scripts

### Master Test Script
```bash
./scripts/testing/test-docker-images.sh
```

Runs all individual tests and provides a summary.

### Individual Component Tests
- Backend: `./scripts/testing/test-backend-container.sh`
- MCP Server: `./scripts/testing/test-mcp-container.sh`
- Frontend: `./scripts/testing/test-frontend-container.sh`
- Integration: `./scripts/testing/test-integration.sh`

## Testing Process

### 1. Individual Component Testing
Test each container in isolation:
- Start container with required environment
- Verify health checks pass
- Test core functionality
- Clean up resources

### 2. Integration Testing
Test all services together:
- Use Docker Compose for multi-container setup
- Verify service-to-service communication
- Test complete user workflows
- Validate data flow

### 3. Load Testing (Optional)
- Test under expected load conditions
- Verify resource usage is reasonable
- Check for memory leaks or performance issues

## Test Validation Criteria

### Backend
- [ ] Starts successfully
- [ ] Health endpoint responds (GET /health)
- [ ] API documentation accessible (GET /docs)
- [ ] Runs as non-root user
- [ ] Connects to database
- [ ] Communicates with MCP server

### MCP Server
- [ ] Starts successfully
- [ ] Accepts TCP connections on configured port
- [ ] Runs as non-root user
- [ ] Connects to database

### Frontend
- [ ] Starts successfully
- [ ] Serves home page
- [ ] Connects to backend API
- [ ] Runs as non-root user
- [ ] Assets load correctly

### Integration
- [ ] All services start together
- [ ] Service-to-service communication works
- [ ] Complete workflows function
- [ ] Error handling works properly

## Running Tests

### Local Development
```bash
# Run all tests
./scripts/testing/test-docker-images.sh

# Run individual tests
./scripts/testing/test-backend-container.sh
./scripts/testing/test-mcp-container.sh
./scripts/testing/test-frontend-container.sh
./scripts/testing/test-integration.sh
```

### CI/CD Pipeline
Tests should run automatically:
- On code commits
- Before Docker image pushes
- During deployment validation

## Troubleshooting Common Issues

### Container Fails to Start
1. Check logs: `docker logs <container-name>`
2. Verify environment variables
3. Confirm required services are available
4. Check resource constraints

### Health Checks Fail
1. Wait longer for initialization
2. Check if dependencies are ready
3. Verify port bindings
4. Review application logs

### Integration Issues
1. Confirm network connectivity
2. Check service discovery
3. Verify API endpoint URLs
4. Test firewall rules

## Best Practices

1. **Test Early**: Run tests after each Docker image build
2. **Test Often**: Integrate into CI/CD pipeline
3. **Clean Up**: Remove test containers after tests
4. **Monitor Resources**: Track CPU, memory usage
5. **Log Verbosely**: Capture detailed logs for debugging
6. **Use Realistic Data**: Test with production-like data
7. **Validate Security**: Ensure containers run as non-root

## Performance Benchmarks

### Startup Time
- Backend: < 30 seconds
- MCP Server: < 20 seconds
- Frontend: < 15 seconds

### Resource Usage
- Backend: < 200MB memory under normal load
- MCP Server: < 100MB memory under normal load
- Frontend: < 50MB memory under normal load

### Response Times
- Health checks: < 1 second
- API calls: < 2 seconds
- Page loads: < 3 seconds

## Reporting

### Test Results
Tests should output:
- Pass/fail status for each test
- Performance metrics
- Resource usage statistics
- Error details when applicable

### Success Criteria
- 100% of tests pass
- Performance within benchmarks
- Security requirements met
- Resource usage acceptable