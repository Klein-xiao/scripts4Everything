#!/usr/bin/env python3
import boto3
import base64

def enum_s3():
    print("\n📦 S3 Buckets")
    try:
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()['Buckets']
        for b in buckets:
            print(f"  [+] {b['Name']}")
    except Exception as e:
        print("  [-] Error:", e)

def enum_iam_users():
    print("\n👤 IAM Users & Policies")
    try:
        iam = boto3.client('iam')
        users = iam.list_users()['Users']
        for user in users:
            print(f"  [+] {user['UserName']}")
            attached = iam.list_attached_user_policies(UserName=user['UserName'])['AttachedPolicies']
            for p in attached:
                print(f"     ↳ Attached Policy: {p['PolicyName']}")
    except Exception as e:
        print("  [-] Error:", e)

def enum_ec2_userdata():
    print("\n🖥️ EC2 User Data")
    try:
        ec2 = boto3.client('ec2')
        reservations = ec2.describe_instances()['Reservations']
        for res in reservations:
            for inst in res['Instances']:
                iid = inst['InstanceId']
                print(f"  [+] Instance: {iid}")
                data = ec2.describe_instance_attribute(InstanceId=iid, Attribute='userData')
                val = data['UserData'].get('Value', '')
                if val:
                    decoded = base64.b64decode(val).decode()
                    print(f"     ↳ UserData:\n{decoded}")
                else:
                    print("     ↳ No UserData.")
    except Exception as e:
        print("  [-] Error:", e)

def enum_lambda():
    print("\n🧬 Lambda Functions")
    try:
        lamb = boto3.client('lambda')
        funcs = lamb.list_functions()['Functions']
        for f in funcs:
            print(f"  [+] {f['FunctionName']} - {f['Runtime']} - {f['Role']}")
    except Exception as e:
        print("  [-] Error:", e)

def enum_rds_snapshots():
    print("\n📚 Public RDS Snapshots")
    try:
        rds = boto3.client('rds')
        snaps = rds.describe_db_snapshots(SnapshotType='public')['DBSnapshots']
        for s in snaps:
            print(f"  [+] Snapshot: {s['DBSnapshotIdentifier']} | Instance: {s['DBInstanceIdentifier']}")
    except Exception as e:
        print("  [-] Error:", e)

def enum_ecr():
    print("\n📦 ECR Repositories")
    try:
        ecr = boto3.client('ecr')
        repos = ecr.describe_repositories()['repositories']
        for repo in repos:
            name = repo['repositoryName']
            print(f"  [+] Repo: {name}")
            try:
                pol = ecr.get_repository_policy(repositoryName=name)
                print("     ↳ Public Policy:", pol['policyText'])
            except:
                print("     ↳ No public policy.")
    except Exception as e:
        print("  [-] Error:", e)

def enum_cloudtrail():
    print("\n📜 CloudTrail Trails")
    try:
        ct = boto3.client('cloudtrail')
        trails = ct.describe_trails()['trailList']
        for t in trails:
            print(f"  [+] {t['Name']} | Multi-region: {t['IsMultiRegionTrail']}")
    except Exception as e:
        print("  [-] Error:", e)

def run_all():
    enum_s3()
    enum_iam_users()
    enum_ec2_userdata()
    enum_lambda()
    enum_rds_snapshots()
    enum_ecr()
    enum_cloudtrail()

if __name__ == "__main__":
    run_all()
