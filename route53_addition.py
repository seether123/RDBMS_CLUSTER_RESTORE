import boto3
from endpoint import NEW_CLUSTER_ENDPOINT
from config import (
    ROUTE53_HOSTED_ZONE_ID,
    ROUTE53_RECORD_NAME,
)

def update_route53_record(cluster_endpoint, hosted_zone_id, record_name):
    try:
        # Initialize the Route 53 client
        route53_client = boto3.client('route53')

        # Define the change batch
        change_batch = {
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'CNAME',
                        'TTL': 300,  # Adjust the TTL as needed
                        'ResourceRecords': [
                            {
                                'Value': cluster_endpoint,
                            },
                        ],
                    },
                },
            ],
        }

        # Update the Route 53 record set
        route53_response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )

        print(f"Route 53 record updated successfully!")

    except Exception as e:
        print(f"Error updating Route 53 record: {str(e)}")

if __name__ == '__main__':
    update_route53_record(NEW_CLUSTER_ENDPOINT, ROUTE53_HOSTED_ZONE_ID, ROUTE53_RECORD_NAME)
