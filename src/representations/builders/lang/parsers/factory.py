# from representations.parsers.spacy_depparser import SpacyParser
from representations.builders.lang.parsers.stanza_depparser import StanzaParser


parsers = {}


def create_parser(parser_name):
    parser = parsers.get(parser_name)
    if parser is None:
        parser = _create_parser(parser_name)
    return parser


def _create_parser(parser_name):
    parser = None
    if parser_name == "stanza":
        parser = StanzaParser()

    # elif parser_name == 'spacy':
    # parser = SpacyParser()
    else:
        raise ValueError("Missing valid parser name")

    parsers[parser_name] = parser
    print(f"{parser_name} parser created")
    return parser
