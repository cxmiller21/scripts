# Automation of AWS IAM User Access Key rotation process
#
# Script Assumptions:
# Users will have an "Active" and or "Inactive" Access Key
#   - if there are two "Active" keys there might be an error
#   - if there are two "Inactive" keys they will both be deleted
#
# This script will do the following:
# 1. Get IAM Users with the tag 'RotateAccessKey:true'
# 2. For each user it will
#   - Delete any inactive access keys
#   - Inactivate any active access keys
#   - Create a new access key
# 3. Generate a csv file with the new access keys
#

import boto3
from botocore.exceptions import ClientError
import datetime
import csv

# Include this for use with an AWS lambda function
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

resource = boto3.resource("iam")
client = boto3.client("iam", region_name="us-east-1")


def get_iam_users():
    users = []
    for user in resource.users.all():
        try:
            user_data = client.get_user(UserName=user.user_name)
            if len(user_data["User"]["Tags"]) > 0:
                for tag in user_data["User"]["Tags"]:
                    if "RotateAccessKey" in tag["Key"] and "true" in tag["Value"]:
                        users.append(user_data)
        except KeyError:
            pass
    return users


def build_user_access_key_dict(key):
    utc_datetime = key["CreateDate"]
    user_access_key = {
        "user_name": key["UserName"],
        "access_key_id": key["AccessKeyId"],
        "status": key["Status"],
        "secret_access_key": key["SecretAccessKey"],
        "utc_create_date": utc_datetime.isoformat(),
    }
    return user_access_key


def modify_user_access_keys(users):
    try:
        new_user_access_keys = []
        for user in users:
            user_name = user["User"]["UserName"]
            user_access_keys = client.list_access_keys(UserName=user_name)
            create_new_access_key = False
            if len(user_access_keys["AccessKeyMetadata"]) > 0:
                for access_key in user_access_keys["AccessKeyMetadata"]:
                    status = access_key["Status"]
                    access_key_id = access_key["AccessKeyId"]
                    if "Inactive" in status:
                        print(
                            f'AK was {access_key["Status"]}: Deleting {user_name}\'s old access key with ID {access_key_id}'
                        )
                        client.delete_access_key(
                            UserName=user_name, AccessKeyId=access_key_id
                        )
                        create_new_access_key = True
                    if "Active" in status:
                        print(
                            f'AK was {access_key["Status"]}: Inactivating {user_name}\'s primary access key with ID {access_key_id}'
                        )
                        client.update_access_key(
                            UserName=user_name,
                            AccessKeyId=access_key_id,
                            Status="Inactive",
                        )
                        create_new_access_key = True
            if create_new_access_key:
                print(f"Creating new Access Key for {user_name}")
                client_access_key = client.create_access_key(UserName=user_name)
                user_access_key = build_user_access_key_dict(
                    client_access_key["AccessKey"]
                )
                new_user_access_keys.append(user_access_key)
        return new_user_access_keys
    except Exception as e:
        print(e)


def generate_csv(new_access_keys):
    keys = new_access_keys[0].keys()
    with open("user_access_keys.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(new_access_keys)


def rotate_access_keys():
    print("Rotating AWS IAM User Access Keys")
    users = get_iam_users()
    if len(users):
        new_access_keys = modify_user_access_keys(users)
        print(
            f"Created {len(new_access_keys)} new user access keys.\nGenerating the user_access_keys.csv file"
        )
        generate_csv(new_access_keys)
    else:
        print("No user access keys to rotate")
    return 1


if __name__ == "__main__":
    rotate_access_keys()
