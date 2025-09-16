#!/usr/bin/env python3
import os
import aws_cdk as cdk
from daily_calories_count_ia_c.dev_app_pipeline_stack import DevAppPipelineStack

app = cdk.App()

# Dev App Pipeline
DevAppPipelineStack(app, "CaloriesCount-Dev-App-Pipeline",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION")
    )
)

app.synth()