#!bin/bash

# Run the Elasticsearch reset password command, redirecting input from a file
#!/bin/bash

# Run the Elasticsearch reset password command with inline input

/usr/share/elasticsearch/bin/elasticsearch-reset-password -i -u elastic --url https://localhost:9200 << EOF
y
$ELASTIC_PASSWORD
$ELASTIC_PASSWORD
EOF

#check the connection: curl -X GET -u elastic:$ELASTIC_PASSWORD https://localhost:9200 --cacert /etc/elasticsearch/certs/ca/ca.crt