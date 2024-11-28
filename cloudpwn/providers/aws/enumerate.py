from rich import print as rich_print
from cloudpwn.providers.aws.ec2 import EC2
from cloudpwn.providers.aws.secrets_manager import Secrets
from cloudpwn.providers.aws.rds import RDS
from cloudpwn.providers.aws.s3 import S3
from cloudpwn.providers.aws.eks import EKS
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
        enumerate_specific_service("secrets", profile, region)
        enumerate_specific_service("rds", profile, region)


def enumerate_specific_service(service, profile, region):
    """
    Enumerates instances for the specified AWS service.
    """
    service = service.lower()

    service_handlers = {
        "ec2": lambda: enumerate_ec2(profile, region),
        "secrets": lambda: enumerate_secrets(profile, region),
        "rds": lambda: enumerate_rds(profile, region),
        "s3": lambda: S3(profile, region).enumerate(),
        "eks": lambda: EKS(profile, region).enumerate(),
    }

    if service in service_handlers:
        service_handlers[service]()
    else:
        rich_print(f"[bold red]Unsupported service: {service}[/bold red]")


def enumerate_ec2(profile, region):
    """Handles EC2 enumeration."""
    ec2 = EC2(profile, region)

    rich_print(ec2.enumerate_ec2_instances())
    rich_print(ec2.enumerate_volumes())
    rich_print(ec2.enumerate_snapshots())
    rich_print(ec2.enumerate_elastic_ip())
    rich_print(ec2.enumerate_custom_amis())
    rich_print(ec2.enumerate_ssm_agent_status())
    rich_print(ec2.enumerate_security_groups())


def enumerate_secrets(profile, region):
    """Handles Secrets Manager enumeration."""
    secrets = Secrets(profile, region)
    rich_print(secrets.display_secrets())


def enumerate_rds(profile, region):
    """Handles RDS enumeration."""
    rds = RDS(profile, region)
    rich_print(rds.enumerate_rds_instances())
    rich_print(rds.enumerate_rds_clusters())
    rich_print(rds.enumerate_rds_snapshots())


def enumerate_s3(profile, region):
    """Handles S3 enumeration."""
    s3 = S3(profile, region)
    rich_print(s3.enumerate())


def enumerate_eks(profile, region):
    """Handles EKS enumeration."""
    eks = EKS(profile, region)
    rich_print(eks.enumerate())
