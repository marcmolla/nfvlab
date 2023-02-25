#!/bin/bash
[ -z "$SUDO_USER" ] && echo "Use sudo!"
[ -z "$SUDO_USER" ] && exit 1
K8S_VERSION="1.25-strict/stable"
JUJU_VERSION="3.0/stable"
apt update && apt upgrade -y
for f in $(snap list | egrep '(microk8s|juju|charmcraft)' | awk '{print $1}')
do
  echo "Removing installed $f snap"
  snap remove $f --purge
done

echo "===== Installing microk8s ====="
snap install microk8s --channel $K8S_VERSION
usermod -a -G microk8s student
chown -f -R student ~student/.kube
microk8s enable hostpath-storage dns

snap alias microk8s.kubectl kubectl


#
# Remember that you are running as sudo
#
CONFIG_YAML=/home/$SUDO_USER/kubeconfig.yaml
microk8s.config > $CONFIG_YAML
chown $SUDO_UID:$SUDO_GID $CONFIG_YAML

echo "===== Installing juju ====="
snap install juju --channel $JUJU_VERSION
mkdir -p ~student/.local/share

echo "===== Installing charmcraft ====="
snap install charmcraft --classic

echo "===== Initiating lxd ====="
cat <<EOF |  lxd init --preseed
config: {}
networks:
- config:
    ipv4.address: auto
    ipv6.address: none
  description: ""
  name: lxdbr0
  type: ""
  project: default
storage_pools:
- config:
    size: 7GiB
  description: ""
  name: default
  driver: zfs
profiles:
- config: {}
  description: ""
  devices:
    eth0:
      name: eth0
      network: lxdbr0
      type: nic
    root:
      path: /
      pool: default
      type: disk
  name: default
projects: []
cluster: null
EOF
usermod -a -G lxd student
echo "**********************************************"
echo "* Please type newgrp microk8s and newgrp lxd *"
echo "**********************************************"