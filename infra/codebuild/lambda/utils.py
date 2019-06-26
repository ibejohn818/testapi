import boto3
from functools import wraps
import requests
from ipaddress import ip_network, ip_address
import hmac
from hashlib import sha1
from github import Github

HOOK_SECRET_ID = "MtawsApiGithubHookSecret"
GITHUB_TOKEN = "MtawsApiGithubToken"


def get_aws_secret(id):
    try:
        sc = boto3.client("secretsmanager")

        res = sc.get_secret_value(SecretId=id)
        if res.get("SecretString"):
            return res.get("SecretString")

    except Exception as e:
        return False
    return False


def github_client():
    token = get_aws_secret(GITHUB_TOKEN)
    return Github(token)


class github_digest:
    def verify_ip(self, evt, ctx):

        ips_in = [
            ip_address(ip)
            for ip in evt["headers"]["X-Forwarded-For"].split(",")
        ]

        hook_cidrs = requests.get("https://api.github.com/meta").json()[
            "hooks"
        ]

        for cidr in hook_cidrs:
            for ip in ips_in:
                if ip in ip_network(cidr):
                    return True

        return False

    def verify_digest(self, evt, ctx):
        """Verify the request by ciphering
            using the secret key
        """
        sig_str = evt["headers"].get("X-Hub-Signature", False)

        if not sig_str:
            return False

        sig_key, sig_val = sig_str.split("=")

        secret = get_aws_secret(HOOK_SECRET_ID)

        digest = hmac.new(
            bytearray(secret, "utf-8"),
            msg=str(evt["body"]).encode("utf-8"),
            digestmod="sha1",
        )

        if str(digest.hexdigest()) == str(sig_val):
            return True

        return False

    def deny(self, *args):
        return {
            "statusCode": 400,
            "headers": {"content-type": "text/plain"},
            "body": "INVALID REQUEST",
        }

    def __call__(self, f):
        @wraps(f)
        def dec(evt, ctx):
            if self.verify_ip(evt, ctx) and self.verify_digest(evt, ctx):
                return f(evt, ctx)
            else:
                return self.deny(evt, ctx)

        return dec
