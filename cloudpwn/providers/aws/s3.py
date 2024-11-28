import boto3
from tabulate import tabulate
from botocore.exceptions import ClientError
from rich import print as rich_print


class S3:
    def __init__(self, profile, region):
        """
        Initialize the S3 client with the specified profile and region.
        """
        self.profile = profile
        self.region = region

        try:
            session = boto3.Session(profile_name=self.profile, region_name=self.region)
            self.s3_client = session.client("s3")
        except Exception as e:
            rich_print(f"[bold red]Error initializing S3 client: {e}[/bold red]")

    def list_buckets(self):
        """
        List all S3 buckets available in the account.
        Returns:
            List of bucket names.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║           S3 Buckets                ║")
        print("╚═════════════════════════════════════╝")

        try:
            response = self.s3_client.list_buckets()
            buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
            return buckets
        except ClientError as e:
            rich_print(f"[bold red]Error listing buckets: {e}[/bold red]")
            return []

    def enumerate(self):
        """
        List all S3 buckets with their names in a table.
        """
        buckets = self.list_buckets()
        if not buckets:
            rich_print("[bold yellow]No buckets found in the account.[/bold yellow]")
            return

        table_data = [[bucket] for bucket in buckets]
        headers = ["Bucket Name"]

        table = tabulate(table_data, headers=headers, tablefmt="grid")

        rich_print(table)
