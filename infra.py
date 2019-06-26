#!/usr/bin/env python

import nimbi
from nimbi.aws import (
    AWSCred,
    s3,
    topic,
    vpc,
    iam,
    logs,
    eip,
    awslambda,
    rds,
    ec2,
    elb_v2,
    asg,
    alarms,
    cloudfront,
    codedeploy,
    apigateway,
    route53,
    elasticache,
    sqs,
    dynamodb)

from nimbi.aws.mt import (MTImage, find_ansible_basedir,
                          GenerateHostKeysPlugin)
from nimbi.aws.mt import user_data as mtud

from awacs.aws import Action, Allow, Statement  # noqa
import awacs.s3

import yaml
from inflection import camelize, underscore
import json
import sys
import os

APIGW_STAGE = "api"

def get_swagger(swagger_func):
    """
    """
    SWAG = 'infra/swagger.json'

    swag_handle = open(SWAG, "r")
    swagger = swag_handle.read()

    return swagger % (
        swagger_func.output_function_arn()
    )



def rest_funcs(infra, stacks):
    """
    """
    # create accounts queue

    ob_sqs = stacks['sqs'].add_queue(sqs.SQSQueue("OnboardAccounts"))
    ob_sqs.visibility_timeout = 360

    iam_stack = stacks['iam']

    lambda_role = iam_stack.add_role(iam.LambdaRole("SwaggerFunc"))
    lambda_role.add_policy(iam.CloudWatchFullAccess())
    lambda_role.add_policy(iam.CloudWatchLogs())
    lambda_role.add_policy(iam.DynamoDBTables(stacks['dynamo'].find_table('accounts')))
    lambda_role.add_policy(iam.SQSFullAccess())

    # lambda_role.add_policy(iam.FullAccessS3Bucket([
        # buckets['code'],
    # ]))

    env = {
        'SWAGG_API_KEY':123456,
        'SQS_ONBOARD_ACCOUNTS': "{{ resolve('%s') }}" % (ob_sqs.output_queue_url()),
        'ACCOUNTS_TBL': "{{ resolve('%s') }}" % (stacks['dynamo'].find_table('accounts').output_table_name())
    }

    swagger_func = awslambda.UnmanagedLambdaStack(
                                                "MtawsSwagger",
                                                lambda_role,
                                                'python3.6',
                                                30,
                                                '256',
                                                env)

    swagger_func.handler = 'api_handler.handler'
    swagger_func.add_permission(
        awslambda.Permission('apigw', 'lambda:*', 'apigateway.amazonaws.com'))  # noqa

    stacks['swagger_func'] = swagger_func

    # keep lambda warm
    swagger_warm = awslambda.LambdaScheduleStack(
        'SnugglySched',
        schedule="cron(*/5 * * * ? *)",
        lambda_stack=swagger_func
    )

    stacks['swagger_warm'] = swagger_warm

    # sqs handler func

    sqs_func = awslambda.UnmanagedLambdaStack(
                        "MtawsSqs",
                        lambda_role,
                        'python3.6',
                        60,
                        '256',
                        env)

    sqs_func.handler = "sqs_handler.handler"

    sqs_func.add_event_source(ob_sqs)

    stacks['sqs_func'] = sqs_func

def api_gw(infra, stacks):
    """
    """
    iam_stack = stacks['iam']

    api_role = iam_stack.add_role(iam.APIGatewayRole("SwaggerApiGw"))
    api_role.add_policy(iam.APIGatewayCloudWatchLogs())
    api_role.add_policy(iam.CloudWatchFullAccess())
    api_role.add_policy(iam.CustomPolicy(
        "ApiGW",
        statements=[Statement(
            Action=[
                awacs.aws.Action('apigateway', '*')
            ],
            Resource=['*', ],
            Effect=Allow
        )]
    ))
    api_role.add_policy(iam.CustomPolicy(
        "Lambda",
        statements=[Statement(
            Action=[
                awacs.aws.Action('lambda', '*')
            ],
            Resource=['*', ],
            Effect=Allow
        )]
    ))

    swagger_json = get_swagger(stacks['swagger_func'])
    # print("SW", swagger_json)
    api_gw = apigateway.SwaggerAPIStack("MtawsApi", swagger_json, api_role)
    api_gw.stage_name = APIGW_STAGE
    api_gw.add_perm_func(stacks['swagger_func'])

    stacks['swagger_apigw'] = api_gw

    # custom domain
    # api_domain = apigateway.CustomDomainStack(

	# dom,
	# api_gw,
	# base_path=APIGW_STAGE,
	# api_stage=APIGW_STAGE)

    # api_domain.set_regional_cert_arn(ACM_WEST2)

def ddb(infra, stacks):
    """
    """
    ddb_stack = dynamodb.DynamoDBStack()

    acc_tbl = ddb_stack.add_table(dynamodb.DynamoDBTable('accounts'))
    acc_tbl.table_data = {
        'table_name': 'accounts',
        'attribute_definitions': [
            {
                'name': 'id',
                'type': 'S'
            },
        ],
        'key_schema': [
            {
                'name': 'id',
                'type': 'HASH'
            },
        ],
        'provisioned_throughput': [5, 5]
    }
    stacks['dynamo'] = ddb_stack

def s3_buckets(infra, stacks, buckets):
    """
    """
    buckets['code'] = stacks['s3'].add_bucket(s3.LambdaBucket("ApiCode"))


def deploy(infra, prefix):
    """
    """
    sub = nimbi.Infra()
    sub.set_prefix(prefix)
    infra.import_infra(sub)

    stacks = {
        'vpc': vpc.VPCStack(),
        'iam': iam.IAMStack(),
        's3': s3.S3Stack(),
        'sqs': sqs.SQSStack()
    }

    roles = {}
    buckets = {}

    s3_buckets(sub, stacks, buckets)
    ddb(sub, stacks)
    rest_funcs(sub, stacks)
    api_gw(sub, stacks)

    for k, stack in stacks.items():
        sub.add_stack(stack)

    return sub, stacks

def import_ci(infra):
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, './infra/codebuild')))
    from infra_ci import deploy_ci
    deploy_ci(infra)

infra = nimbi.Infra('MtApi')
infra.add_cred(AWSCred(region='us-west-2'))

dev_infra, dev_stacks = deploy(infra, 'Dev')
import_ci(infra)
