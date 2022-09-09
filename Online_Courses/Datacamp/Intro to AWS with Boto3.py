'''
S3 
- allows the storage of any file on the cloud, being accessible through a link by anyone in the world.
- 'buckets' are like folders; 'objects' are files. You can only store objects in buckets.
- can be used as a filesystem for a website
- can generate logs
- bucket names must be unique
'''

# Generate the boto3 client for interacting with S3
s3 = boto3.client('s3', region_name='us-east-1', 
                        # Set up AWS credentials 
                        aws_access_key_id='AWS_KEY_ID', 
                        aws_secret_access_key='AWS_SECRET')
# List the buckets
buckets = s3.list_buckets()
print(buckets)

# create buckets
response_staging = s3.create_bucket(Bucket='gim-staging')
response_processed = s3.create_bucket(Bucket='gim-processed')
response_test = s3.create_bucket(Bucket='gim-test')

# delete buckets with name containing 'gid'
response = s3.list_buckets()

# Delete all the buckets with 'gim', create replacements.
for bucket in response['Buckets']:
  if 'gim' in bucket['Name']:
      s3.delete_bucket(Bucket=bucket['Name'])
    
s3.create_bucket(Bucket='gid-staging')
s3.create_bucket(Bucket='gid-processed')
  
# Print bucket listing after deletion
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])
