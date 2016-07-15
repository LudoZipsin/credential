import sys
import errno
import argparse
import getpass


def list_handler(args):
    pass


def get_handler(args):
    pass


def add_handler(args):
    pass


def remove_handler(args):
    pass


if __name__ == "__main__":

    # parsing args
    parser = argparse.ArgumentParser(prog="credential")
    subparsers = parser.add_subparsers(help="sub commands")

    # list sub command parser
    parser_list = subparsers.add_parser("list", help="Get information on the services")
    # parser_list.add_argument()
    parser_list.set_default(func=list_handler)

    # list sub command parser
    parser_get = subparsers.add_parser("get", help="Get a stored credential")
    # parser_get.add_argument()
    parser_get.set_default(func=get_handler)

    # list sub command parser
    parser_add = subparsers.add_parser("add", help="Add a credential")
    # parser_add.add_argument()
    parser_add.set_default(func=add_handler)

    # list sub command parser
    parser_remove = subparsers.add_parser("remove", help="Remove a credential")
    # parser_remove.add_argument()
    parser_remove.set_default(func=remove_handler)

    args = parser.parse_args()

    try:
        args.func(args)
    except IOError as e:
        if e[0] == errno.EPERM:
            print >> sys.stderr, "You need root permissions to do use credential."
            sys.exit(1)
