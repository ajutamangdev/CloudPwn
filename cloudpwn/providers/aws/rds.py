"""
This module provides the RDS class that handles the enumeration of RDS services.
"""

import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate


class RDS:
    """
    A class to interact with Amazon RDS services using a specified AWS profile and region.

    This class provides methods to enumerate RDS instances, clusters, and snapshots.
    """

    def __init__(self, profile: str, region: str):
        """
        Initializes the RDS class with the specified AWS profile and region.
        """
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.client = self.session.client("rds")

    def list_rds_instances(self):
        """
        Retrieves and lists RDS instances in the specified region.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║          RDS Instances Info         ║")
        print("╚═════════════════════════════════════╝")

        try:
            instances = self.client.describe_db_instances()
            return instances.get("DBInstances", [])
        except ClientError as e:
            print(f"Error listing RDS instances: {e}")
            return []

    def list_rds_clusters(self):
        """
        Retrieves and lists RDS clusters in the specified region.
        """
        try:
            clusters = self.client.describe_db_clusters()
            return clusters.get("DBClusters", [])
        except ClientError as e:
            print(f"Error listing RDS clusters: {e}")
            return []

    def list_rds_snapshots(self):
        """
        Retrieves and lists RDS snapshots in the specified region.
        """
        try:
            snapshots = self.client.describe_db_snapshots()
            return snapshots.get("DBSnapshots", [])
        except ClientError as e:
            print(f"Error listing RDS snapshots: {e}")
            return []

    def enumerate_rds_instances(self):
        """
        Enumerates and displays RDS instances in a table format using tabulate.
        """
        instances = self.list_rds_instances()
        if not instances:
            print("No RDS instances found.")
        else:
            headers = ["Instance Identifier", "Engine", "Status", "Endpoint"]
            table = []
            for instance in instances:
                table.append(
                    [
                        instance["DBInstanceIdentifier"],
                        instance["Engine"],
                        instance["DBInstanceStatus"],
                        (
                            instance["Endpoint"]["Address"]
                            if "Endpoint" in instance
                            else "N/A"
                        ),
                    ]
                )
            print(tabulate(table, headers=headers, tablefmt="grid"))
        return ""

    def enumerate_rds_clusters(self):
        """
        Enumerates and displays RDS clusters in a table format using tabulate.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║           RDS Clusters Info         ║")
        print("╚═════════════════════════════════════╝")

        clusters = self.list_rds_clusters()
        if not clusters:
            print("No RDS clusters found.")
        else:
            headers = ["Cluster Identifier", "Engine", "Status"]
            table = []
            for cluster in clusters:
                table.append(
                    [
                        cluster["DBClusterIdentifier"],
                        cluster["Engine"],
                        cluster["Status"],
                    ]
                )
            print(tabulate(table, headers=headers, tablefmt="grid"))
        return ""

    def enumerate_rds_snapshots(self):
        """
        Enumerates and displays RDS snapshots in a table format using tabulate,
        including the public/private status of the snapshot.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║          RDS Snapshots Info         ║")
        print("╚═════════════════════════════════════╝")

        snapshots = self.list_rds_snapshots()
        if not snapshots:
            print("No RDS snapshots found.")
        else:
            headers = [
                "Snapshot Identifier",
                "Instance Identifier",
                "Status",
                "Public/Private",
            ]
            table = []
            for snapshot in snapshots:
                # Checking public/private snapshot status (this is a simplified approach)
                public_status = "Public" if snapshot.get("Public", False) else "Private"
                table.append(
                    [
                        snapshot["DBSnapshotIdentifier"],
                        snapshot["DBInstanceIdentifier"],
                        snapshot["Status"],
                        public_status,
                    ]
                )
            print(tabulate(table, headers=headers, tablefmt="grid"))
        return ""
