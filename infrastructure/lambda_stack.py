from aws_cdk import (
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    aws_lambda,
    aws_logs,
    aws_sns,
    aws_sns_subscriptions,
    aws_sqs,
    core
)
from aws_cdk.core import (
    App, Duration, RemovalPolicy, SecretValue, Stack, Token
)


# You need to manually setup this 'your_secret_id' in Secrets Manager
# before deploy CDK with 3 fields: bot_id, token of the telegram_bot
# and chat_id of the telegram chat where the bot will write the messages.
SECRET_ID = 'your_secret_id'

bot_id = Token.as_string(SecretValue.secrets_manager(
    secret_id=SECRET_ID,
    json_field='bot_id'))

token = Token.as_string(SecretValue.secrets_manager(
    secret_id=SECRET_ID,
    json_field='token'))

chat_id = Token.as_string(SecretValue.secrets_manager(
    secret_id=SECRET_ID,
    json_field='chat_id'))


class LambdaStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:

        super().__init__(app, id, **kwargs)

        # ========================================
        # LAMBDA
        # ========================================
        app_code = aws_lambda.Code.asset("./src")

        lambda_fn = aws_lambda.Function(
            self,
            "Lambda",
            function_name="telegram-bot-function",
            code=app_code,
            environment={
                'TELEGRAM_BOT_ID': bot_id,
                'TELEGRAM_TOKEN': token,
                'CHAT_ID': chat_id,
                'BASE_URL': f"https://api.telegram.org/{bot_id}:{token}",
                'PYTHONPATH': './packages'
            },
            handler="handler.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            timeout=Duration.seconds(60)
        )

        aws_logs.LogGroup(
            self,
            "LambdaFunctionLog",
            log_group_name=f"/aws/lambda/{lambda_fn.function_name}",
            removal_policy=RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_WEEK
        )

        # ========================================
        # SNS
        # ========================================
        topic = aws_sns.Topic(
            self,
            "Topic",
            topic_name="telegram-bot-alarm-topic",
            display_name="telegram-bot-alarm-topic"
        )

        topic.add_subscription(
            aws_sns_subscriptions.LambdaSubscription(lambda_fn)
        )

        # ========================================
        # SQS
        # ========================================
        queue = aws_sqs.Queue(
            self,
            "Queue",
            queue_name="telegram-bot-queue"
        )

        metric = queue.metric_approximate_number_of_messages_visible(
            label="Number of messages visible",
            period=Duration.seconds(60)
        )

        # ========================================
        # CLOUDWATCH ALARM
        # ========================================
        alarm = metric.create_alarm(
            self,
            "AlarmTooManyMessages",
            alarm_name="telegram-alarm-bot-TooManyMessages",
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            evaluation_periods=1,
            threshold=1,
            treat_missing_data=cw.TreatMissingData.MISSING,
        )

        alarm.add_alarm_action(cw_actions.SnsAction(topic))
        alarm.add_ok_action(cw_actions.SnsAction(topic))
