#!/usr/bin/env python3
import os
import aws_cdk as cdk
from daily_calories_count_ia_c.dev_pipeline_stack import DevPipelineStack

app = cdk.App()

# Dev Pipeline
DevPipelineStack(app, "CaloriesCount-Dev-Pipeline",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION")
    )
)

app.synth()
