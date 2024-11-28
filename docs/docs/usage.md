# Usage

The primary script for CloudPwn is main.py. You can use the --help flag to view all available options and commands:

```
python3 cloudpwn/main.py --help  
```

Example:

```
python3 cloudpwn/main.py aws --profile custom-profile  # perform full enumeration
python3 cloudpwn/main.py aws --profile custom-profile ec2 --region us-east-1 
```

## Command Structure


```
Usage: main.py [OPTIONS] PROVIDER [SERVICE]  
```

Arguments
```
Argument	Description	Required	Default
PROVIDER	Select a cloud provider (aws, azure, gcp).
SERVICE	    Specify a service type (e.g., ec2, s3, rds, eks).
```

Options
```
Option	Description	Default
--profile TEXT	Specify the AWS profile name to use.	None
--region TEXT	Specify the AWS region to target.	us-east-1
--help	Display the help message and exit.	—
```

## Sample

- Enumerate AWS Resources with a Custom Profile

    ```
    python3 cloudpwn/main.py aws --profile custom-profile  
    ```

- Target Specific AWS Service
    - Enumerate all EC2 instances in the us-west-2 region:

    ```
    python3 cloudpwn/main.py aws --profile custom-profile ec2 --region us-west-2  
    ```

    - Enumerate all secrets from secrets manager in the ap-south-1 region

    ```
    python3 cloudpwn/main.py aws --profile custom-profile secrets --region ap-south-1
    ```


# Supported Cloud Providers
- AWS
- Azure
- GCP

# Supported AWS Services
- ec2 : Elastic Compute Cloud
- secrets : Secrets Manager
- rds : Relational Database Service
- iam : Identity and Access Management
- route53 : Route 53
- eks : Elastic Kubernetes Service
- Coming soon
