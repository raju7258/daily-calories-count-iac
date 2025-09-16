from aws_cdk import (
    Stack,
    pipelines
)
from constructs import Construct
from ..daily_calories_count_ia_c.daily_calories_count_ia_c_stack import DailyCaloriesCountIaCStack

class TestPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(
            "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME",
            "test"
        )

        pipeline = pipelines.CodePipeline(
            self, "TestPipeline",
            pipeline_name="CaloriesCount-Test-Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        test_stage = TestStage(self, "TestDeploy")
        pipeline.add_stage(test_stage)

class TestStage(pipelines.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        DailyCaloriesCountIaCStack(self, "CaloriesCount-Test", env_name="test")