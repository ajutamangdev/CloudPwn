# Quick Start

This guide provides a streamlined workflow to get up and running with CloudPwn right after installation.

- Initialize CloudPwn
Ensure you’ve already installed and configured CloudPwn.

Verify your setup with:

```
python3 cloudpwn/main.py --help 
```

## Basic Usage
Here’s how you can start enumerating and find exploitable cloud resources:

### AWS Example Commands

Explore EC2 Instances in a Specific Region

```
python3 cloudpwn/main.py aws ec2 --region us-west-2  
```


Enumerate All AWS Resources

```
python3 cloudpwn/main.py aws --profile default  
```

This Quickstart is designed to help you take your first steps with CloudPwn while leaving room to explore advanced workflows. Let me know if you'd like further refinements!