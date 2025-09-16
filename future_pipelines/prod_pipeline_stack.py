from aws_cdk import (
    Stack,
    pipelines
)
from constructs import Construct
from ..daily_calories_count_ia_c.daily_calories_count_ia_c_stack import DailyCaloriesCountIaCStack

class ProdPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(
            "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME",
            "main"
        )

        pipeline = pipelines.CodePipeline(
            self, "ProdPipeline",
            pipeline_name="CaloriesCount-Prod-Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        prod_stage = ProdStage(self, "ProdDeploy")
        pipeline.add_stage(prod_stage,
            pre=[pipelines.ManualApprovalStep("DeployToProd")]
        )

class ProdStage(pipelines.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        DailyCaloriesCountIaCStack(self, "CaloriesCount-Prod", env_name="prod")