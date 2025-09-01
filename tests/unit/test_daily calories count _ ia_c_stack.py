import aws_cdk as core
import aws_cdk.assertions as assertions

from daily calories count _ ia_c.daily calories count _ ia_c_stack import DailyCaloriesCountIaCStack

# example tests. To run these tests, uncomment this file along with the example
# resource in daily calories count _ ia_c/daily calories count _ ia_c_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DailyCaloriesCountIaCStack(app, "daily-calories-count---ia-c")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
