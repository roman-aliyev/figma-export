from inspect import signature
from argparse import ArgumentParser
from .exporters import exporters_by_format


def init_argument_parser():
    parser = ArgumentParser(prog="figma_export")
    subparsers = parser.add_subparsers(dest='export_format', help='export format')
    subparsers.required = True
    for command, exporter_type in exporters_by_format.items():
        subparser = subparsers.add_parser(
            command,
            description=exporter_type.__doc__
        )
        subparser.add_argument(
            "document_id",
            help="can be parsed from any Figma document url: https://www.figma.com/file/DOCUMENT_ID/..."
        )
        for k, v in signature(exporter_type.__call__).parameters.items():
            if k == "self":
                continue
            arg_name = v.name
            arg_type = v.annotation
            arg_default = getattr(arg_type, "default", None)
            subparser.add_argument(
                "-" + arg_name,
                type=arg_type,
                default=arg_default,
                required=arg_default is None,
                help=getattr(arg_type, "__doc__", None)
            )
    return parser


def main():
    argument_parser = init_argument_parser()
    args = argument_parser.parse_args()
    document_id = args.document_id
    del args.document_id
    export_format = args.export_format
    exporter_type = exporters_by_format.get(args.export_format)
    del args.export_format
    exporter_type(export_format, document_id)(**vars(args))
    print("Done")


if __name__ == '__main__':
    main()
