import os


class Config:
    AWS_DEFAULT_REGION = "us-east-1"

    def create_output_dir(self, output_dir="dist/aws/"):
        """Creates the output directory if it doesn't exist and returns the path."""
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
