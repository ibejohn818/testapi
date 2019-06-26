""" Emulate SQS Lambda handler
"""
from argparse import ArgumentParser
import subprocess
import shlex
import sys
import os
import time
import logging
from mtaws.data import sqs
from mtaws import sqs_handler

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class ContextMock:
    pass

def lowerf(s):
    """ lowercase first letter
    """
    return s[:1].lower() + s[1:]

def make_sqs_payload(msg):
    """
    """
    payload = {
        'Records': [parse_msg(msg)]
    }
    return payload, ContextMock()

def parse_msg(msg):
    """
    """
    out = {
        'messageId': msg.message_id,
        'body': msg.body,
        'receiptHandle': msg.receipt_handle,
        'md5OfBody': msg.md5_of_body,
        'md5OfMessageAttributes': msg.md5_of_message_attributes,
        'messageAttributes': {},
        'attributes': {},

    }

    for k, v in msg.message_attributes.items():
        new = {k: {}}
        for kk, vv in v.items():
            new[k][lowerf(kk)] = vv
        out['messageAttributes'].update(new)

    for k, v in msg.attributes.items():
        out['attributes'].update({lowerf(k): v})

    return out

def cmdbg(cmd):
    """ Run a command and send to bg
    """
    subprocess.Popen(shlex.split("nohup {} {}".format(
        sys.executable,
        cmd)), preexec_fn=os.setpgrp)


def start_listener(**kw):
    """ start an sqs repl and send messages to
        the sqs_handler formatted in the same
        way cloudwatch events does
    """
    queue = sqs.Sqs.factory(kw.get("queue")).resource()
    while True:
        msgs = queue.receive_messages(WaitTimeSeconds=20,
                                      MessageAttributeNames=['All'],
                                      AttributeNames=['All'])
        if len(msgs) > 0:
            for k, msg in enumerate(msgs):
                logger.info("({})Processing..".format(kw.get('queue')))
                evt, ctx = make_sqs_payload(msg)
                sqs_handler.handler(evt, ctx)
                logger.info("Proccesed ({}): {} ".format(
                                            kw.get("queue"),
                                            msg.message_id))

def runner(**kw):
    """
    """
    logger.info("Initializing...")
    # time.sleep(20)
    for q in sqs.QueueUrls:
        cmdbg("/app/local_sqs_runner.py start-listener {}".format(q.name))

    while True:
        logger.info("Ping...")
        time.sleep(120)

def init():
    """
    """
    parser = ArgumentParser(description="Tools to run sqs handlers locally")

    sub = parser.add_subparsers()

    sl = sub.add_parser("start-listener", description=("Listen for a queue in the background "
                                                       "and send message to sqs_handler.py"))
    sl.add_argument("queue", type=str, help="The queue name the Sqs.factory will load")
    sl.set_defaults(cmd=start_listener)

    run = sub.add_parser("runner", description="Run the queue listeners")
    run.set_defaults(cmd=runner)

    return parser


if __name__ == "__main__":

    try:
        parser = init()
        args = parser.parse_args()

        if hasattr(args, "cmd"):
            cmd = getattr(args, "cmd")
            kw = vars(args)
            cmd(**kw)
        else:
            parser.print_help()
    except Exception as e:
        str(e)
