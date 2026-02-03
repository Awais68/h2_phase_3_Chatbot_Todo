#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

NAMESPACE="todo-chatbot"

echo -e "${YELLOW}Checking health of Todo AI Chatbot deployment...${NC}"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed or not in PATH${NC}"
    exit 1
fi

# Check namespace exists
if ! kubectl get namespace $NAMESPACE &> /dev/null; then
    echo -e "${RED}Namespace $NAMESPACE does not exist${NC}"
    exit 1
fi

echo -e "${YELLOW}Checking deployments...${NC}"
DEPLOYMENTS=$(kubectl get deployments -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

for deployment in $DEPLOYMENTS; do
    DESIRED=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.spec.replicas}')
    CURRENT=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.status.replicas}')
    UPDATED=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.status.updatedReplicas}')
    READY=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')

    if [ "$READY" = "$DESIRED" ] && [ "$UPDATED" = "$DESIRED" ]; then
        echo -e "${GREEN}✓ $deployment: $READY/$DESIRED replicas ready${NC}"
    else
        echo -e "${RED}✗ $deployment: $READY/$DESIRED replicas ready (desired: $DESIRED, current: $CURRENT, updated: $UPDATED)${NC}"
    fi
done

echo ""
echo -e "${YELLOW}Checking services...${NC}"
SERVICES=$(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

for service in $SERVICES; do
    TYPE=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.type}')
    SELECTOR=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.selector.app}')

    # Count matching pods
    MATCHING_PODS=$(kubectl get pods -n $NAMESPACE -l app=$SELECTOR --no-headers | wc -l)

    if [ "$MATCHING_PODS" -gt 0 ]; then
        echo -e "${GREEN}✓ $service ($TYPE): $MATCHING_PODS pods selected${NC}"
    else
        echo -e "${RED}✗ $service ($TYPE): No matching pods${NC}"
    fi
done

echo ""
echo -e "${YELLOW}Checking pods...${NC}"
PODS=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

for pod in $PODS; do
    STATUS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.phase}')
    READY_COUNT=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.containerStatuses[*].ready}' | tr ' ' '\n' | grep -c true)
    TOTAL_CONTAINERS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.containerStatuses[*]}' | wc -w)

    if [ "$STATUS" = "Running" ] && [ "$READY_COUNT" -eq "$TOTAL_CONTAINERS" ]; then
        echo -e "${GREEN}✓ $pod: $STATUS ($READY_COUNT/$TOTAL_CONTAINERS containers ready)${NC}"
    else
        echo -e "${RED}✗ $pod: $STATUS ($READY_COUNT/$TOTAL_CONTAINERS containers ready)${NC}"
        # Show logs for failed pods
        if [ "$STATUS" = "CrashLoopBackOff" ] || [ "$STATUS" = "Error" ]; then
            echo "  Pod logs:"
            kubectl logs $pod -n $NAMESPACE --tail=10
        fi
    fi
done

echo ""
echo -e "${YELLOW}Checking ingress...${NC}"
INGRESSES=$(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

if [ -n "$INGRESSES" ]; then
    for ingress in $INGRESSES; do
        HOSTS=$(kubectl get ingress $ingress -n $NAMESPACE -o jsonpath='{.spec.rules[*].host}')
        if [ -n "$HOSTS" ]; then
            echo -e "${GREEN}✓ $ingress: $HOSTS${NC}"
        else
            echo -e "${YELLOW}~ $ingress: No hosts configured${NC}"
        fi
    done
else
    echo -e "${YELLOW}~ No ingress resources found${NC}"
fi

echo ""
echo -e "${GREEN}Health check completed!${NC}"

# Summary
TOTAL_DEPLOYMENTS=$(echo $DEPLOYMENTS | wc -w)
READY_DEPLOYMENTS=$(for deployment in $DEPLOYMENTS; do
    DESIRED=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.spec.replicas}')
    READY=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')
    if [ "$READY" = "$DESIRED" ]; then echo 1; fi
done | wc -l)

TOTAL_PODS=$(echo $PODS | wc -w)
RUNNING_PODS=$(for pod in $PODS; do
    STATUS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.phase}')
    if [ "$STATUS" = "Running" ]; then echo 1; fi
done | wc -l)

echo ""
echo "Summary:"
echo "Deployments: $READY_DEPLOYMENTS/$TOTAL_DEPLOYMENTS ready"
echo "Pods: $RUNNING_PODS/$TOTAL_PODS running"