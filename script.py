import boto3

   # Get the log group and log stream names from the CloudWatch Logs event
log_group = "arn:aws:logs:ap-south-1:018474877703:log-group:Nginx_access_logs:*"
log_stream = "Grafana_source"
    
def get_log_events(log_group, log_stream):
    # Create a CloudWatch Logs client
    logs_client = boto3.client('logs')
    
    # Create an S3 client
s3_client = boto3.client('s3')
    
    # Set the S3 bucket and key
s3_bucket = 'grafanalogexport'
s3_key = f'{log_group}/{log_stream}'
    
try:
    # Get the log events from CloudWatch Logs
    log_events = get_log_events(log_group, log_stream)
        
    # Prepare the log data as a single string
    log_data = '\n'.join(log['message'] for log in log_events)
    
    # Upload the log data to S3
    s3_client.put_object(
         Bucket=s3_bucket,
        Key=s3_key,
        Body=log_data
    )
        
    print(f'Logs pushed to S3 bucket: s3://{s3_bucket}/{s3_key}')
        
except Exception as e:
    print(f'Error pushing logs to S3: {e}')
    raise e


    
    # Get the latest log events from CloudWatch Logs
    response = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startFromHead=True
    )
    
    # Return the log events
    return response['events']
