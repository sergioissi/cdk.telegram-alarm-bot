import os
from aws_cdk.core import App, Environment
from infrastructure.lambda_stack import LambdaStack


env = Environment(
    account=os.environ["CDK_DEPLOY_ACCOUNT"],
    region=os.environ["CDK_DEPLOY_REGION"])

app = App()

LambdaStack(app, "telegram-alarm-bot", env=env)

app.synth()
