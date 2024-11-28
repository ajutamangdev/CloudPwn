import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate
from rich import print as rich_print


class Route53:
    def __init__(self, profile, region):
        """
        Initialize the Route 53 client with the specified profile and region.
        """
        self.profile = profile
        self.region = region

        try:
            session = boto3.Session(profile_name=self.profile, region_name=self.region)
            self.route53_client = session.client("route53")
        except Exception as e:
            rich_print(f"[bold red]Error initializing Route 53 client: {e}[/bold red]")

    def list_hosted_zones(self):
        """
        List all Route 53 hosted zones in the account.
        Returns:
            List of hosted zone IDs and names.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║        Route 53 Hosted Zones        ║")
        print("╚═════════════════════════════════════╝")

        try:
            response = self.route53_client.list_hosted_zones()
            hosted_zones = response.get("HostedZones", [])
            return hosted_zones
        except ClientError as e:
            rich_print(f"[bold red]Error listing hosted zones: {e}[/bold red]")
            return []

    def list_records(self, hosted_zone_id):
        """
        List all records in a specific hosted zone.
        """
        try:
            response = self.route53_client.list_resource_record_sets(
                HostedZoneId=hosted_zone_id
            )
            records = response.get("ResourceRecordSets", [])
            return records
        except ClientError as e:
            rich_print(
                f"[bold red]Error listing records for hosted zone {hosted_zone_id}: {e}[/bold red]"
            )
            return []

    def enumerate(self):
        """
        Enumerate Route 53 hosted zones and their records.
        """
        hosted_zones = self.list_hosted_zones()
        if not hosted_zones:
            rich_print(
                "[bold yellow]No hosted zones found in the account.[/bold yellow]"
            )
            return

        for zone in hosted_zones:
            zone_name = zone["Name"]
            zone_id = zone["Id"]
            print(f"\nHosted Zone: {zone_name} (ID: {zone_id})")

            records = self.list_records(zone_id)
            if not records:
                rich_print(
                    "[bold yellow]No records found in this hosted zone.[/bold yellow]"
                )
                continue

            table_data = [
                [record["Name"], record["Type"], record.get("TTL", "N/A")]
                for record in records
            ]
            headers = ["Record Name", "Record Type", "TTL"]

            rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))
