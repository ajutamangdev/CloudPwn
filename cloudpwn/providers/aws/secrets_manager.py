"""
This module provides the Secrets class that handles the enumeration of Secret Manager services.
"""

import json
import boto3
from botocore.exceptions import ClientError
from rich import print as rich_print


class Secrets:
    """
    A class to interact with AWS Secrets Manager services using a specified AWS profile and region.

    This class provides methods to list secrets and retrieve secret values.
    """

    def __init__(self, profile: str, region: str):
        """
        Initializes the Secrets class with the specified AWS profile and region.
        """
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.client = self.session.client("secretsmanager")

    def list_secrets(self):
        """
        Retrieves and lists secrets from the specified AWS region.

        :return: A list of secret metadata or an empty list if no secrets are found.
        """

        print("╔═════════════════════════════════════════╗")
        print("║         Secrets Manager                 ║")
        print("╚═════════════════════════════════════════╝")

        try:
            secrets_list = []
            paginator = self.client.get_paginator("list_secrets")
            for page in paginator.paginate():
                secrets_list.extend(page.get("SecretList", []))
            return secrets_list
        except ClientError as e:
            print(f"Error listing secrets: {e}")
            return []

    def get_secret_value(self, secret_name: str):
        """
        Retrieves and decodes the value of a specific secret.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)

            secret_string = response.get("SecretString")
            if secret_string:
                try:
                    return json.loads(secret_string)
                except json.JSONDecodeError:
                    return secret_string

            return "Binary or unavailable secret"
        except self.client.exceptions.ResourceNotFoundException:
            return f"Secret '{secret_name}' not found."
        except self.client.exceptions.DecryptionFailure as e:
            return f"Failed to decrypt secret '{secret_name}': {e}"
        except ClientError as e:
            return f"Error retrieving secret '{secret_name}': {e}"

    def display_secrets(self):
        """
        Lists secrets and displays their metadata and values in JSON format.
        """
        secrets_list = self.list_secrets()
        if not secrets_list:
            print(
                json.dumps(
                    {"message": "No secrets found in AWS Secrets Manager."}, indent=4
                )
            )
            return ""

        secrets_data = []
        for secret in secrets_list:
            secret_name = secret["Name"]
            secret_value = self.get_secret_value(secret_name)
            secrets_data.append({"Secret Name": secret_name, "Value": secret_value})

        rich_print(json.dumps(secrets_data, indent=4))
        return ""
