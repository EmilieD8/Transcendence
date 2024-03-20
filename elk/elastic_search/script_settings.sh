#!/bin/sh

cd  /usr/share/elasticsearch/bin

echo "root:$ROOT_PW" | chpasswd
./elasticsearch-users useradd "$ELASTICSEARCH_USER" -p "$ELASTICSEARCH_PW" -r superuser,kibana_system

chown -R elasticsearch:elasticsearch /usr/share/elasticsearch
mkdir -p /var/data/elasticsearch
mkdir -p /var/log/elasticsearch
chown -R elasticsearch:elasticsearch /var/data/elasticsearch
chown -R elasticsearch:elasticsearch /var/log/elasticsearch
usermod -d /usr/share/elasticsearch elasticsearch
usermod -s /bin/bash elasticsearch
su -s /bin/bash -c '/usr/share/elasticsearch/bin/elasticsearch' elasticsearch
