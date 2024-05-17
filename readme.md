# Provider Utilization Dashboard

This program has three pods with three diffrent services: 
1) A shell script that runs periodically (the frequency is configurable) making a gRPCurl request to a server with reflection enabled to retrieve the current provider utilization data and store the JSON response in a database;
2) A NoSQL database (Couch DB) to store the server utilization log (JSON) retrieved above;
3) A web app with a dashboard to display the daily average of the provider utilization such as CPU, GPU, Memory and Storage allocated;

## Getting Started

These instructions will cover usage information the Cloudmos Deploy of this project.


### Deploying

You'll need an Akash wallet with at least 0.5 AKT. You can use any deploy tool that you would like to. I will use Cloudmos but you and use the Akash Console or the Akash CLI


#### Environment Variables

- `COUCHDB_USER` - The admin user for CouchDB.
- `COUCHDB_PASSWORD` - The password for the CouchDB admin user.
- `COUCHDB_URL` - The Couch DB URL, like: "http://admin:password@couchdb:5984" 
- `COUCHDB_DB_NAME` - The database name
- `COUCHDB_DESIGN_DOC` - The database design doc
- `COUCHDB_CPU_VIEW` - The database index for CPU data
- `COUCHDB_GPU_VIEW` - The database index for GPU data
- `COUCHDB_MEMORY_VIEW` - The database index for Memory data
- `COUCHDB_STORAGE_VIEW` - The database index for Storage data
- `PROVIDER_URL` - The provider URL the service will pull from
- `NODES` - The name of the nodes you are wanting to pull data from

Be aware that when changing the `COUCHDB_USER` and `COUCHDB_PASSWORD` values, it's necessary to change in both containers environment variables

#### Volumes

- `couchdb_data` - This is where CouchDB persists its data.


### Accessing the Applications

* CouchDB: To access CouchDB UI, navigate to URL that Cloudmos gives you in your web browser. Login with the COUCHDB_USER and COUCHDB_PASSWORD configured in your environment variables. You will need to add `/_utils/` to the end of your URl

    <img width="812" alt="Screenshot 2024-05-17 at 10 48 07 AM" src="https://github.com/Zblocker64/provider-stats/assets/105066639/fb215d9e-08bf-4db1-ab98-fddd1108bcad">


* Flask App: Your Flask application will be available at the url Cloudmos gives you. You can also set a custom domain specified in the SDL like I have.
<img width="597" alt="Screenshot 2024-05-17 at 10 48 38 AM" src="https://github.com/Zblocker64/provider-stats/assets/105066639/25c34023-404e-4ff1-949c-827e06fbc3d5">

* gRPC Poller: This service depends on the CouchDB and performs periodic polling, you can adjust the interval by setting the REQUEST_INTERVAL environment variable. No need to access this after deployment.


### Persistent Data

The composition is configured with named volumes so your data will be persistent across container restarts.
