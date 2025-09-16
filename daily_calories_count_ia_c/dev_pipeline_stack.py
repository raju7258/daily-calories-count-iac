from aws_cdk import (
    Stack,
    Stage,
    pipelines
)
from constructs import Construct
from .daily_calories_count_ia_c_stack import DailyCaloriesCountIaCStack

class DevPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.connection(
            "raju7258/daily-calories-count-iac",
            "main",
            connection_arn="arn:aws:codeconnections:us-east-1:087260250299:connection/c91a69b3-2909-465c-b312-e04db094a023"
        )

        pipeline = pipelines.CodePipeline(
            self, "DevPipeline",
            pipeline_name="CaloriesCount-Dev-Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        dev_stage = DevStage(self, "DevDeploy")
        pipeline.add_stage(dev_stage)

class DevStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        DailyCaloriesCountIaCStack(self, "CaloriesCount-Dev", env_name="dev")