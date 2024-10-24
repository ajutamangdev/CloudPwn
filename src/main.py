import time
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from providers.aws.enumerate import aws_enumerate_all, enumerate_specific_service


def main(
    provider: str = typer.Argument(
        ..., help="Select a cloud provider (aws, azure, gcp)", case_sensitive=False
    ),
    profile: str = typer.Option(None, "--profile", help="AWS profile name"),
    service: str = typer.Argument(
        None,
        help="Services type (e.g., ec2, s3, rds, eks)",
        case_sensitive=False,
        show_default=False,
    ),
    region: str = typer.Option("us-east-1", "--region", help="AWS region to use"),
):
    """
    CloudPwn: A toolkit for cloud platform enumeration and exploitation.

    Example usage:
    - python src/main.py aws --profile custom-profile
    - python src/main.py aws --profile custom-profile ec2 --region us-east-1
    """

    provider = provider.lower()

    if provider == "aws":
        if profile is None:
            print(
                "[red]Error:[/red] AWS profile is required. Use '--profile' option to specify the profile."
            )
            raise typer.Abort()

        confirm = typer.confirm("Are you sure you want to perform AWS enumerations?")
        if not confirm:
            print("Exiting...")
            raise typer.Exit()

        print(
            f"Performing AWS enumerations with profile: {profile} in region: {region}"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Processing...", total=None)
            time.sleep(5)

            if service is None:
                aws_enumerate_all(profile, region)
                progress.update(task, description="Processing complete.")
                print(
                    "[green]Full AWS scan complete. Results saved to database.[/green]"
                )
            else:
                result = enumerate_specific_service(service, profile, region)

                if result:
                    print(f"\n[green]Enumerated {service.upper()} results:[/green]")
                    print(result)

    print("Done!")


if __name__ == "__main__":
    typer.run(main)
