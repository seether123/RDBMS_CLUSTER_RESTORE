# main.py
from rds_snapshot_manager import RDSSnapshotManager
from config import RDS_REGION, RDS_CLUSTER_IDENTIFIER, NEW_CLUSTER_IDENTIFIER

if __name__ == '__main__':
    # Create an instance of the RDSSnapshotManager
    snapshot_manager = RDSSnapshotManager(RDS_REGION, RDS_CLUSTER_IDENTIFIER)

    # List snapshots created today for the specified RDS cluster
    snapshot_manager.list_snapshots_created_yesterday()

    # Check if a source snapshot was found and print it
    if snapshot_manager.source_snapshot_identifier:
        print(f"Source snapshot identifier: {snapshot_manager.source_snapshot_identifier}")
        snapshot_manager.restore_cluster_from_snapshot(NEW_CLUSTER_IDENTIFIER)
    else:
        print("No source snapshot available.")
