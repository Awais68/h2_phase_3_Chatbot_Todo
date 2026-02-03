---
id: "001-k8s-deployment-tasks"
title: "Kubernetes Deployment Tasks Generation"
stage: "tasks"
date_iso: "2026-01-26"
model: "claude-sonnet-4-5-20250929"
feature: "general"
branch: "001-k8s-deployment"
user: "user"
command: "sp.tasks"
labels: ["kubernetes", "deployment", "tasks", "containerization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-k8s-deployment/tasks.md
tests: []
outcome: "Generated comprehensive task breakdown for Kubernetes deployment of Todo AI Chatbot"
evaluation: "Successfully created detailed task list with 110 tasks across 10 phases, including environment setup, containerization, deployment, monitoring, and documentation"
---

# Kubernetes Deployment Tasks Generation

## Prompt Text

Prerequisites Checklist

 Completed Phase III (Todo AI Chatbot with voice, analytics, recurring tasks)
 Have access to Claude Code
 Have Neon PostgreSQL database credentials
 Have OpenAI API key
 Have Better Auth secret keys
 Have OpenAI domain key for ChatKit
 Have system with 8GB+ RAM
 Have admin/sudo access on development machine
 Have stable internet connection
 Have at least 60GB free disk space

Task Dependency Graph
Environment Setup (P4-T001 to P4-T015)
          ↓
Docker Containerization (P4-T016 to P4-T035)
          ↓
Minikube Cluster Setup (P4-T036 to P4-T047)
          ↓
Kubernetes Base Manifests (P4-T048 to P4-T082)
          ↓
Helm Chart Creation (P4-T083 to P4-T107)
          ↓
Deployment Scripts (P4-T108 to P4-T122)
          ↓
Testing & Validation (P4-T123 to P4-T158)
          ↓
Monitoring & Observability (P4-T159 to P4-T173)
          ↓
Operations & Management (P4-T174 to P4-T193)
          ↓
Documentation (P4-T194 to P4-T213)
          ↓
Advanced Features [Optional] (P4-T214 to P4-T228)
How to Use This Task Breakdown

Sequential Execution: Execute tasks in order (P4-T001, P4-T002, etc.)
Copy-Paste Prompts: Copy the entire "CLAUDE CODE PROMPT" section
Paste into Claude Code: Paste directly into Claude Code interface
Review Generated Code: Check all files created by Claude Code
Execute Scripts: Run any scripts generated (chmod +x if needed)
Verify Success: Check all success criteria before proceeding
Mark Complete: Check off task in this document
Handle Failures: If a task fails, troubleshoot before proceeding
Track Progress: Keep this document updated with completion status


CATEGORY 1: ENVIRONMENT SETUP & PREREQUISITES
Task P4-T001: Install and Verify Docker Desktop
Metadata:

Task ID: P4-T001
Category: Environment Setup
Priority: Critical
Estimated Time: 20 minutes
Complexity: Simple
Prerequisites: None
Status: [ ] Not Started / [ ] In Progress / [ ] Complete

Description:
Install Docker Desktop and create verification scripts to confirm installation.
CLAUDE CODE PROMPT:
TASK: Install and Verify Docker Desktop

CONTEXT:
This is the first task in Phase IV: Kubernetes Deployment. Starting fresh with environment setup for Todo AI Chatbot Kubernetes deployment.

OBJECTIVE:
Create verification scripts and documentation for Docker Desktop installation.

REQUIREMENTS:
- Docker Desktop version 24.0.0 or higher
- Docker Compose version 2.20.0 or higher
- Verification script that checks all components
- Installation documentation for all platforms
- Troubleshooting guide

TECHNOLOGY STACK:
- Docker Desktop: Latest stable version
- Docker Engine: Latest
- Docker Compose: v2.20.0+
- Shell: Bash for scripts

FILES TO CREATE:

1. File: scripts/verify-docker.sh
   Purpose: Comprehensive Docker installation verification

2. File: docs/DOCKER_INSTALLATION.md
   Purpose: Step-by-step installation guide for all platforms

3. File: docs/TROUBLESHOOTING_DOCKER.md
   Purpose: Common issues and solutions (use the complete troubleshooting guide already provided)

SCRIPT REQUIREMENTS (scripts/verify-docker.sh):
- Check Docker installation
- Check Docker daemon status
- Check Docker version (must be 24.0+)
- Check Docker Compose availability
- Test container execution with hello-world
- Check Kubernetes availability in Docker Desktop
- Colored output (green for success, red for errors, yellow for warnings)
- Clear next steps messaging
- Exit codes: 0 for success, 1 for failure

DOCUMENTATION REQUIREMENTS (docs/DOCKER_INSTALLATION.md):
- System requirements for each platform
- Step-by-step installation for macOS
- Step-by-step installation for Windows (with WSL2)
- Step-by-step installation for Linux
- Post-installation configuration (resource allocation)
- Enable Kubernetes in Docker Desktop
- Verification steps
- Troubleshooting section
- Next steps

VALIDATION:
After Claude Code creates the files:
1. Run: chmod +x scripts/verify-docker.sh
2. Run: ./scripts/verify-docker.sh
3. Expected: All checks pass with green checkmarks
4. Check Docker version is 24.0+
5. Check Docker Compose version is v2.20.0+
6. Verify hello-world container runs successfully

SUCCESS CRITERIA:
- [ ] scripts/verify-docker.sh created and executable
- [ ] Script runs without errors
- [ ] All Docker checks pass
- [ ] Docker Compose is available
- [ ] Can run test container
- [ ] docs/DOCKER_INSTALLATION.md is comprehensive
- [ ] docs/TROUBLESHOOTING_DOCKER.md covers common issues

NEXT TASK: P4-T002 (Install Minikube)
Success Criteria:

 All files created
 Verification script passes
 Docker Desktop installed and running
 Can execute docker commands
 Can run test containers


Task P4-T002: Install and Verify Minikube
Metadata:

Task ID: P4-T002
Category: Environment Setup
Priority: Critical
Estimated Time: 25 minutes
Complexity: Medium
Prerequisites: P4-T001
Status: [ ] Not Started / [ ] In Progress / [ ] Complete

Description:
Install Minikube with proper resource allocation and create verification scripts.
CLAUDE CODE PROMPT:
TASK: Install and Verify Minikube

CONTEXT:
Docker Desktop is now installed and verified. We need Minikube for local Kubernetes cluster that will run our Todo AI Chatbot.

OBJECTIVE:
Install Minikube, configure with appropriate resources, and create verification scripts.

REQUIREMENTS:
- Minikube version 1.31.0 or higher
- Configured with 4 CPUs minimum
- Configured with 8GB RAM minimum
- Docker driver (using Docker Desktop)
- Verification script
- Installation documentation

TECHNOLOGY STACK:
- Minikube: Latest stable (1.31+)
- Driver: Docker
- Kubernetes: v1.27+ (comes with Minikube)
- Shell: Bash

FILES TO CREATE:

1. File: scripts/install-minikube.sh
   Purpose: Automated Minikube installation for different platforms

2. File: scripts/verify-minikube.sh
   Purpose: Verify Minikube installation and configuration

3. File: docs/MINIKUBE_INSTALLATION.md
   Purpose: Complete installation guide

INSTALL SCRIPT REQUIREMENTS (scripts/install-minikube.sh):
- Detect operating system (macOS, Linux, Windows)
- Download appropriate Minikube binary
- Install to correct location (/usr/local/bin or C:\minikube)
- Make executable (chmod +x on Unix systems)
- Verify installation
- Print installation success message with version

VERIFICATION SCRIPT REQUIREMENTS (scripts/verify-minikube.sh):
- Check if Minikube is installed
- Check Minikube version (must be 1.31+)
- Check if Minikube cluster exists
- Check cluster status (Running/Stopped)
- Check configured driver (should be docker)
- Check configured resources (CPU, memory)
- Check kubectl context (should point to minikube)
- Colored output for results
- Clear next steps

DOCUMENTATION REQUIREMENTS (docs/MINIKUBE_INSTALLATION.md):
- What is Minikube and why we use it
- System requirements
- Installation steps for macOS (using Homebrew and direct download)
- Installation steps for Windows (using Chocolatey and direct download)
- Installation steps for Linux (using curl)
- Starting Minikube with proper resources
- Verifying installation
- Common commands
- Troubleshooting section

MINIKUBE START COMMAND TEMPLATE:
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --kubernetes-version=v1.27.0

VALIDATION:
After Claude Code creates files:
1. Run: chmod +x scripts/install-minikube.sh scripts/verify-minikube.sh
2. Run: ./scripts/install-minikube.sh
3. Expected: Minikube installed successfully
4. Run: minikube start --driver=docker --cpus=4 --memory=8192
5. Run: ./scripts/verify-minikube.sh
6. Expected: All checks pass

SUCCESS CRITERIA:
- [ ] scripts/install-minikube.sh created
- [ ] scripts/verify-minikube.sh created
- [ ] Installation script works on your platform
- [ ] Minikube version 1.31+
- [ ] Can start Minikube cluster
- [ ] Cluster has 4 CPUs and 8GB RAM
- [ ] docs/MINIKUBE_INSTALLATION.md is complete

NEXT TASK: P4-T003 (Install kubectl CLI)
Success Criteria:

 All files created
 Minikube installed successfully
 Can start Minikube cluster
 Cluster has proper resources
 Verification script passes


Task P4-T003: Install and Verify kubectl CLI
Metadata:

Task ID: P4-T003
Category: Environment Setup
Priority: Critical
Estimated Time: 15 minutes
Complexity: Simple
Prerequisites: P4-T002
Status: [ ] Not Started / [ ] In Progress / [ ] Complete

Description:
Install kubectl command-line tool and verify it can communicate with Minikube cluster.
CLAUDE CODE PROMPT:
TASK: Install and Verify kubectl CLI

CONTEXT:
Minikube cluster is now set up. We need kubectl to interact with the Kubernetes cluster and deploy our Todo AI Chatbot application.

OBJECTIVE:
Install kubectl, configure it to work with Minikube, and create verification scripts.

REQUIREMENTS:
- kubectl version matching Kubernetes version (v1.27+)
- Configured to connect to Minikube cluster
- Able to execute basic commands
- Verification script
- Installation documentation
- Cheat sheet of common commands

TECHNOLOGY STACK:
- kubectl: v1.27+ (matching cluster version)
- Kubernetes API version: v1.27
- Config location: ~/.kube/config
- Shell: Bash

FILES TO CREATE:

1. File: scripts/install-kubectl.sh
   Purpose: Automated kubectl installation

2. File: scripts/verify-kubectl.sh
   Purpose: Verify kubectl installation and cluster connectivity

3. File: scripts/kubectl-setup.sh
   Purpose: Configure kubectl for Minikube

4. File: docs/KUBECTL_INSTALLATION.md
   Purpose: Installation and configuration guide

5. File: docs/KUBECTL_CHEATSHEET.md
   Purpose: Common kubectl commands reference

INSTALL SCRIPT REQUIREMENTS (scripts/install-kubectl.sh):
- Detect OS (macOS, Linux, Windows)
- Download kubectl v1.27.x
- Install to system path
- Make executable
- Verify installation
- Show version

VERIFICATION SCRIPT REQUIREMENTS (scripts/verify-kubectl.sh):
- Check kubectl installation
- Check kubectl version (v1.27+)
- Check cluster connectivity
- List cluster contexts
- Check current context (should be minikube)
- Test basic commands (get nodes, get namespaces)
- Check cluster-info
- Colored output
- Clear next steps

SETUP SCRIPT REQUIREMENTS (scripts/kubectl-setup.sh):
- Set context to minikube
- Display current context
- Display cluster info
- Create alias 'k' for kubectl (optional)
- Show available contexts
- Verify connectivity

INSTALLATION DOCUMENTATION (docs/KUBECTL_INSTALLATION.md):
- What is kubectl
- Why we need it
- Installation for macOS (Homebrew and curl)
- Installation for Windows (Chocolatey and direct download)
- Installation for Linux (curl and package manager)
- Verifying installation
- Configuring for Minikube
- Testing connectivity
- Shell completion setup (optional)

CHEATSHEET DOCUMENTATION (docs/KUBECTL_CHEATSHEET.md):
Essential commands to include:
- Cluster info and status
- Context management
- Namespace operations
- Pod operations (get, describe, logs, exec, delete)
- Deployment operations (get, describe, scale, rollout)
- Service operations
- ConfigMap and Secret operations
- Resource creation (apply, create, delete)
- Troubleshooting commands
- Shortcuts and aliases

VALIDATION:
After Claude Code creates files:
1. Ensure Minikube is running: minikube status
2. Run: chmod +x scripts/*.sh
3. Run: ./scripts/install-kubectl.sh
4. Run: ./scripts/kubectl-setup.sh
5. Run: ./scripts/verify-kubectl.sh
6. Expected: All connectivity checks pass
7. Run: kubectl get nodes
8. Expected: Minikube node shown as Ready

SUCCESS CRITERIA:
- [ ] All script files created
- [ ] kubectl installed (v1.27+)
- [ ] Can execute kubectl commands
- [ ] Connected to Minikube cluster
- [ ] kubectl get nodes shows minikube node
- [ ] kubectl get namespaces lists namespaces
- [ ] Documentation complete
- [ ] Cheatsheet comprehensive

NEXT TASK: P4-T004 (Install Helm)
Success Criteria:

 kubectl installed successfully
 Can connect to Minikube cluster
 All verification checks pass
 Documentation created


Task P4-T004: Install and Verify Helm 3
Metadata:

Task ID: P4-T004
Category: Environment Setup
Priority: Critical
Estimated Time: 15 minutes
Complexity: Simple
Prerequisites: P4-T003
Status: [ ] Not Started / [ ] In Progress / [ ] Complete

Description:
Install Helm 3 package manager for Kubernetes and verify installation.
CLAUDE CODE PROMPT:
TASK: Install and Verify Helm 3

CONTEXT:
kubectl is installed and configured. We need Helm to package and deploy our Todo AI Chatbot as a Helm chart for easier management and deployment.

OBJECTIVE:
Install Helm 3, configure it, and create verification scripts and documentation.

REQUIREMENTS:
- Helm version 3.12.0 or higher (NOT Helm 2)
- Helm configured to work with Minikube cluster
- Able to list and install charts
- Verification script
- Installation documentation
- Helm basics guide

TECHNOLOGY STACK:
- Helm: v3.12+ (latest stable)
- Kubernetes: v1.27+
- Repository: stable charts (optional)
- Shell: Bash

FILES TO CREATE:

1. File: scripts/install-helm.sh
   Purpose: Automated Helm installation

2. File: scripts/verify-helm.sh
   Purpose: Verify Helm installation and functionality

3. File: docs/HELM_INSTALLATION.md
   Purpose: Installation guide

4. File: docs/HELM_BASICS.md
   Purpose: Helm concepts and common commands

INSTALL SCRIPT REQUIREMENTS (scripts/install-helm.sh):
- Detect OS
- Download Helm v3.12+ binary
- Install to system path (/usr/local/bin or equivalent)
- Make executable
- Verify installation
- Add stable repo (optional)
- Show installed version

VERIFICATION SCRIPT REQUIREMENTS (scripts/verify-helm.sh):
- Check Helm installation
- Check Helm version (must be 3.x, not 2.x)
- Check cluster connectivity
- List Helm releases (should be empty initially)
- List Helm repositories
- Test helm create command (create test chart, then delete)
- Check helm lint functionality
- Colored output
- Success summary

INSTALLATION DOCUMENTATION (docs/HELM_INSTALLATION.md):
- What is Helm and why use it
- Helm 2 vs Helm 3 (note: we use Helm 3, no Tiller)
- Installation for macOS (Homebrew and script)
- Installation for Windows (Chocolatey and script)
- Installation for Linux (script and package manager)
- Verifying installation
- Adding chart repositories
- Basic Helm commands
- Troubleshooting

HELM BASICS DOCUMENTATION (docs/HELM_BASICS.md):
Cover these topics:
- Helm architecture (charts, releases, repositories)
- Chart structure explanation
- values.yaml and templating
- Installing a chart
- Upgrading a release
- Rolling back a release
- Uninstalling a release
- Creating custom charts
- Best practices
- Common commands with examples

COMMON HELM COMMANDS TO DOCUMENT:
```bash
# Repository management
helm repo add <name> <url>
helm repo list
helm repo update

# Chart operations
helm search repo <keyword>
helm show chart <chart>
helm show values <chart>

# Release management
helm install <name> <chart>
helm list
helm status <release>
helm get values <release>
helm upgrade <release> <chart>
helm rollback <release> <revision>
helm uninstall <release>

# Chart development
helm create <chartname>
helm lint <chartpath>
helm template <name> <chart>
helm package <chartpath>
```

VALIDATION:
After Claude Code creates files:
1. Run: chmod +x scripts/install-helm.sh scripts/verify-helm.sh
2. Run: ./scripts/install-helm.sh
3. Expected: Helm v3.12+ installed
4. Run: helm version
5. Expected: Shows version 3.x (NOT 2.x)
6. Run: ./scripts/verify-helm.sh
7. Expected: All checks pass
8. Run: helm list
9. Expected: Returns empty list (no releases yet)

SUCCESS CRITERIA:
- [ ] Helm 3.12+ installed
- [ ] Helm version command works
- [ ] helm list executes successfully
- [ ] Can create test chart
- [ ] helm lint works
- [ ] All scripts created
- [ ] Documentation complete

NEXT TASK: P4-T005 (Install kubectl-ai plugin)
Success Criteria:

 Helm 3 installed (not Helm 2)
 Can execute Helm commands
 Verification passes
 Documentation created


Task P4-T005: Install and Configure kubectl-ai
Metadata:

Task ID: P4-T005
Category: Environment Setup
Priority: High
Estimated Time: 20 minutes
Complexity: Medium
Prerequisites: P4-T003, OpenAI API Key
Status: [ ] Not Started / [ ] In Progress / [ ] Complete

Description:
Install kubectl-ai plugin for AI-powered kubectl operations using OpenAI.
CLAUDE CODE PROMPT:
TASK: Install and Configure kubectl-ai

CONTEXT:
We have kubectl and Helm installed. Now we need kubectl-ai for AI-assisted Kubernetes operations. This will allow us to use natural language commands to interact with our Todo AI Chatbot Kubernetes deployment.

OBJECTIVE:
Install kubectl-ai plugin, configure with OpenAI API key, and create usage documentation.

REQUIREMENTS:
- kubectl-ai plugin installed
- Configured with OpenAI API key
- Able to execute AI-powered commands
- Verification script
- Usage guide with examples
- Integration with existing kubectl setup

TECHNOLOGY STACK:
- kubectl-ai: Latest version from GitHub
- OpenAI API: gpt-4 model
- kubectl: Already installed (v1.27+)
- Shell: Bash

FILES TO CREATE:

1. File: scripts/install-kubectl-ai.sh
   Purpose: Install kubectl-ai plugin

2. File: scripts/configure-kubectl-ai.sh
   Purpose: Configure OpenAI API key securely

3. File: scripts/verify-kubectl-ai.sh
   Purpose: Verify installation and test functionality

4. File: docs/KUBECTL_AI_SETUP.md
   Purpose: Installation and configuration guide

5. File: docs/KUBECTL_AI_USAGE.md
   Purpose: Usage examples and best practices

6. File: .env.kubectl-ai.example
   Purpose: Environment variable template

INSTALL SCRIPT REQUIREMENTS (scripts/install-kubectl-ai.sh):
- Check for kubectl installation
- Download kubectl-ai from GitHub releases
- Install as kubectl plugin (in ~/.kube/plugins or PATH)
- Make executable
- Verify installation
- Show version if available

Installation command reference:
```bash
# macOS/Linux
curl -LO https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai_$(uname -s)_$(uname -m).tar.gz
tar -xzf kubectl-ai_$(uname -s)_$(uname -m).tar.gz
sudo mv kubectl-ai /usr/local/bin/
chmod +x /usr/local/bin/kubectl-ai
```

CONFIGURE SCRIPT REQUIREMENTS (scripts/configure-kubectl-ai.sh):
- Prompt for OpenAI API key (or read from .env file)
- Store securely in environment variable
- Update shell profile (.bashrc, .zshrc)
- Export OPENAI_API_KEY
- Verify configuration
- Test with simple query

VERIFICATION SCRIPT REQUIREMENTS (scripts/verify-kubectl-ai.sh):
- Check kubectl-ai command exists
- Check OPENAI_API_KEY is set
- Test simple query: "get all pods"
- Test namespace query: "list all namespaces"
- Verify output is valid kubectl command
- Show examples of usage
- Colored output

ENV TEMPLATE (.env.kubectl-ai.example):
```bash
# OpenAI API Key for kubectl-ai
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Specify model (default is gpt-4)
# KUBECTL_AI_MODEL=gpt-4

# Optional: Temperature for responses
# KUBECTL_AI_TEMPERATURE=0.0
```

SETUP DOCUMENTATION (docs/KUBECTL_AI_SETUP.md):
- What is kubectl-ai and benefits
- Prerequisites (kubectl, OpenAI API key)
- Installation steps for macOS
- Installation steps for Linux
- Installation steps for Windows
- Obtaining OpenAI API key
- Configuring environment variables
- Verifying installation
- Troubleshooting
- Security considerations (API key safety)

USAGE DOCUMENTATION (docs/KUBECTL_AI_USAGE.md):
Include examples:

Basic queries:
```bash
kubectl ai "get all pods in kube-system namespace"
kubectl ai "show me all services"
kubectl ai "list deployments"
```

Deployment operations:
```bash
kubectl ai "scale deployment backend to 3 replicas"
kubectl ai "restart all pods in todo-chatbot namespace"
kubectl ai "show logs from backend pods"
```

Troubleshooting:
```bash
kubectl ai "why is my pod not starting"
kubectl ai "show me pods that are not running"
kubectl ai "get events from last 1 hour"
```

Complex operations:
```bash
kubectl ai "create a deployment with nginx image"
kubectl ai "expose deployment backend on port 8000"
kubectl ai "show resource usage for all pods"
```

Best practices:
- Be specific in queries
- Use natural language
- Review generated commands before executing
- Verify outputs
- Don't share API key
- Use for learning kubectl commands

VALIDATION:
After Claude Code creates files:
1. Run: chmod +x scripts/install-kubectl-ai.sh
2. Run: ./scripts/install-kubectl-ai.sh
3. Expected: kubectl-ai installed
4. Copy .env.kubectl-ai.example to .env.kubectl-ai
5. Add your OpenAI API key to .env.kubectl-ai
6. Run: chmod +x scripts/configure-kubectl-ai.sh
7. Run: source scripts/configure-kubectl-ai.sh
8. Run: chmod +x scripts/verify-kubectl-ai.sh
9. Run: ./scripts/verify-kubectl-ai.sh
10. Expected: Can generate kubectl commands from natural language

SUCCESS CRITERIA:
- [ ] kubectl-ai installed
- [ ] OpenAI API key configured
- [ ] Can execute: kubectl ai "get pods"
- [ ] Generates valid kubectl commands
- [ ] All scripts created
- [ ] Documentation complete
- [ ] Security practices documented

NEXT TASK: P4-T006 (Install Kagent)
Success Criteria:

 kubectl-ai installed successfully
 API key configured securely
 Can generate commands from natural language
 Documentation created

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response Text

Generated comprehensive task breakdown for Kubernetes deployment of Todo AI Chatbot with 110 tasks across 10 phases, including environment setup, containerization, deployment, monitoring, and documentation.