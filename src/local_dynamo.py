from argparse import ArgumentParser
import logging
from mtaws.data import dynamo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_tables(**kw):

    print("Creating accounts table...")
    dynamo.Account.create_table()


def init():

    parser = ArgumentParser(description='Local dynamo table management')

    sub = parser.add_subparsers()

    c = sub.add_parser("create", description='Create local dev tables')
    c.set_defaults(cmd=create_tables)


    return parser


if __name__ == '__main__':

    try:
        parser = init()
        args = parser.parse_args()

        if hasattr(args, "cmd"):
            cmd = getattr(args, "cmd")
            cmd(**vars(args))
        else:
            parser.print_help()

    except Exception as e:
        print("ERROR: ", str(e))
