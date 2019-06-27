from utils import github_digest, github_client
import boto3
import json


@github_digest()
def handler(evt, ctx):

    cbc = boto3.client("codebuild")

    from pprint import pprint

    headers = evt.get("headers", {})
    body = json.loads(evt.get("body", {}))

    if headers.get("X-GitHub-Event") in ("pull_request"):

        cbc = boto3.client("codebuild")
        commit_id = body["pull_request"]["head"]["sha"]
        cbc.start_build(
            projectName="MtawsApi",
            sourceVersion=body["pull_request"]["head"]["ref"],
            environmentVariablesOverride=[
                {"name": "commit", "value": commit_id}
            ],
        )

        # mt = github_client().get_organization("mediatemple")
        mt = github_client().get_user("ibejohn818")
        repo = mt.get_repo(body["repository"]["name"])
        commit = repo.get_commit(commit_id)

        commit.create_status(
            "pending", context="Codebuild", description="Build Started"
        )

    return {
        "statusCode": 200,
        "headers": {"content-type": "text/plain"},
        "body": "HOLA",
    }
