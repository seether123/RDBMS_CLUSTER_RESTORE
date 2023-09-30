import boto3
from datetime import datetime, timedelta

class RDSSnapshotManager:
    def __init__(self, region, cluster_identifier):
        self.region = region
        self.cluster_identifier = cluster_identifier
        self.rds_client = boto3.client('rds', region_name=region)
        self.source_snapshot_identifier = None  # Initialize as None

    def list_snapshots_created_today(self):
        # List the snapshots for the specified RDS cluster
        response = self.rds_client.describe_db_cluster_snapshots(DBClusterIdentifier=self.cluster_identifier)

        # Get the current date
        current_date = datetime.now()
        one_day_ago = current_date - timedelta(days=1)

        # Extract and print the snapshot names created today
        snapshot_names = []

        for snapshot in response['DBClusterSnapshots']:
            snapshot_creation_date = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
            if snapshot_creation_date >= one_day_ago and snapshot_creation_date < current_date and snapshot['SnapshotType'] == 'automated':
                snapshot_names.append(snapshot['DBClusterSnapshotIdentifier'])

        if snapshot_names:
            print(f"Snapshots created today for cluster {self.cluster_identifier}:")
            for name in snapshot_names:
                print(name)

            # Store the first snapshot in the list as the source snapshot identifier
            self.source_snapshot_identifier = snapshot_names[0]
        else:
            print(f"No snapshots created yesterday for cluster {self.cluster_identifier}.")


    def restore_cluster_from_snapshot(self, new_cluster_identifier):
        if self.source_snapshot_identifier:
            print(f"Using source snapshot identifier: {self.source_snapshot_identifier}")

            # Initialize the RDS client
            rds_client = boto3.client('rds', region_name=self.region)

            # Get information about the source cluster
            source_cluster = rds_client.describe_db_clusters(DBClusterIdentifier=self.cluster_identifier)['DBClusters'][0]
            response = rds_client.restore_db_cluster_from_snapshot(
                DBClusterIdentifier=new_cluster_identifier,
                SnapshotIdentifier=self.source_snapshot_identifier,
                Engine='aurora-postgresql',
                EngineVersion='14.6',
                DBSubnetGroupName=source_cluster['DBSubnetGroup'],
                #VpcSecurityGroupIds=source_cluster['VpcSecurityGroups'],
                AvailabilityZones=source_cluster['AvailabilityZones'],
                #BackupRetentionPeriod=source_cluster['BackupRetentionPeriod'],
                #PreferredMaintenanceWindow=source_cluster['PreferredMaintenanceWindow'],
                #Port=source_cluster['Port'],
                #DBClusterParameterGroupName=source_cluster['DBClusterParameterGroup'],
            )

            # Wait for the new cluster to become available
            rds_client.get_waiter('db_cluster_available').wait(
                DBClusterIdentifier=new_cluster_identifier
            )

            # Check the response for any errors
            if 'DBCluster' in response:
                print(f"New Aurora cluster '{new_cluster_identifier}' created successfully.")
            else:
                print("Error creating Aurora cluster.")
        else:
            print("No source snapshot available.")
