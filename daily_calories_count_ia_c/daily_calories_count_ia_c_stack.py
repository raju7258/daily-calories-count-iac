from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cognito as cognito,
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
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
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

        # Cognito User Pool
        user_pool = cognito.UserPool(
            self,
            "UserPool",
            user_pool_name=f"nourisheye-user-pool-{env_name}",
            sign_in_aliases=cognito.SignInAliases(email=True),
            self_sign_up_enabled=True,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                given_name=cognito.StandardAttribute(required=True, mutable=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=removal_policy
        )

        # User Pool Client
        user_pool_client = cognito.UserPoolClient(
            self,
            "UserPoolClient",
            user_pool=user_pool,
            user_pool_client_name=f"nourisheye-app-client-{env_name}",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_srp=True,
                user_password=True
            )
        )

        # Apply tags
        for key, value in config["tags"].items():
            Tags.of(self).add(key, value)
            
        CfnOutput(self, f"BucketName-{env_name}", value=web_bucket.bucket_name)
        CfnOutput(self, f"WebsiteURL-{env_name}", value=web_bucket.bucket_website_url)
        CfnOutput(self, f"UserPoolId-{env_name}", value=user_pool.user_pool_id)
        CfnOutput(self, f"UserPoolClientId-{env_name}", value=user_pool_client.user_pool_client_id)

