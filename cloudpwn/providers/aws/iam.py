import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate
from rich import print as rich_print


class IAM:
    def __init__(self, profile, region):
        """
        Initialize the IAM client with the specified profile and region.
        """
        self.profile = profile
        self.region = region

        try:
            session = boto3.Session(profile_name=self.profile, region_name=self.region)
            self.iam_client = session.client("iam")
            self.sts_client = session.client(
                "sts"
            )  # Add STS client for get_caller_identity
        except Exception as e:
            rich_print(f"[bold red]Error initializing IAM client: {e}[/bold red]")

    def get_caller_identity(self):
        """
        Fetch and display the current IAM user's identity, account, and ARN.
        """
        try:
            response = self.sts_client.get_caller_identity()
            user_id = response.get("UserId")
            account = response.get("Account")
            arn = response.get("Arn")

            return user_id, account, arn
        except ClientError as e:
            rich_print(f"[bold red]Error fetching caller identity: {e}[/bold red]")
            return None, None, None

    def list_users(self):
        """
        List all IAM users in the account with pagination.
        Returns:
            List of IAM users with their usernames and ARNs.
        """
        users = []
        try:
            paginator = self.iam_client.get_paginator("list_users")
            for page in paginator.paginate():
                users.extend(page["Users"])
            return users
        except ClientError as e:
            rich_print(f"[bold red]Error listing users: {e}[/bold red]")
            return []

    def list_groups(self):
        """
        List all IAM groups in the account with pagination.
        Returns:
            List of IAM groups with their names and ARNs.
        """
        groups = []
        try:
            paginator = self.iam_client.get_paginator("list_groups")
            for page in paginator.paginate():
                groups.extend(page["Groups"])
            return groups
        except ClientError as e:
            rich_print(f"[bold red]Error listing groups: {e}[/bold red]")
            return []

    def list_roles(self):
        """
        List all IAM roles in the account with pagination.
        Returns:
            List of IAM roles with their names and ARNs.
        """
        roles = []
        try:
            paginator = self.iam_client.get_paginator("list_roles")
            for page in paginator.paginate():
                roles.extend(page["Roles"])
            return roles
        except ClientError as e:
            rich_print(f"[bold red]Error listing roles: {e}[/bold red]")
            return []

    def list_policies(self):
        """
        List all IAM policies in the account with pagination.
        Returns:
            List of IAM policies with their names and ARNs.
        """
        policies = []
        try:
            paginator = self.iam_client.get_paginator("list_policies")
            for page in paginator.paginate(Scope="Local"):
                policies.extend(page["Policies"])
            return policies
        except ClientError as e:
            rich_print(f"[bold red]Error listing policies: {e}[/bold red]")
            return []

    def list_attached_user_policies(self, username):
        """
        List policies attached to a specific IAM user.
        """
        try:
            paginator = self.iam_client.get_paginator("list_attached_user_policies")
            policies = []
            for page in paginator.paginate(UserName=username):
                policies.extend(page["AttachedPolicies"])
            return policies
        except ClientError as e:
            rich_print(
                f"[bold red]Error listing attached policies for user {username}: {e}[/bold red]"
            )
            return []

    def enumerate(self):
        """
        Enumerate IAM resources: users, groups, roles, policies, and simulate user permissions.
        """
        # Get current IAM identity details
        user_id, account, arn = self.get_caller_identity()
        if user_id and account and arn:
            print("\n╔═════════════════════════════════════╗")
            print("║        Current IAM Identity          ║")
            print("╚═════════════════════════════════════╝")
            print(f"UserId: {user_id}")
            print(f"Account: {account}")
            print(f"ARN: {arn}")

        # List IAM Users
        users = self.list_users()
        if not users:
            rich_print("[bold yellow]No users found in the account.[/bold yellow]")
        else:
            print("\nIAM Users:")
            table_data = [[user["UserName"], user["Arn"]] for user in users]
            headers = ["Username", "ARN"]
            rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # List IAM Groups
        groups = self.list_groups()
        if not groups:
            rich_print("[bold yellow]No groups found in the account.[/bold yellow]")
        else:
            print("\nIAM Groups:")
            table_data = [[group["GroupName"], group["Arn"]] for group in groups]
            headers = ["Group Name", "ARN"]
            rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # List IAM Roles
        roles = self.list_roles()
        if not roles:
            rich_print("[bold yellow]No roles found in the account.[/bold yellow]")
        else:
            print("\nIAM Roles:")
            table_data = [[role["RoleName"], role["Arn"]] for role in roles]
            headers = ["Role Name", "ARN"]
            rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # List IAM Policies
        policies = self.list_policies()
        if not policies:
            rich_print("[bold yellow]No policies found in the account.[/bold yellow]")
        else:
            print("\nIAM Policies:")
            table_data = [[policy["PolicyName"], policy["Arn"]] for policy in policies]
            headers = ["Policy Name", "ARN"]
            rich_print(tabulate(table_data, headers=headers, tablefmt="grid"))
