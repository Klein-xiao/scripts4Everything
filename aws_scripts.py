# a. Enumerate S3 Buckets & Check Permissions
# Check for public buckets or misconfigured policies:
import boto3

s3 = boto3.client('s3')

# List all buckets
buckets = s3.list_buckets()
for bucket in buckets['Buckets']:
    print(f"Bucket: {bucket['Name']}")
    try:
        acl = s3.get_bucket_acl(Bucket=bucket['Name'])
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and 'AllUsers' in grant['Grantee']['URI']:
                print(f"[!] Public Access: {bucket['Name']}")
    except Exception as e:
        print(f"Error checking {bucket['Name']}: {e}")
# b. List IAM Users & Policies
# Identify users with excessive permissions:

import boto3

iam = boto3.client('iam')

users = iam.list_users()
for user in users['Users']:
    print(f"User: {user['UserName']}")
    policies = iam.list_user_policies(UserName=user['UserName'])
    for policy in policies['PolicyNames']:
        print(f"  Inline Policy: {policy}")

# c. Check for Publicly Accessible EC2 Snapshots
# Find publicly shared RDS/EBS snapshots:
import boto3

ec2 = boto3.client('ec2')

snapshots = ec2.describe_snapshots(OwnerIds=['self'])
for snapshot in snapshots['Snapshots']:
    if snapshot.get('Public', False):
        print(f"[!] Public Snapshot: {snapshot['SnapshotId']}")

# d. Dump EC2 Instance User Data
# Retrieve user data from EC2 instances (may contain secrets):
import boto3

ec2 = boto3.client('ec2')

instances = ec2.describe_instances()
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance: {instance['InstanceId']}")
        user_data = ec2.describe_instance_attribute(
            InstanceId=instance['InstanceId'],
            Attribute='userData'
        )
        if 'UserData' in user_data:
            print(user_data['UserData']['Value'])
# e. Check Public ECR Repositories
# Find public Elastic Container Registry (ECR) repositories:
import boto3

ecr = boto3.client('ecr')

repos = ecr.describe_repositories()
for repo in repos['repositories']:
    policy = ecr.get_repository_policy(repositoryName=repo['repositoryName'])
    if 'Allow public pull' in policy['policyText']:
        print(f"[!] Public ECR Repo: {repo['repositoryName']}")

