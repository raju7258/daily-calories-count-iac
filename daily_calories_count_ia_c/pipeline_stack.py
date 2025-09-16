from aws_cdk import (
    Stack,
    Environment,
    pipelines
)
from constructs import Construct
from .daily_calories_count_ia_c_stack import DailyCaloriesCountIaCStack

class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(
            "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME",
            "main"
        )

        pipeline = pipelines.CodePipeline(
            self, "Pipeline",
            pipeline_name="CaloriesCountPipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        # Dev environment - auto deploy
        dev_stage = EnvironmentStage(self, "Dev", env_name="dev")
        pipeline.add_stage(dev_stage)

        # Test environment - with manual approval
        test_stage = EnvironmentStage(self, "Test", env_name="test")
        pipeline.add_stage(test_stage, 
            pre=[pipelines.ManualApprovalStep("PromoteToTest")]
        )

        # Prod environment - with manual approval
        prod_stage = EnvironmentStage(self, "Prod", env_name="prod")
        pipeline.add_stage(prod_stage,
            pre=[pipelines.ManualApprovalStep("PromoteToProd")]
        )

class EnvironmentStage(pipelines.Stage):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        DailyCaloriesCountIaCStack(self, f"CaloriesCount-{env_name}", env_name=env_name)