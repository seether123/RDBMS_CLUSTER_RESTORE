from endpoint import NEW_CLUSTER_ENDPOINT
        route53_client = boto3.client('route53')
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
