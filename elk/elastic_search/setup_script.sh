#!bin/bash

# chmod -R 777 /etc/elasticsearch/
# chmod -R 777 /etc/elasticsearch/certs

/usr/share/elasticsearch/bin/elasticsearch-certutil ca --pem --out /etc/elasticsearch/certs/ca.zip
cd /etc/elasticsearch/certs/
unzip ca.zip

/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --out /etc/elasticsearch/certs/elastic.zip \
  --name elastic \
  --ca-cert /etc/elasticsearch/certs/ca/ca.crt \
  --ca-key /etc/elasticsearch/certs/ca/ca.key \
  --dns localhost \
  --pem;

cd /etc/elasticsearch/certs/;
unzip elastic.zip


