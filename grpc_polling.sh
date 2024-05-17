#!/bin/sh

# Wait 10 seconds before running the script for the first time
sleep 10

# Create the CouchDB name using the HTTP API. (Specially when running the first time)
curl -X PUT "$COUCHDB_URL/$DB_NAME"
curl -X PUT "$COUCHDB_URL/_users"

# Create the CouchDB index using the HTTP API. (Specially when running the first time)
curl -X PUT "$COUCHDB_URL/$DB_NAME/_design/utilization" -H "Content-Type: application/json" --data-binary @database_index.json

while true; do
  # The variables are defined in the environment

  # Make gRPC request to retrieve the server status

response=$(grpcurl -insecure ${PROVIDER_URL}:8444 akash.provider.v1.ProviderRPC.GetStatus)


  # Save the response in a CouchDB document by using the CouchDB HTTP API.
  curl -X POST "$COUCHDB_URL/$DB_NAME" \
       -H "Content-Type: application/json" \
       -d "$response"

  # echo "$response"

  # Interval between gRPC requests
  sleep "$REQUEST_INTERVAL"
done
