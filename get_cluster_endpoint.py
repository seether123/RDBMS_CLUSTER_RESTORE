import boto3
from config import RDS_REGION,NEW_CLUSTER_IDENTIFIER  # Import the new cluster identifier

def get_new_cluster_endpoint():
    try:
        # Initialize the RDS client
        rds_client = boto3.client('rds', region_name=RDS_REGION)

        # Retrieve information about the newly created Aurora cluster
        response = rds_client.describe_db_clusters(DBClusterIdentifier=NEW_CLUSTER_IDENTIFIER)

        if 'DBClusters' in response and response['DBClusters']:
            new_cluster_endpoint = response['DBClusters'][0]['Endpoint']
            return new_cluster_endpoint
        else:
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the cluster endpoint: {str(e)}")
        return None

if __name__ == '__main__':
    cluster_endpoint = get_new_cluster_endpoint()
    if cluster_endpoint:
        print(f"New Aurora cluster endpoint: {cluster_endpoint}")
        with open('endpoint.py', 'w') as config_file:
           config_file.write(f"NEW_CLUSTER_ENDPOINT = '{cluster_endpoint}'\n")
           config_file.close()
    else:
        print(f"Unable to retrieve endpoint for cluster {NEW_CLUSTER_IDENTIFIER}")
