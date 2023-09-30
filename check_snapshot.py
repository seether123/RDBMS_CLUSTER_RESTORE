import boto3
from datetime import datetime, timedelta
from config import RDS_REGION, RDS_CLUSTER_IDENTIFIER

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

if __name__ == '__main__':
    # Example usage of the RDSSnapshotManager class
    snapshot_manager = RDSSnapshotManager(RDS_REGION, RDS_CLUSTER_IDENTIFIER)
    snapshot_manager.list_snapshots_created_today()

    # Check if a source snapshot was found and print it
    if snapshot_manager.source_snapshot_identifier:
        print(f"Source snapshot identifier: {snapshot_manager.source_snapshot_identifier}")
    else:
        print("No source snapshot available.")
