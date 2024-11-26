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
        print("╔═════════════════════════════════════╗")
        print("║         EC2 Instances               ║")
        print("╚═════════════════════════════════════╝")

        formatted_ec2 = ec2.enumerate_ec2_instances()
        rich_print(formatted_ec2)

        print("╔═════════════════════════════════════╗")
        print("║         Volumes                     ║")
        print("╚═════════════════════════════════════╝")
        volume = ec2.enumerate_volumes()
        rich_print(volume)

        print("╔═════════════════════════════════════╗")
        print("║         Snapshot Results            ║")
        print("╚═════════════════════════════════════╝")
        snapshots = ec2.enumerate_snapshots()
        rich_print(snapshots)

        print("╔═════════════════════════════════════╗")
        print("║         Elastic IP Results          ║")
        print("╚═════════════════════════════════════╝")
        eip = ec2.enumerate_elastic_ip()
        rich_print(eip)

        print("╔═════════════════════════════════════╗")
        print("║         AMI Results                 ║")
        print("╚═════════════════════════════════════╝")
        amis = ec2.enumerate_custom_amis()
        rich_print(amis)

        print("╔═════════════════════════════════════╗")
        print("║         SSM Agent                   ║")
        print("╚═════════════════════════════════════╝")
        ssm_agent = ec2.enumerate_ssm_agent_status()
        rich_print(ssm_agent)

        print("╔════════════════════════════════════════════╗")
        print("║            Security Groups Info            ║")
        print("╚════════════════════════════════════════════╝")
        security_groups_ec2 = ec2.enumerate_security_groups()
        rich_print(security_groups_ec2)
    else:
        print("Unsupported services")
