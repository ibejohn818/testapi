from utils import github_client
import boto3
import json


def extract_commit(vars):
    for v in vars:
        if v["name"] == "commit":
            return v["value"]

def build_link(build_id):
    id = build_id.split('/')[1]
    link = "https://us-west-2.console.aws.amazon.com/codesuite/codebuild/projects/CustomerTasks/build/{}/log?region=us-west-2".format(id) # noqa
    return link


def handler(evt, ctx):

    commit = extract_commit(
        evt.get("detail")["additional-information"]["environment"][
            "environment-variables"
        ]
    )

    if commit is None:
        return

    cb_link = build_link(evt['detail']['build-id'])
    status = evt['detail']['build-status']
    # mt = github_client().get_organization("mediatemple")
    mt = github_client().get_user("ibejohn818")
    # repo = mt.get_repo("mt_aws_api")
    repo = mt.get_repo("testapi")
    commit = repo.get_commit(commit)

    status_labels = {
        'SUCCEEDED': 'success',
        'FAILED': 'failure'
    }

    gh_status = status_labels.get(status, 'error')

    commit.create_status(
        gh_status,
        context="Codebuild",
        description="Build {}".format(status.lower()),
        target_url=cb_link
    )

    return True
