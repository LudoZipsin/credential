import sys
import errno
import argparse
import getpass
from account import Account
from urlparse import urlparse
import click


def list_handler(sub_args):

    if sub_args.service is None:
        # list all with indication of the number of account stored for each service
        service_dict = {}
        for i in Account.select():
            if i.service in service_dict:
                service_dict[i.service] += 1
            else:
                service_dict[i.service] = 1
        _list_service_printer(service_dict, ["service name", "nbs account"])
    else:
        # list only the account of the given service if the service is used
        account_dict = {}
        for i in Account.select().where(Account.service == sub_args.service):
            account_dict[i.account] = i.alias
        _list_account_printer(account_dict, ["account name", "alias"])


def _pretty_table_availability():
    import imp
    try:
        imp.find_module('prettytable')
        custom_print_available = True
    except ImportError:
        custom_print_available = False
    return custom_print_available


def _pretty_print(dictionary, field_list):
    from prettytable import PrettyTable
    table = PrettyTable([field_list[0], field_list[1]])
    for i in dictionary:
        table.add_row([i, dictionary[i]])
    print table.get_string(sortby=field_list[1], reversesort=True)


def _list_service_printer(dictionary, field_list):
    if _pretty_table_availability():
        _pretty_print(dictionary, field_list)
    else:
        for i in dictionary:
            print i, "(", dictionary[i], ")"


def _list_account_printer(dictionary, field_list):
    if _pretty_table_availability():
        _pretty_print(dictionary, field_list)
    else:
        for i in dictionary:
            print "account :", i, ", alias :", dictionary[i]


def get_handler(sub_args):
    credential = Account.select().where(Account.alias == sub_args.alias)
    get = credential.account if sub_args.selection == "account" \
        else credential.passphrase if sub_args.selection == "passphrase" \
        else credential.service
    if sub_args.prompt:
        print get
    else:
        import pyperclip
        pyperclip.copy(get)


def add_handler(sub_args):
    alias = sub_args.alias
    service = sub_args.service
    account = sub_args.account
    if alias is None:
        alias = str(click.prompt("Please type an alias to store the credential (this alias must be unique):"))
        if not _alias_valid(alias):
            select = Account.select().where(Account.alias == alias)
            service = str(select[0].service)
            account = str(select[0].account)
            sys.exit("Aborting , this alias already exist for the service " + service + " and the account " + account)
    if service is None:
        service = str(click.prompt("Please type the name of the service you want to use"))
        if not sub_args.noformat:
            if service.split("://")[0].lower() == "http":
                service = urlparse(service).netloc
            service = service.lower()
    if account is None:
        account = str(click.prompt("Please enter the account for the credential (aka login)"))
        select = Account.select().where(Account.service == service and Account.account == account)
        if len(select) == 0:
            print "The account " + account + " associated to the service " + service + " already exist"
            if not click.confirm("Do you wish to continue adding this credential ?"):
                sys.exit("Aborting")
    passphrase = getpass.getpass("Enter passphrase:")
    Account.create(service=service,
                   account=account,
                   passphrase=passphrase,
                   alias=alias)


def remove_handler(sub_args):
    credential = Account.select().where(Account.alias == sub_args.alias)
    if len(credential) == 0:
        sys.exit("There is no credential with alias " + sub_args.alias)
    else:
        if sub_args.force:
            _delete_alias(sub_args.alias)
        else:
            account = str(credential[0].account)
            service = str(credential[0].service)
            print "The credential for the account " + account + " of the service " + service + " will be removed."
            if click.confirm("Confirm credential removal:"):
                _delete_alias(sub_args.alias)
            else:
                sys.exit("Removal aborted")


def _delete_alias(alias):
    query = Account.delete().where(Account.alias == alias)
    query.execute()


def edit_handler(sub_args):
    # TODO
    pass


def _alias_valid(alias):
    select = Account.select().where(Account.alias == alias)
    return True if len(select) == 0 else False


if __name__ == "__main__":

    # parsing args
    parser = argparse.ArgumentParser(prog="credential")
    subparsers = parser.add_subparsers(help="sub commands")

    # list sub command parser
    parser_list = subparsers.add_parser("list", help="Get information on the services")
    parser_list.add_argument("-s", "--service",
                             help="List account stored for the given service",
                             type=str,
                             nargs=1)
    parser_list.set_default(func=list_handler)

    # get sub command parser
    parser_get = subparsers.add_parser("get", help="Get a stored credential")
    parser_get.add_argument("alias", nargs=1,
                            help="the alias of the account you want to gain credential of")
    parser_get.add_argument("-s", "--selection",
                            help="select which part of the credential you want. Account, passphrase or service",
                            choices=["account", "passphrase", "service"],
                            default="service",
                            nargs=1)
    parser_get.add_argument("-p", "--prompt",
                            help="Do not store the credential in the clipboard but pormpt it",
                            action="store_true",
                            default=False)
    parser_get.set_default(func=get_handler)

    # add sub command parser
    parser_add = subparsers.add_parser("add", help="Add a credential")
    parser_add.add_argument("-s", "--service",
                            help="specify the service you want to register")
    parser_add.add_argument("-a", "--account",
                            help="specify the account you want to register")
    parser_add.add_argument("-A", "--alias",
                            help="specify the alias to give to this credential")
    parser_add.add_argument("-n", "--noformat",
                            help="do not perform format on service (default to lower case and domain name)",
                            action="store_true",
                            default=False
                            )
    parser_add.set_default(func=add_handler)

    # remove sub command parser
    parser_remove = subparsers.add_parser("remove", help="Remove a credential")
    parser_remove.add_argument("alias", nargs=1,
                               help="The alias of the account you want to delete")
    parser_remove.add_argument("-f", "--force",
                               help="Will delete the credential without asking",
                               action="store_true",
                               default=False)
    parser_remove.set_default(func=remove_handler)

    # edit sub command parser
    parser_edit = subparsers.add_parser("edit", help="Edit a credential")
    # parser_edit.add_argument()
    parser_edit.set_default(func=edit_handler)

    args = parser.parse_args()

    try:
        args.func(args)
    except IOError as e:
        if e[0] == errno.EPERM:
            print >> sys.stderr, "You need root permissions to do use credential."
            sys.exit(1)
