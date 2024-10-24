import boto3
from tabulate import tabulate
import csv
from datetime import datetime
from config.settings import Config
import os


class EC2:
    def __init__(self, profile: str, region: str):
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.region = region

    def list_ec2_instances(self):
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

                return instances_info if instances_info else "No instances found"
            else:
                return "No reservations found"
        except Exception as e:
            return {"error": str(e)}

    def get_ec2_instances_raw(self):
        """Return raw EC2 instance data for CSV export."""
        return self.list_ec2_instances()

    def save_ec2_to_csv(self, instances):
        """Saves EC2 instance data to a CSV file."""
        config = Config()
        outputs = config.create_output_dir()
        filename = os.path.join(
            outputs, f"ec2_instances_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        headers = ["Instance ID", "Instance Name", "Region", "Public IP"]

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(instances)

    def enumerate_ec2_instances(self):
        """Retrieves and formats a list of EC2 instances."""
        instances = self.list_ec2_instances()
        if isinstance(instances, list):
            return self.format_as_table(instances)
        else:
            return instances

    def format_as_table(self, instances):
        """Formats the results as a grid table for output."""
        headers = ["Instance ID", "Instance Name", "Region", "Public IP"]
        return tabulate(instances, headers, tablefmt="grid")
