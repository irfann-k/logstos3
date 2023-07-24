import boto3
from datetime import datetime



def lambda_handler(event, context):
    # Get the log group and log stream names from the CloudWatch Logs event
    log_group = 'error.log'
    log_stream = 'nginx_error_logs'
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    time = datetime.now()
    
    # Set the S3 bucket and key
    s3_bucket = 'schbang.server.logs'
    s3_key = f'{log_group}/{log_stream}{time}.txt'
    
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

def get_log_events(log_group, log_stream):
    # Create a CloudWatch Logs client
    logs_client = boto3.client('logs')
    
    # Get the latest log events from CloudWatch Logs
    response = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startFromHead=True
    )
    
    # Return the log events
    return response['events']
