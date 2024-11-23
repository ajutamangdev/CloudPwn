"""
This module provides functions that perform enumeration processes for AWS services.
Full enumerations handle all AWS services and save the data in a CSV format.
It also supports specific enumeration of AWS services.
"""

from rich import print as rich_print
from cloudpwn.providers.aws.ec2 import EC2
from cloudpwn.config.settings import Config


def aws_enumerate_all(profile):
    """
    Performs full enumeration of AWS services across all regions and saves results to a CSV file.
    """
    config = Config()
    all_regions = config.AWS_REGIONS

    for region in all_regions:
        print(f"[bold blue]Enumerating AWS services in region: {region}[/bold blue]")
        enumerate_specific_service("ec2", profile, region)


def enumerate_specific_service(service, profile, region):
    """Enumerates instances for the specified AWS service."""
    service = str(service).lower()

    if service == "ec2":
        ec2 = EC2(profile, region)
        formatted_output = ec2.enumerate_ec2_instances()
        rich_print(formatted_output)
    else:
        print("Unsupported services")
