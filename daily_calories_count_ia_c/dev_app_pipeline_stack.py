from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codebuild as codebuild,
    aws_s3 as s3,
    aws_iam as iam
)
from constructs import Construct
from .config_loader import ConfigLoader

class DevAppPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = ConfigLoader.load_config("dev")
        bucket_name = config["resources"]["s3_bucket_name"]

        # Source artifact
        source_output = codepipeline.Artifact()
        
        # Build project for Flutter
        build_project = codebuild.Project(
            self, "FlutterBuild",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {
                            "android": "29"
                        },
                        "commands": [
                            "git clone https://github.com/flutter/flutter.git -b stable",
                            "export PATH=\"$PATH:`pwd`/flutter/bin\"",
                            "flutter doctor"
                        ]
                    },
                    "build": {
                        "commands": [
                            "flutter build web"
                        ]
                    }
                },
                "artifacts": {
                    "files": ["**/*"],
                    "base-directory": "build/web"
                }
            })
        )

        # Add S3 permissions to build project
        build_project.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
                resources=[f"arn:aws:s3:::{bucket_name}/*", f"arn:aws:s3:::{bucket_name}"]
            )
        )

        # Deploy project
        deploy_project = codebuild.Project(
            self, "S3Deploy",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        "commands": [
                            f"aws s3 sync . s3://{bucket_name} --delete"
                        ]
                    }
                }
            })
        )

        deploy_project.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
                resources=[f"arn:aws:s3:::{bucket_name}/*", f"arn:aws:s3:::{bucket_name}"]
            )
        )

        # Pipeline
        pipeline = codepipeline.Pipeline(
            self, "AppPipeline",
            pipeline_name="CaloriesCount-Dev-App-Pipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        cpactions.CodeStarConnectionsSourceAction(
                            action_name="GitHub_Source",
                            owner="raju7258",
                            repo=config["github"]["app_repo"],
                            branch="dev",
                            connection_arn="arn:aws:codeconnections:us-east-1:087260250299:connection/c91a69b3-2909-465c-b312-e04db094a023",
                            output=source_output
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        cpactions.CodeBuildAction(
                            action_name="Flutter_Build",
                            project=build_project,
                            input=source_output,
                            outputs=[codepipeline.Artifact("BuildOutput")]
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Deploy",
                    actions=[
                        cpactions.CodeBuildAction(
                            action_name="S3_Deploy",
                            project=deploy_project,
                            input=codepipeline.Artifact("BuildOutput")
                        )
                    ]
                )
            ]
        )