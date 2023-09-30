import boto3
from config import RDS_REGION, NEW_CLUSTER_IDENTIFIER, NEW_INSTANCE_IDENTIFIER,RDS_INSTANCE_CLASS, RDS_AVAILABILITY_ZONE

def create_rds_instance(cluster_identifier, instance_identifier):
    try:
        # Initialize the RDS client
        rds_client = boto3.client('rds', region_name=RDS_REGION)

        # Specify the instance configuration
        instance_class = RDS_INSTANCE_CLASS  # You can change this to the desired instance type
        availability_zone = RDS_AVAILABILITY_ZONE  # You can change this to your preferred AZ

        # Create the RDS instance
        response = rds_client.create_db_instance(
            DBInstanceIdentifier=instance_identifier,
            DBInstanceClass=RDS_INSTANCE_CLASS,
            Engine='aurora-postgresql',
            DBClusterIdentifier=cluster_identifier,
            AvailabilityZone=RDS_AVAILABILITY_ZONE,
            PubliclyAccessible=False,  # Set to True if you want it to be publicly accessible
            AutoMinorVersionUpgrade=True,  # Set to True for automatic minor version upgrades
        )

        print(f"Creating RDS instance {instance_identifier}...")

        # Wait for the instance creation to complete
        rds_client.get_waiter('db_instance_available').wait(DBInstanceIdentifier=instance_identifier)

        print(f"RDS instance {instance_identifier} created successfully!")

    except Exception as e:
        print(f"Error creating RDS instance: {str(e)}")

if __name__ == '__main__':
    create_rds_instance(NEW_CLUSTER_IDENTIFIER, NEW_INSTANCE_IDENTIFIER)

