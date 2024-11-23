"""
This module provides the EC2 class that handles the enumeration of EC2 services.
"""

import boto3
import botocore.exceptions
from tabulate import tabulate


class EC2:
    """
    A class to interact with AWS EC2 services using a specified AWS profile and region.

    This class provides methods to list EC2 instances and retrieve instance details
    like instance ID, name, region, and public IP address.
    """

    def __init__(self, profile: str, region: str):
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.region = region

    def list_ec2_instances(self):
        """Retrieves and lists EC2 instance details from the specified region."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_instances()
            instances_info = []

            if "Reservations" in response and response["Reservations"]:
                for reservation in response["Reservations"]:
                    for instance in reservation.get("Instances", []):
                        instance_id = instance.get("InstanceId", "N/A")
                        instance_name = next(
                            (
                                tag["Value"]
                                for tag in instance.get("Tags", [])
                                if tag.get("Key") == "Name"
                            ),
                            "N/A",
                        )
                        public_ip = instance.get("PublicIpAddress", "N/A")
                        instances_info.append(
                            [instance_id, instance_name, self.region, public_ip]
                        )

            if instances_info:
                return instances_info
            return "No instances found"

        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def get_ec2_instances_raw(self):
        """Return raw EC2 instance data for CSV export."""
        return self.list_ec2_instances()

    def enumerate_ec2_instances(self):
        """Retrieves and formats a list of EC2 instances."""
        instances = self.list_ec2_instances()
        if isinstance(instances, list):
            return self.format_as_table(instances)
        return instances

    def format_as_table(self, instances):
        """Formats the results as a grid table for output."""
        headers = ["Instance ID", "Instance Name", "Region", "Public IP"]
        return tabulate(instances, headers, tablefmt="grid")
