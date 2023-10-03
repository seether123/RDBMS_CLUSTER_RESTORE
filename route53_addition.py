import boto3
from endpoint import NEW_CLUSTER_ENDPOINT
from config import (
    ROUTE53_HOSTED_ZONE_ID,
    ROUTE53_RECORD_NAME,
)
# Initialize the Route 53 client
route53_client = boto3.client('route53')

# Define the parameters for the new DNS record
hosted_zone_id = 'your_hosted_zone_id'  # Replace with your hosted zone ID
record_name = 'example.com'  # Replace with the DNS record name
record_type = 'A'  # Replace with the desired record type (e.g., A, CNAME, MX, etc.)
ttl = 300  # Specify the TTL (Time to Live) in seconds
resource_value = '1.2.3.4'  # Replace with the IP address or value for the record

# Check if the DNS record already exists
existing_records = route53_client.list_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    StartRecordName=record_name,
    StartRecordType=record_type,
    MaxItems='1'  # Limit the response to one record
)

if 'ResourceRecordSets' in existing_records:
    for record_set in existing_records['ResourceRecordSets']:
        if record_set['Name'] == record_name and record_set['Type'] == record_type:
            print(f"DNS record '{record_name}' of type '{record_type}' already exists.")
            # If the record exists, you can choose to update it or take other actions if needed.
            # You can add your update logic here if necessary.
            break
else:
    # Create a change batch to add the new record
    change_batch = {
        'Changes': [
            {
                'Action': 'CREATE',  # Use 'CREATE' to add a new record
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type,
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': resource_value}]
                }
            }
        ]
    }

    # Apply the change batch to create the DNS record
    route53_response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch
    )

    print("DNS record added successfully.")
