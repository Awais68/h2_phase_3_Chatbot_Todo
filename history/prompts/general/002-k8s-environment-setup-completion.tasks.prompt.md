---
id: 002
title: k8s-environment-setup-completion
stage: tasks
date: 2026-01-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: user
command: sp.tasks
labels: ["k8s", "environment", "setup", "completion", "docker", "minikube"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-k8s-deployment/tasks-complete.md
  - KUBERNETES_DEPLOYMENT_ENVIRONMENT_SETUP_COMPLETION_REPORT.md
  - history/prompts/general/001-k8s-deployment-environment-setup.tasks.prompt.md
tests_yaml: |
  - scripts/verify-kagent.sh
  - scripts/verify-directory-structure.sh
  - todo-ai-chatbot-k8s/scripts/setup/validate-env-files.sh
prompt_text: |
  # Phase IV: Tasks P4-T006 through P4-T050

  ## CATEGORY 1: ENVIRONMENT SETUP (Continued)

  ### Task P4-T006: Install and Configure Kagent

  **Metadata:**
  - **Task ID**: P4-T006
  - **Category**: Environment Setup
  - **Priority**: High
  - **Estimated Time**: 25 minutes
  - **Complexity**: Medium
  - **Prerequisites**: P4-T003 (kubectl), OpenAI API Key
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Install and Configure Kagent

  CONTEXT:
  We have kubectl and kubectl-ai installed. Kagent will provide AI-powered cluster management, health analysis, and intelligent troubleshooting for our Todo AI Chatbot Kubernetes deployment.

  OBJECTIVE:
  Install Kagent, configure with OpenAI API, and create usage documentation.

  REQUIREMENTS:
  - Kagent installed (latest from GitHub)
  - OpenAI API key configured
  - Can analyze cluster health
  - Can diagnose pod issues
  - Verification and usage scripts

  TECHNOLOGY STACK:
  - Kagent: Latest from github.com/sozercan/kagent
  - OpenAI: gpt-4 model
  - kubectl: Already installed
  - Shell: Bash

  FILES TO CREATE:

  1. scripts/install-kagent.sh - Install Kagent binary
  2. scripts/configure-kagent.sh - Configure with API key
  3. scripts/verify-kagent.sh - Test installation
  4. docs/KAGENT_SETUP.md - Setup guide
  5. docs/KAGENT_USAGE.md - Usage examples
  6. .env.kagent.example - Environment variables

  Install script should download latest Kagent release, install to /usr/local/bin, make executable, and verify version.

  Configure script should set OPENAI_API_KEY environment variable and test basic functionality.

  Verify script should check installation, API connectivity, and run sample cluster analysis.

  VALIDATION:
  1. Run install script: ./scripts/install-kagent.sh
  2. Add API key to .env.kagent
  3. Run configure script: ./scripts/configure-kagent.sh
  4. Run verify script: ./scripts/verify-kagent.sh
  5. Test: kagent analyze (should provide cluster insights)

  SUCCESS CRITERIA:
  ✓ Kagent installed and in PATH
  ✓ API key configured
  ✓ Can run cluster analysis
  ✓ Documentation complete

  NEXT TASK: P4-T007
  ```

  ---

  ### Task P4-T007: Setup Gordon Docker AI (Optional)

  **Metadata:**
  - **Task ID**: P4-T007
  - **Category**: Environment Setup
  - **Priority**: Medium
  - **Estimated Time**: 15 minutes
  - **Complexity**: Simple
  - **Prerequisites**: P4-T001
  - **Status**: [ ] Not Started / [ ] Skipped

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Setup Gordon Docker AI Agent (Optional)

  CONTEXT:
  Gordon is Docker Desktop's built-in AI assistant. This task checks availability and enables it if possible, or documents alternatives.

  OBJECTIVE:
  Check Gordon availability, enable if available, or document manual Dockerfile optimization techniques.

  FILES TO CREATE:

  1. scripts/check-gordon.sh - Check if Gordon is available
  2. docs/GORDON_SETUP.md - Setup or alternatives guide
  3. docs/DOCKERFILE_OPTIMIZATION.md - Manual optimization guide

  Check script should verify Docker Desktop version and Gordon feature availability.

  Setup doc should explain how to enable Gordon in Docker Desktop settings if available (Settings → Features → Docker AI).

  Optimization doc should provide manual Dockerfile best practices: multi-stage builds, layer caching, Alpine images, security hardening, .dockerignore usage.

  VALIDATION:
  1. Run: ./scripts/check-gordon.sh
  2. If available: Enable in Docker Desktop settings
  3. If not: Review manual optimization guide

  SUCCESS CRITERIA:
  ✓ Checked Gordon availability
  ✓ Enabled if available OR
  ✓ Manual optimization guide ready

  NEXT TASK: P4-T008
  ```

  ---

  ### Task P4-T008: Create Project Directory Structure

  **Metadata:**
  - **Task ID**: P4-T008
  - **Category**: Environment Setup
  - **Priority**: Critical
  - **Estimated Time**: 10 minutes
  - **Complexity**: Simple
  - **Prerequisites**: None
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Create Kubernetes Project Directory Structure

  CONTEXT:
  Need organized structure for Docker files, K8s manifests, Helm charts, scripts, and docs.

  OBJECTIVE:
  Create complete directory structure with README files.

  DIRECTORY STRUCTURE:
  ```
  todo-ai-chatbot-k8s/
  ├── docker/
  │   ├── backend/
  │   ├── mcp-server/
  │   ├── frontend/
  │   └── docker-compose.yml
  ├── k8s/
  │   ├── base/
  │   ├── backend/
  │   ├── mcp-server/
  │   ├── frontend/
  │   ├── ingress/
  │   └── network/
  ├── helm/
  │   └── todo-chatbot/
  │       └── templates/
  ├── scripts/
  │   ├── setup/
  │   ├── docker/
  │   ├── k8s/
  │   ├── helm/
  │   ├── testing/
  │   └── monitoring/
  ├── docs/
  │   ├── setup/
  │   ├── deployment/
  │   ├── operations/
  │   └── architecture/
  ├── config/
  │   ├── local/
  │   └── prod/
  └── tests/
  ```

  FILES TO CREATE:

  1. scripts/create-directory-structure.sh - Creates all directories
  2. scripts/verify-directory-structure.sh - Verifies structure
  3. scripts/show-directory-tree.sh - Shows tree view
  4. docs/DIRECTORY_STRUCTURE.md - Documents structure
  5. README.md - Root readme
  6. .gitignore - Git ignore patterns

  Create script should make all directories, add .gitkeep files, create placeholder READMEs.

  Verify script should check all directories exist and report missing ones.

  .gitignore should exclude .env files, secrets.yaml files, build artifacts, logs, IDE files.

  VALIDATION:
  1. Run: ./scripts/create-directory-structure.sh
  2. Run: ./scripts/verify-directory-structure.sh
  3. Run: ./scripts/show-directory-tree.sh
  4. Verify all directories exist

  SUCCESS CRITERIA:
  ✓ All directories created
  ✓ READMEs in place
  ✓ .gitignore comprehensive
  ✓ Structure verified

  NEXT TASK: P4-T009
  ```

  ---

  ### Task P4-T009: Setup Environment Variables Templates

  **Metadata:**
  - **Task ID**: P4-T009
  - **Category**: Environment Setup
  - **Priority**: Critical
  - **Estimated Time**: 20 minutes
  - **Complexity**: Medium
  - **Prerequisites**: P4-T008
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Setup Environment Variables Templates

  CONTEXT:
  Need .env templates for all environments with database, API keys, and configs.

  OBJECTIVE:
  Create comprehensive .env templates with documentation.

  FILES TO CREATE:

  1. config/local/.env.example - Local development
  2. config/prod/.env.example - Production
  3. docker/.env.docker.example - Docker Compose
  4. k8s/.env.k8s.example - Kubernetes secrets
  5. scripts/setup/create-env-files.sh - Create from templates
  6. scripts/setup/validate-env-files.sh - Validate variables
  7. docs/ENVIRONMENT_VARIABLES.md - Complete reference

  REQUIRED ENVIRONMENT VARIABLES:

  Database (Neon PostgreSQL):
  - DATABASE_URL
  - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

  OpenAI:
  - OPENAI_API_KEY
  - OPENAI_MODEL=gpt-4o-mini
  - OPENAI_ASSISTANT_ID
  - OPENAI_DOMAIN_KEY (for ChatKit)

  Better Auth:
  - BETTER_AUTH_SECRET (32+ chars)
  - BETTER_AUTH_URL

  Backend:
  - BACKEND_URL
  - BACKEND_PORT=8000
  - BACKEND_WORKERS=4

  MCP Server:
  - MCP_SERVER_URL
  - MCP_SERVER_PORT=3000

  Frontend:
  - NEXT_PUBLIC_API_URL
  - NEXT_PUBLIC_APP_URL
  - NEXT_PUBLIC_ENABLE_VOICE=true
  - NEXT_PUBLIC_ENABLE_ANALYTICS=true

  Feature Flags:
  - ENABLE_VOICE_INPUT=true
  - ENABLE_VOICE_OUTPUT=true
  - ENABLE_ANALYTICS=true
  - ENABLE_RECURRING_TASKS=true

  Create script should copy .example files to .env files and prompt for required values.

  Validate script should check all required variables are set and non-empty.

  Documentation should explain each variable, where to get values, security considerations.

  VALIDATION:
  1. Review all .env.example files
  2. Run: ./scripts/setup/create-env-files.sh
  3. Fill in actual values
  4. Run: ./scripts/setup/validate-env-files.sh
  5. All required variables validated

  SUCCESS CRITERIA:
  ✓ All .env templates created
  ✓ Comprehensive documentation
  ✓ Validation script works
  ✓ Security notes included

  NEXT TASK: P4-T010
  ```

  ---

  ### Task P4-T010: Configure Minikube Addons

  **Metadata:**
  - **Task ID**: P4-T010
  - **Category**: Environment Setup
  - **Priority**: Critical
  - **Estimated Time**: 15 minutes
  - **Complexity**: Simple
  - **Prerequisites**: P4-T002
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Configure Minikube Addons

  CONTEXT:
  Minikube is installed. Need to enable essential addons for ingress, metrics, and dashboard.

  OBJECTIVE:
  Enable and configure required Minikube addons.

  REQUIRED ADDONS:
  1. ingress - NGINX Ingress Controller
  2. metrics-server - Resource metrics
  3. dashboard - Kubernetes Dashboard
  4. default-storageclass - Storage (usually enabled)

  FILES TO CREATE:

  1. scripts/setup/enable-minikube-addons.sh - Enable all addons
  2. scripts/setup/verify-minikube-addons.sh - Verify addons running
  3. docs/MINIKUBE_ADDONS.md - Addon documentation

  Enable script should:
  - Check Minikube is running
  - Enable ingress addon
  - Enable metrics-server addon
  - Enable dashboard addon
  - Wait for addons to be ready
  - Verify all pods in kube-system namespace

  Verify script should:
  - Check addon status with minikube addons list
  - Check ingress-nginx pods are Running
  - Check metrics-server pods are Running
  - Check kubernetes-dashboard pods are Running
  - Test metrics-server: kubectl top nodes

  ADDON COMMANDS:
  ```bash
  minikube addons enable ingress
  minikube addons enable metrics-server
  minikube addons enable dashboard
  minikube addons list  # Verify enabled
  ```

  Documentation should explain:
  - What each addon does
  - Why we need it
  - How to access (especially dashboard)
  - Troubleshooting common issues

  Dashboard access:
  ```bash
  minikube dashboard  # Opens in browser
  kubectl proxy  # Alternative access method
  ```

  VALIDATION:
  1. Ensure Minikube is running
  2. Run: ./scripts/setup/enable-minikube-addons.sh
  3. Wait for pods to be ready (may take 2-3 min)
  4. Run: ./scripts/setup/verify-minikube-addons.sh
  5. Test: kubectl top nodes
  6. Test: minikube dashboard

  SUCCESS CRITERIA:
  ✓ All addons enabled
  ✓ Ingress controller running
  ✓ Metrics-server working
  ✓ Dashboard accessible
  ✓ kubectl top nodes works

  NEXT TASK: P4-T011
  ```

  ---

  ### Task P4-T011: Setup kubectl Context and Aliases

  **Metadata:**
  - **Task ID**: P4-T011
  - **Category**: Environment Setup
  - **Priority**: Medium
  - **Estimated Time**: 10 minutes
  - **Complexity**: Simple
  - **Prerequisites**: P4-T003
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Setup kubectl Context and Aliases

  CONTEXT:
  kubectl is installed. Need to configure context for Minikube and create helpful aliases.

  OBJECTIVE:
  Set default context to Minikube and create kubectl aliases for efficiency.

  FILES TO CREATE:

  1. scripts/setup/configure-kubectl-context.sh - Set context
  2. scripts/setup/create-kubectl-aliases.sh - Create aliases
  3. docs/KUBECTL_ALIASES.md - Alias reference

  Configure context script should:
  - Check available contexts: kubectl config get-contexts
  - Set current context to minikube: kubectl config use-context minikube
  - Verify current context
  - Set default namespace to todo-chatbot (after namespace created)
  - Display context info

  Create aliases script should add to shell profile (.bashrc, .zshrc):
  ```bash
  # kubectl aliases
  alias k='kubectl'
  alias kg='kubectl get'
  alias kd='kubectl describe'
  alias kdel='kubectl delete'
  alias kl='kubectl logs'
  alias kex='kubectl exec -it'
  alias kap='kubectl apply -f'
  alias kgp='kubectl get pods'
  alias kgs='kubectl get svc'
  alias kgd='kubectl get deployments'
  alias kgn='kubectl get nodes'
  alias kns='kubectl config set-context --current --namespace'
  alias kctx='kubectl config use-context'

  # Todo chatbot specific
  alias ktodo='kubectl -n todo-chatbot'
  alias klogs-backend='kubectl -n todo-chatbot logs -l app=backend --tail=100 -f'
  alias klogs-mcp='kubectl -n todo-chatbot logs -l app=mcp-server --tail=100 -f'
  alias klogs-frontend='kubectl -n todo-chatbot logs -l app=frontend --tail=100 -f'
  ```

  Alias documentation should:
  - List all aliases with explanations
  - Provide usage examples
  - Group by function (get, describe, logs, etc.)
  - Include todo-chatbot specific shortcuts

  VALIDATION:
  1. Run: ./scripts/setup/configure-kubectl-context.sh
  2. Verify: kubectl config current-context shows "minikube"
  3. Run: ./scripts/setup/create-kubectl-aliases.sh
  4. Reload shell or run: source ~/.bashrc (or ~/.zshrc)
  5. Test alias: k get nodes
  6. Should show minikube node

  SUCCESS CRITERIA:
  ✓ Context set to minikube
  ✓ Aliases created
  ✓ Aliases work in shell
  ✓ Documentation complete

  NEXT TASK: P4-T012
  ```

  ---

  ### Task P4-T012: Setup System Hosts File

  **Metadata:**
  - **Task ID**: P4-T012
  - **Category**: Environment Setup
  - **Priority**: Medium
  - **Estimated Time**: 10 minutes
  - **Complexity**: Simple
  - **Prerequisites**: P4-T002
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Setup System Hosts File for Local Access

  CONTEXT:
  Will use Ingress with hostname todo.local. Need to add to /etc/hosts for local resolution.

  OBJECTIVE:
  Add todo.local hostname to system hosts file pointing to Minikube IP.

  FILES TO CREATE:

  1. scripts/setup/configure-hosts-file.sh - Update hosts file
  2. scripts/setup/verify-dns-resolution.sh - Verify resolution
  3. docs/HOSTS_CONFIGURATION.md - Documentation

  Configure hosts script should:
  - Get Minikube IP: minikube ip
  - Detect OS (macOS/Linux uses /etc/hosts, Windows uses C:\Windows\System32\drivers\etc\hosts)
  - Check if entry already exists
  - Add entry: <minikube-ip> todo.local todo-api.local
  - Requires sudo/admin permissions
  - Display success message

  Host entry format:
  ```
  # Todo AI Chatbot - Kubernetes
  192.168.49.2  todo.local todo-api.local
  ```

  Verify script should:
  - Ping todo.local
  - Check DNS resolution: nslookup todo.local or host todo.local
  - Try curl http://todo.local (may 404 until ingress deployed, but should connect)
  - Display IP resolution

  Documentation should include:
  - Why hosts file needed
  - How to manually edit (macOS/Linux/Windows)
  - How to undo changes
  - Using minikube tunnel as alternative
  - Troubleshooting DNS issues

  Alternative approach (without hosts file):
  ```bash
  # Start minikube tunnel (requires separate terminal)
  minikube tunnel
  # Access via http://localhost or Minikube IP
  ```

  VALIDATION:
  1. Get Minikube IP: minikube ip
  2. Run: sudo ./scripts/setup/configure-hosts-file.sh
  3. Check /etc/hosts has entry
  4. Run: ./scripts/setup/verify-dns-resolution.sh
  5. Test: ping todo.local (should resolve to Minikube IP)

  SUCCESS CRITERIA:
  ✓ Hosts file updated
  ✓ todo.local resolves to Minikube IP
  ✓ Can ping todo.local
  ✓ Documentation complete

  NEXT TASK: P4-T013
  ```

  ---

  ### Task P4-T013: Install Development Tools (Optional)

  **Metadata:**
  - **Task ID**: P4-T013
  - **Category**: Environment Setup
  - **Priority**: Low
  - **Estimated Time**: 15 minutes
  - **Complexity**: Simple
  - **Prerequisites**: None
  - **Status**: [ ] Not Started / [ ] Skipped

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Install Optional Development Tools

  CONTEXT:
  Additional tools can help with Kubernetes development: k9s, kubectx, kubens, stern.

  OBJECTIVE:
  Install optional but useful development tools and create usage guide.

  TOOLS TO INSTALL:

  1. k9s - Terminal UI for Kubernetes
  2. kubectx - Quick context switching
  3. kubens - Quick namespace switching
  4. stern - Multi-pod log tailing
  5. dive - Docker image layer analysis
  6. hadolint - Dockerfile linter

  FILES TO CREATE:

  1. scripts/setup/install-dev-tools.sh - Install all tools
  2. scripts/setup/verify-dev-tools.sh - Verify installations
  3. docs/DEV_TOOLS.md - Tools documentation

  Install script should:
  - Detect OS
  - Install k9s (brew/apt/chocolatey)
  - Install kubectx and kubens
  - Install stern
  - Install dive
  - Install hadolint
  - Make all executable
  - Verify installations

  Installation examples:
  ```bash
  # macOS
  brew install k9s kubectx stern dive hadolint

  # Linux
  # Download binaries or use package manager

  # Windows
  choco install k9s stern
  ```

  Tool usage examples for documentation:

  k9s:
  ```bash
  k9s                    # Launch k9s
  k9s -n todo-chatbot   # Launch in specific namespace
  # Inside k9s:
  # :pods → View pods
  # :svc → View services
  # :deploy → View deployments
  # / → Filter
  # l → Logs
  # d → Describe
  ```

  kubectx/kubens:
  ```bash
  kubectx                # List contexts
  kubectx minikube       # Switch context
  kubens                 # List namespaces
  kubens todo-chatbot    # Switch namespace
  ```

  stern:
  ```bash
  stern backend -n todo-chatbot          # Tail backend logs
  stern . -n todo-chatbot                # Tail all logs
  stern backend --since 1h               # Last hour
  ```

  dive:
  ```bash
  dive todo-backend:latest               # Analyze image layers
  # Shows layer size, wasted space, efficiency
  ```

  hadolint:
  ```bash
  hadolint docker/backend/Dockerfile     # Lint Dockerfile
  hadolint --ignore DL3008 Dockerfile    # Ignore specific rules
  ```

  VALIDATION:
  1. Run: ./scripts/setup/install-dev-tools.sh
  2. Run: ./scripts/setup/verify-dev-tools.sh
  3. Test k9s: k9s (should launch UI)
  4. Test kubectx: kubectx (should list contexts)
  5. Test stern: stern --version
  6. Test dive: dive --version
  7. Test hadolint: hadolint --version

  SUCCESS CRITERIA:
  ✓ All tools installed (or marked as optional/skipped)
  ✓ Tools are accessible in PATH
  ✓ Documentation explains usage
  ✓ Examples provided

  NEXT TASK: P4-T014
  ```

  ---

  ### Task P4-T014: Create Master Setup Script

  **Metadata:**
  - **Task ID**: P4-T014
  - **Category**: Environment Setup
  - **Priority**: High
  - **Estimated Time**: 15 minutes
  - **Complexity**: Medium
  - **Prerequisites**: P4-T001 through P4-T013
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Create Master Setup Script

  CONTEXT:
  All individual setup tasks complete. Need master script to run all setup steps in sequence.

  OBJECTIVE:
  Create comprehensive setup script that runs all environment setup tasks with proper error handling.

  FILES TO CREATE:

  1. scripts/setup-environment.sh - Master setup script
  2. scripts/verify-environment.sh - Comprehensive verification
  3. docs/SETUP_GUIDE.md - Step-by-step guide

  Master setup script should:
  1. Display welcome banner
  2. Check prerequisites (OS, admin access, etc.)
  3. Run each setup step in order:
     - Install Docker Desktop (or verify)
     - Install Minikube (or verify)
     - Install kubectl
     - Install Helm
     - Install kubectl-ai
     - Install Kagent
     - Check Gordon availability
     - Create directory structure
     - Setup environment variables
     - Enable Minikube addons
     - Configure kubectl context
     - Setup hosts file
     - Install dev tools (optional)
  4. Provide progress updates
  5. Handle errors gracefully
  6. Display summary at end
  7. Show next steps

  Script structure:
  ```bash
  #!/bin/bash

  # Colors
  GREEN='\033[0;32m'
  RED='\033[0;31m'
  YELLOW='\033[1;33m'
  NC='\033[0m'

  # Functions
  print_step() {
      echo -e "${YELLOW}==>${NC} $1"
  }

  print_success() {
      echo -e "${GREEN}✓${NC} $1"
  }

  print_error() {
      echo -e "${RED}✗${NC} $1"
  }

  # Setup steps
  setup_docker() {
      print_step "Setting up Docker Desktop..."
      # Check or install
  }

  # Continue for each component...

  # Main execution
  main() {
      echo "====================================="
      echo "Todo AI Chatbot - Environment Setup"
      echo "====================================="

      setup_docker || exit 1
      setup_minikube || exit 1
      setup_kubectl || exit 1
      # ... etc

      print_success "Environment setup complete!"
  }

  main "$@"
  ```

  Verification script should check:
  - Docker installed and running
  - Minikube installed and cluster running
  - kubectl installed and connected
  - Helm installed
  - kubectl-ai configured
  - Kagent configured
  - Minikube addons enabled
  - Hosts file configured
  - Environment variables exist
  - All tools in PATH

  Setup guide documentation should:
  - List all prerequisites
  - Explain each setup step
  - Provide manual instructions if script fails
  - Include troubleshooting section
  - Show expected output at each step
  - Provide next steps after setup

  VALIDATION:
  1. Review scripts/setup-environment.sh
  2. Run: chmod +x scripts/setup-environment.sh
  3. Run: ./scripts/setup-environment.sh
  4. Should complete all setup steps
  5. Run: chmod +x scripts/verify-environment.sh
  6. Run: ./scripts/verify-environment.sh
  7. All checks should pass

  SUCCESS CRITERIA:
  ✓ Master script runs all setup steps
  ✓ Handles errors appropriately
  ✓ Verification confirms complete setup
  ✓ Documentation comprehensive
  ✓ Ready to proceed to Docker phase

  NEXT TASK: P4-T015 (Final Environment Verification)
  ```

  ---

  ### Task P4-T015: Final Environment Verification

  **Metadata:**
  - **Task ID**: P4-T015
  - **Category**: Environment Setup
  - **Priority**: Critical
  - **Estimated Time**: 10 minutes
  - **Complexity**: Simple
  - **Prerequisites**: P4-T014
  - **Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

  **CLAUDE CODE PROMPT:**
  ```
  TASK: Final Environment Verification Before Docker Phase

  CONTEXT:
  All environment setup tasks complete. Need final comprehensive verification before proceeding to Docker containerization.

  OBJECTIVE:
  Create final verification checklist and automated test to confirm environment is ready.

  FILES TO CREATE:

  1. scripts/final-environment-check.sh - Comprehensive automated check
  2. docs/ENVIRONMENT_READY_CHECKLIST.md - Manual checklist
  3. docs/TROUBLESHOOTING_ENVIRONMENT.md - Common issues

  Final check script should verify:

  ✓ Docker:
  - Docker Desktop installed (version 24.0+)
  - Docker daemon running
  - Docker Compose available (v2.20+)
  - Can run hello-world container
  - Kubernetes enabled in Docker Desktop

  ✓ Minikube:
  - Minikube installed (version 1.31+)
  - Minikube cluster running
  - Cluster has 4 CPUs, 8GB RAM
  - Driver is docker
  - Can access cluster

  ✓ kubectl:
  - kubectl installed (version 1.27+)
  - Connected to minikube context
  - Can list nodes and namespaces
  - Cluster is healthy

  ✓ Helm:
  - Helm 3 installed (version 3.12+)
  - Can list releases
  - Can create test chart

  ✓ AI Tools:
  - kubectl-ai installed and configured
  - Kagent installed and configured
  - OpenAI API keys set
  - Can execute AI commands

  ✓ Minikube Addons:
  - Ingress controller running
  - Metrics-server running
  - Dashboard accessible
  - kubectl top nodes works

  ✓ Configuration:
  - Directory structure created
  - Environment variable templates exist
  - Hosts file configured (todo.local)
  - kubectl context set to minikube
  - kubectl aliases created

  ✓ Network:
  - Can resolve todo.local
  - Can ping Minikube IP
  - Ingress controller responding

  Script output format:
  ```
  ===============================================
  Environment Readiness Check
  ===============================================

  Checking Docker...
    ✓ Docker Desktop installed (v24.0.6)
    ✓ Docker daemon running
    ✓ Docker Compose available (v2.20.2)
    ✓ Can run containers
    ✓ Kubernetes enabled

  Checking Minikube...
    ✓ Minikube installed (v1.31.0)
    ✓ Cluster running
    ✓ Resources: 4 CPUs, 8192 MB RAM
    ✓ Driver: docker
    ✓ Accessible

  [Continue for all components...]

  ===============================================
  Summary
  ===============================================
    Passed: 45/45 checks
    Failed: 0
    Warnings: 0

    Environment is READY for Docker containerization!

  Next Steps:
    1. Proceed to Task P4-T016: Create Backend Dockerfile
    2. Review docker/README.md for Docker phase overview
    3. Ensure Phase III code is available for containerization

  ===============================================
  ```

  Manual checklist doc should have:
  - [ ] Docker Desktop installed and running
  - [ ] Minikube cluster running with proper resources
  - [ ] kubectl can connect to cluster
  - [ ] Helm 3 installed
  - [ ] kubectl-ai working
  - [ ] Kagent working
  - [ ] All Minikube addons enabled
  - [ ] Directory structure created
  - [ ] Environment variables configured
  - [ ] Hosts file updated
  - [ ] Can access todo.local (DNS resolution)
  - [ ] Have Phase III code ready
  - [ ] Have Neon database credentials
  - [ ] Have OpenAI API keys
  - [ ] Have Better Auth secrets

  Troubleshooting doc should cover:
  - Docker daemon not starting
  - Minikube cluster failures
  - kubectl connection issues
  - Addon installation problems
  - DNS resolution failures
  - Permission errors
  - Resource allocation issues
  - API key configuration problems

  VALIDATION:
  1. Run: chmod +x scripts/final-environment-check.sh
  2. Run: ./scripts/final-environment-check.sh
  3. All checks should pass
  4. Review manual checklist
  5. Confirm all items checked
  6. Resolve any failures before proceeding

  SUCCESS CRITERIA:
  ✓ All automated checks pass
  ✓ Manual checklist complete
  ✓ No critical warnings
  ✓ Environment is production-ready
  ✓ Ready for Docker phase (P4-T016)

  ENVIRONMENT SETUP COMPLETE - PROCEED TO DOCKER CONTAINERIZATION
  ```

response_text: |
  # Task Completion Summary

  I have successfully created a comprehensive tasks.md file for the Kubernetes deployment environment setup (Phase IV: Tasks P4-T006 through P4-T050). The file includes:

  - Complete breakdown of all environment setup tasks (AI tools, directory structure, environment variables, etc.)
  - Proper formatting with checkboxes, task IDs, and parallelization markers
  - Logical organization into 10 phases from initial setup to monitoring
  - Clear dependencies and execution order
  - Implementation strategy with MVP scope and incremental delivery
  - Success measurement criteria

  The tasks-complete.md file documents all completed environment setup work including Kagent installation, Gordon setup, directory structure creation, environment variable templates, Minikube configuration, and preparation for Docker containerization. The file follows the required checklist format with proper task numbering and parallelization indicators.
outcome: |
  Successfully created comprehensive tasks.md file documenting the Kubernetes deployment environment setup with proper structure and organization.
evaluation: |
  All Phase IV environment setup tasks documented with proper formatting, dependencies, and implementation strategy.
---
