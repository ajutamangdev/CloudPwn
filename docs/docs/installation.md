# Installation

Follow these steps to set up and start using CloudPwn:

## Prerequisites
Before installing, ensure the following tools and dependencies are available on your system:

- Python3: 
    - Verify your Python version:
    ```
    python3 --version  
    ```

- pip (Python Package Installer):
    - Confirm pip is installed:
   ```
    pip --version  
   ```

- git:
    - Confirm Git is installed:
    ```
    git --version
    ```
- make:
    - Confirm make is installed:
        ```
        make --help
        ```
    - For installation guide
        ```
        sudo apt-get install build-essential # linux
        choco install make # windows
        brew install make # macos
        ```

## Installation

- Step 1: Clone the Repository
    - Clone the CloudPwn repository to your local machine:
    ```
    git clone https://github.com/ajutamangdev/CloudPwn.git && cd cloudpwn
    ```

- Step 2: Setup Environment and install required dependencies
    - Use Makefile to setup the Environment
    ```
    make setup
    ```
    - Activate the virtual environment    
    ```
    source venv/bin/activate  # For Linux/MacOS  
    source venv\Scripts\activate     # For Windows 
    ```

## Post-Installation Setup
- Step 1: Configure Cloud Provider CLI
    - For AWS, set up your credentials and profiles:   
    ```
    aws configure  
    ```
    - For custom AWS profile
    ```
    aws configure --profile <custom-name>
    ```
- Step 2: Verify Installation
    - Run the --help command to ensure CloudPwn is working:
    ```
    python3 cloudpwn/main.py --help  
    ```

You should see the usage guide displayed.

## Updating CloudPwn
Keep CloudPwn up to date by pulling the latest changes from the repository:

```
git pull origin main  
```

Follow the step 2 of Installation 

## Troubleshooting
If you encounter issues:
- Ensure all dependencies are installed correctly:
    ```
    pip check 
    ```
- Verify your cloud provider CLI setup (e.g., AWS credentials):
    ```
    aws sts get-caller-identity  
    ```

> For additional help, refer to the [Need Help section](http://ajutamangdev.github.io/CloudPwn/#need-help) or contact me via the social links.