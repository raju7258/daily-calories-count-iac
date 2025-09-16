from aws_cdk import (
    Stack,
    aws_s3 as s3,
    CfnOutput,
    RemovalPolicy,
    Duration,
    Tags
)
from constructs import Construct
from .config_loader import ConfigLoader

class DailyCaloriesCountIaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_name: str = "dev", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Load configuration
        config = ConfigLoader.load_config(env_name)
        
        # Environment-specific configurations
        removal_policy = RemovalPolicy.RETAIN if config["retention_policy"] == "retain" else RemovalPolicy.DESTROY
        auto_delete = config["retention_policy"] == "destroy"

        web_bucket = s3.Bucket(
            self,
            "WebBucket",
            bucket_name=config["resources"]["s3_bucket_name"],
            website_index_document="index.html",
            website_error_document="index.html",
            removal_policy=removal_policy,
            auto_delete_objects=auto_delete,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD],
                    allowed_origins=config["cors"]["allowed_origins"],
                    allowed_headers=["*"],
                    max_age=Duration.hours(1).to_seconds()
                )
            ],
        )
        # Apply tags
        for key, value in config["tags"].items():
            Tags.of(self).add(key, value)
            
        CfnOutput(self, f"BucketName-{env_name}", value=web_bucket.bucket_name)
        CfnOutput(self, f"WebsiteURL-{env_name}", value=web_bucket.bucket_website_url)

