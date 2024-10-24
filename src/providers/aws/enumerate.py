from providers.aws.ec2 import EC2
from rich import print


def aws_enumerate_all(profile, region):
    """Performs full enumeration of AWS services and saves results to a CSV file."""
    ec2 = EC2(profile, region)

    # Get raw EC2 instance data
    ec2_instances = ec2.get_ec2_instances_raw()

    # Prepare data for CSV
    if isinstance(ec2_instances, list):
        ec2.save_ec2_to_csv(ec2_instances)


def enumerate_specific_service(service, profile, region):
    """Enumerates instances for the specified AWS service."""
    if service.lower() == "ec2":
        ec2 = EC2(profile, region)
        formatted_output = ec2.enumerate_ec2_instances()
        print(formatted_output)  # Print the formatted output
    else:
        raise ValueError(
            f"Unsupported service: {service}. Supported services are: ec2."
        )
