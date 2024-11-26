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

    def list_volumes(self):
        """Retrieves and lists EC2 volumes and their attached instance IDs from the specified region."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_volumes()
            volumes_info = []

            if "Volumes" in response and response["Volumes"]:
                for volume in response["Volumes"]:
                    volume_id = volume.get("VolumeId", "N/A")
                    volume_name = next(
                        (
                            tag["Value"]
                            for tag in volume.get("Tags", [])
                            if tag.get("Key") == "Name"
                        ),
                        "N/A",
                    )
                    volume_size = volume.get("Size", "N/A")
                    attached_instance_id = self.get_attached_instance_id(
                        volume.get("Attachments", [])
                    )
                    volumes_info.append(
                        [volume_id, volume_name, volume_size, attached_instance_id]
                    )

            if volumes_info:
                return volumes_info
            return "No volumes found"

        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def get_attached_instance_id(self, attachments):
        """Extracts the attached instance ID from volume attachment details."""
        if attachments:
            return attachments[0].get("InstanceId", "N/A")
        return "No attached instance"

    def enumerate_ec2_instances(self):
        """Retrieves and formats a list of EC2 instances."""
        instances = self.list_ec2_instances()
        if isinstance(instances, list):
            return self.format_as_ec2_table(instances)
        return instances

    def format_as_ec2_table(self, instances):
        """Formats EC2 instances data as a grid table for output."""
        headers = ["Instance ID", "Instance Name", "Region", "Public IP"]
        return tabulate(instances, headers, tablefmt="grid")

    def enumerate_volumes(self):
        """Retrieves and formats a list of EC2 volumes."""
        volumes = self.list_volumes()
        if isinstance(volumes, list):
            return self.format_as_volumes_table(volumes)
        return volumes

    def format_as_volumes_table(self, volumes):
        """Formats EC2 volumes data as a grid table for output."""
        headers = ["Volume ID", "Volume Name", "Size (GB)", "Attached Instance ID"]
        return tabulate(volumes, headers, tablefmt="grid")

    def describe_snapshots(self, OwnerIds):
        """Retrieves a list of snapshots owned by the specified AWS account."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_snapshots(OwnerIds=OwnerIds)
            snapshots_info = []
            for snapshot in response.get("Snapshots", []):
                snapshot_id = snapshot.get("SnapshotId", "N/A")
                volume_id = snapshot.get("VolumeId", "N/A")
                volume_size = snapshot.get("VolumeSize", "N/A")
                snapshots_info.append([snapshot_id, volume_id, volume_size])
            return snapshots_info
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def enumerate_snapshots(self):
        """Retrieves and formats a list of EC2 snapshots."""
        snapshots = self.describe_snapshots(OwnerIds=["self"])
        if isinstance(snapshots, list):
            return self.format_as_snapshots_table(snapshots)
        return snapshots

    def format_as_snapshots_table(self, snapshots):
        """Formats EC2 snapshots data as a grid table for output."""
        headers = ["Snapshot ID", "Volume ID", "Volume Size (GB)"]
        return tabulate(snapshots, headers, tablefmt="grid")

    def enumerate_elastic_ip(self):
        """Retrieves and formats a list of Elastic IP addresses."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_addresses()
            elastic_ips_info = []
            for address in response.get("Addresses", []):
                public_ip = address.get("PublicIp", "N/A")
                elastic_ips_info.append([public_ip])
            return elastic_ips_info
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def format_as_elastic_ip_table(self, elastic_ips):
        """Formats Elastic IP addresses data as a grid table for output."""
        headers = ["Public IP", "Instance ID"]
        return tabulate(elastic_ips, headers, tablefmt="grid")

    def enumerate_custom_amis(self):
        """Retrieves and formats a list of custom AMIs owned by the user."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_images(Owners=["self"])
            amis_info = []
            for image in response.get("Images", []):
                image_id = image.get("ImageId", "N/A")
                name = image.get("Name", "N/A")
                visibility = "Public" if image.get("Public", False) else "Private"
                creation_date = image.get("CreationDate", "N/A")
                amis_info.append([image_id, name, visibility, creation_date])
            return self.format_as_amis_table(amis_info)
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def format_as_amis_table(self, amis_info):
        """Formats AMIs data as a grid table for output."""
        headers = ["Image ID", "Name", "Visibility", "Creation Date"]
        return tabulate(amis_info, headers, tablefmt="grid")

    def enumerate_ssm_agent_status(self):
        """Checks and formats the SSM Agent status of EC2 instances."""
        ssm = self.session.client("ssm", region_name=self.region)
        try:
            response = ssm.describe_instance_information()
            ssm_info = []
            for instance in response.get("InstanceInformationList", []):
                instance_id = instance.get("InstanceId", "N/A")
                ping_status = instance.get("PingStatus", "N/A")  # Online/Offline
                agent_version = instance.get("AgentVersion", "N/A")
                platform_name = instance.get("PlatformName", "N/A")
                platform_version = instance.get("PlatformVersion", "N/A")
                ssm_info.append(
                    [
                        instance_id,
                        ping_status,
                        agent_version,
                        platform_name,
                        platform_version,
                    ]
                )
            if not ssm_info:
                return "No instances with SSM Agent found."
            return self.format_as_ssm_agent_table(ssm_info)
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def format_as_ssm_agent_table(self, ssm_info):
        """Formats SSM Agent status data as a grid table."""
        headers = [
            "Instance ID",
            "Ping Status",
            "Agent Version",
            "Platform Name",
            "Platform Version",
        ]
        return tabulate(ssm_info, headers, tablefmt="grid")

    def enumerate_security_groups(self):
        """
        Retrieves and formats a list of security groups associated
        with EC2 instances along with open ports and other relevant data.
        """
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            # Describe EC2 instances
            response = ec2.describe_instances()
            security_groups_info = []

            # Loop through instances and their associated security groups
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instance_id = instance.get("InstanceId", "N/A")
                    security_groups = instance.get("SecurityGroups", [])

                    for sg in security_groups:
                        group_id = sg.get("GroupId", "N/A")

                        # Retrieve security group rules (ports and sources)
                        security_group_rules = self.get_security_group_rules(group_id)

                        security_groups_info.append(
                            [instance_id, group_id, security_group_rules]
                        )

            return self.format_as_security_groups_table(security_groups_info)
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def get_security_group_rules(self, group_id):
        """Retrieves security group rules (open ports and sources)."""
        ec2 = self.session.client("ec2", region_name=self.region)
        try:
            response = ec2.describe_security_groups(GroupIds=[group_id])
            rules = []
            security_group = response["SecurityGroups"][0]

            # Iterate over ingress rules (inbound traffic)
            for rule in security_group.get("IpPermissions", []):
                from_port = rule.get("FromPort", "N/A")
                to_port = rule.get("ToPort", "N/A")
                ip_protocol = rule.get("IpProtocol", "N/A")
                cidr_blocks = rule.get("IpRanges", [])
                for cidr in cidr_blocks:
                    rules.append(
                        f"{ip_protocol} {from_port}-{to_port} from {cidr['CidrIp']}"
                    )

            # Iterate over egress rules (outbound traffic)
            for rule in security_group.get("IpPermissionsEgress", []):
                from_port = rule.get("FromPort", "N/A")
                to_port = rule.get("ToPort", "N/A")
                ip_protocol = rule.get("IpProtocol", "N/A")
                cidr_blocks = rule.get("IpRanges", [])
                for cidr in cidr_blocks:
                    rules.append(
                        f"{ip_protocol} {from_port}-{to_port} to {cidr['CidrIp']}"
                    )

            return (
                self.format_security_group_rules_multiline(rules)
                if rules
                else "No rules found"
            )
        except botocore.exceptions.ClientError as e:
            return f"Client error: {str(e)}"
        except botocore.exceptions.BotoCoreError as e:
            return f"BotoCore error: {str(e)}"

    def format_security_group_rules_multiline(self, rules):
        """Split long security group rules into multiple lines and format them."""
        formatted_rules = []
        for rule in rules:
            formatted_rules.append(f"    {rule.strip()};")  # Indent for new lines
        return "\n".join(formatted_rules)  # Join the lines back together

    def format_as_security_groups_table(self, security_groups_info):
        """Formats the security group data as a grid table."""
        headers = ["Instance ID", "Security Group ID", "Security Group Rules"]
        return tabulate(security_groups_info, headers, tablefmt="fancy_grid")
