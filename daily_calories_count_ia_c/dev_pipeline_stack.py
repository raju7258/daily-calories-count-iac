from aws_cdk import (
    Stack,
    pipelines
)
from constructs import Construct
from .daily_calories_count_ia_c_stack import DailyCaloriesCountIaCStack

class DevPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(
            "raju7258/daily-calories-count-iac",
            "dev"  # Dev branch
        )

        pipeline = pipelines.CodePipeline(
            self, "DevPipeline",
            pipeline_name="CaloriesCount-Dev-Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        dev_stage = DevStage(self, "DevDeploy")
        pipeline.add_stage(dev_stage)

class DevStage(pipelines.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        DailyCaloriesCountIaCStack(self, "CaloriesCount-Dev", env_name="dev")