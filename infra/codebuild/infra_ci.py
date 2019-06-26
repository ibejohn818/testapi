import nimbi
from nimbi.aws import (
    AWSCred,
    s3,
    iam,
    awslambda,
    codebuild,
    events,
    apigateway,
)

from awacs.aws import Action, Allow, Statement  # noqa
import awacs.s3

import yaml
from inflection import camelize, underscore
import json
import sys
import os

def get_swagger(f1, f2):
    with open("infra/codebuild//Swagger.json", "r") as swag:
        swag_json = swag.read() % (f1.output_function_arn())
        return swag_json

def codebuild_stacks(sub, stacks):

    role = stacks["iam"].add_role(iam.CodeBuildRole("MtAwsApi"))
    role.add_policy(iam.CodeBuildBase())
    role.add_policy(
        iam.CustomPolicy(
            "custom",
            statements=[
                Statement(
                    Action=[
                        awacs.aws.Action("ssm", "GetParameter"),
                        awacs.aws.Action("kms", "Decrypt"),
                    ],
                    Resource=["*"],
                    Effect=Allow,
                )
            ],
        )
    )
    env = codebuild.Environment("aws/codebuild/python:3.7.1")
    repo = codebuild.GithubEnterpriseSource(
        "https://github.com/mediatemple/mt_aws_api.git"
    )

    project = codebuild.BuildProject("CustomerTasks", role, env, repo)
    build_stack = codebuild.CodeBuildStack()

    build_stack.add_build(project)

    stacks["codebuild"] = build_stack

    # cloudwatch event
    event = events.EventsStack()
    event.variant = "CIEvents"

    pattern = events.Pattern()
    pattern.add_source(project)
    pattern.add_detail({"build-status": ["SUCCEEDED", "FAILED"]})

    rule = event.add_rule(events.Rule("CI"))
    rule.add_event_pattern(pattern)
    target = events.Target("CiEvent", stacks["event_lambda"])
    rule.add_target(target)

    stacks["codebuild_event"] = event

def codebuild_handlers(sub, stacks, buckets):

    iam_stack = stacks["iam"]

    lambda_role = iam_stack.add_role(iam.LambdaRole("GithubWebhook"))
    lambda_role.add_policy(iam.CloudWatchFullAccess())
    lambda_role.add_policy(iam.CloudWatchLogs())
    lambda_role.add_policy(iam.TriggerBuild())
    lambda_role.add_policy(iam.GetSecrets())
    lambda_role.add_policy(
        iam.CustomPolicy(
            "custom",
            statements=[
                Statement(
                    Action=[
                        awacs.aws.Action("ssm", "GetParameter"),
                        awacs.aws.Action("kms", "Decrypt"),
                    ],
                    Resource=["*"],
                    Effect=Allow,
                )
            ],
        )
    )

    env = {}

    github_webhook = awslambda.UnmanagedLambdaStack(
        "CIWebhook", lambda_role, "python3.6", 180, "256", env
    )
    github_webhook.handler = "webhook.handler"
    github_webhook.environment = env
    stacks["webhook_lambda"] = github_webhook


    build_event = awslambda.UnmanagedLambdaStack(
        "CIBuildEvent", lambda_role, "python3.6", 180, "256", env
    )
    build_event.handler = "build_event.handler"
    build_event.environment = env
    build_event.add_permission(
        awslambda.Permission(
            "events", "lambda:InvokeFunction", "events.amazonaws.com"
        )
    )
    stacks["event_lambda"] = build_event

def codebuild_api_gw(sub, stacks):

    # Swagger API Gateway
    api_role = stacks['iam'].add_role(iam.APIGatewayRole("MtAwsGithubWebhook"))
    api_role.add_policy(iam.APIGatewayCloudWatchLogs())
    api_role.add_policy(iam.CloudWatchFullAccess())
    api_role.add_policy(iam.InvokeFunction())

    swag_json = get_swagger(stacks['event_lambda'], stacks['webhook_lambda'])

    webook_api = apigateway.SwaggerAPIStack("AwsApiGithook", swag_json, api_role)
    webook_api.set_endpoint_type("REGIONAL")
    webook_api.add_perm_func(stacks["webhook_lambda"])

    stacks["webhook_api"] = webook_api

def s3_buckets(sub, stacks, buckets):
    """
    """
    buckets['code'] = stacks['s3'].add_bucket(s3.LambdaBucket('MtAwsCi'))

def deploy_ci(infra):
    """ Deploy the ci and github webhook
    """

    stacks = {
        's3': s3.S3Stack('CI'),
        'iam': iam.IAMStack('CI')
    }

    buckets = {}

    s3_buckets(infra, stacks, buckets)
    codebuild_handlers(infra, stacks, buckets)
    codebuild_stacks(infra, stacks)
    codebuild_api_gw(infra, stacks)

    for k, stack in stacks.items():
        infra.add_stack(stack)

    return stacks
