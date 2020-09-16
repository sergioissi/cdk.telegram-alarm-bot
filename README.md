# cdk.telegram-alarm-bot
Deploy infrastructure with AWS CDK

Created with Aws CDK, this lambda is triggered by a CloudWatch Alarm that checks the number of messages
visibile in a SQS queue. If the alarm change state, the lambda will send an http request to the telegram
bot and then the bot will write a message like this in your telegram chat:

"<i>Monitoring status for resource: telegram-bot-queue. New State is: ALARM</i>"

Please take a look at <a href="https://docs.aws.amazon.com/lambda/latest/dg/limits.html">Lambda limits</a>

What you have to do before deploy the infrastructure is to create a telegram bot with 'BotFather' and
save the bot_id, token and chat_id into a secret in AWS Secrets Manager.

## Setup

### Installing the CDK CLI

```sh
$ npm install -g aws-cdk
$ cdk --version
```

### Create your python virtual env

```sh
$ python -m venv .env
$ source .env/bin/activate
$ make requirements
```

### Bootstrapping your AWS Environment
Before you can use the AWS CDK you must bootstrap your AWS environment to create the infrastructure that the AWS CDK CLI needs to deploy your AWS CDK app. Currently the bootstrap command creates only an Amazon S3 bucket.

```sh
$ cdk bootstrap
```

You incur any charges for what the AWS CDK stores in the bucket. Because the AWS CDK does not remove any objects from the bucket, the bucket can accumulate objects as you use the AWS CDK. You can get rid of the bucket by deleting the CDKToolkit stack from your account.

## Commands to manage and create/update infrastructure:

Synthesizes and prints the CloudFormation template for this stack in the 'cdk.out' folder.
```sh
$ cdk synth
```

Compares the specified stack with the deployed stack or a local template file, and returns with status 1 if any difference is found.
```sh
$ cdk diff
```

Deploys (create and update) the stack(s) named STACKS into your AWS account.
```sh
$ cdk deploy
```

Destroy the stack(s) named STACKS.
```sh
$ cdk destroy
```