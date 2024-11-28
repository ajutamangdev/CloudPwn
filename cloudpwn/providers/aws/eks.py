import boto3
from tabulate import tabulate
from rich import print as rich_print
from botocore.exceptions import ClientError


class EKS:
    def __init__(self, profile, region):
        """
        Initialize the EKS client with the specified profile and region.
        """
        session = boto3.Session(profile_name=profile, region_name=region)
        self.eks_client = session.client("eks")

    def list_clusters(self):
        """
        List all EKS clusters in the account.
        """
        try:
            response = self.eks_client.list_clusters()
            clusters = response.get("clusters", [])
            return clusters
        except ClientError as e:
            print(f"Error listing clusters: {e}")
            return []

    def describe_cluster(self, cluster_name):
        """
        Describe an EKS cluster.
        """
        try:
            response = self.eks_client.describe_cluster(name=cluster_name)
            cluster_info = response.get("cluster", {})
            return {
                "Endpoint Public Access": cluster_info.get(
                    "resourcesVpcConfig", {}
                ).get("endpointPublicAccess"),
                "Public Access CIDRs": cluster_info.get("resourcesVpcConfig", {}).get(
                    "publicAccessCidrs"
                ),
            }
        except ClientError as e:
            print(f"Error describing cluster {cluster_name}: {e}")
            return {}

    def enumerate(self):
        """
        Perform enumeration for all EKS resources.
        """
        print("\n╔═════════════════════════════════════╗")
        print("║          EKS Cluster Info           ║")
        print("╚═════════════════════════════════════╝")

        clusters = self.list_clusters()
        if not clusters:
            print("No EKS clusters found.")
            return

        table_data = []
        headers = ["Cluster Name", "Endpoint Public Access", "Public Access CIDRs"]

        for cluster in clusters:
            cluster_info = self.describe_cluster(cluster)
            table_data.append(
                [
                    cluster,
                    str(cluster_info.get("Endpoint Public Access", "Unknown")),
                    str(cluster_info.get("Public Access CIDRs", "Unknown")),
                ]
            )

        rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))
