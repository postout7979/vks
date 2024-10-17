#!/bin/bash
# Supervisor control plane VIP from Load balancer
VSPHERE_WITH_TANZU_CONTROL_PLANE_IP=10.10.152.1
# vSphere account that is registered to vSphere Namespace
VSPHERE_WITH_TANZU_USERNAME=ichoi@vsphere.local
VSPHERE_WITH_TANZU_PASSWORD=VMware1!
# vSphere Namespace name
VSPHERE_WITH_TANZU_NAMESPACE=ns-ichoi
# Tanzu Kubernetes Cluster name
VSPHERE_WITH_TANZU_TKC_NAME=beta-tkg01
# Kuberctl binary path
KUBECTL_PATH=/usr/bin/kubectl

KUBECTL_VSPHERE_LOGIN_COMMAND=$(expect -c "
spawn $KUBECTL_PATH vsphere login --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_NAMESPACE --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_TKC_NAME
expect \"*?assword:*\"
send -- \"$VSPHERE_WITH_TANZU_PASSWORD\r\"
expect eof
")
