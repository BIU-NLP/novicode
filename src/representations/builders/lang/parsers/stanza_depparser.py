from typing import Optional, Any, Iterable, List, Tuple
from representations.builders.lang.parsers.base_parser import BaseParser
import stanza
stanza.download("en")  # download English model


class StanzaParser(BaseParser):
    def __init__(self) -> None:
        super().__init__(name="stanza")
        print(f"Using Stanza version: {stanza.__version__}")
        self.nlp = stanza.Pipeline(
            lang="en", processors="tokenize,mwt,pos,lemma,depparse"
        )  # initialize English neural pipeline

    def parse(self, text) -> List[Iterable]:
        doc = self.nlp(text)
        return doc.sentences

    def get_root(self, doc) -> Optional[any]:
        for word in doc.words:
            if word.deprel == "root":
                return word
        return None

    def get_token_info(self, token, doc) -> Tuple[Any, Any, Any, Any, Any]:
        return (
            token.id,  # id (str)
            token.text,  # label (str)
            token.deprel,  # dep label (str)
            self.is_head(token, doc),  # head (bool)
            self.is_root(token),  # root (bool)
            self.is_terminal(token),  # terminal (bool)
        )

    def get_token_children(self, token, doc) -> List[Tuple[Any, Any]]:
        children = []
        for word in doc.words:
            if (
                word.head == token.id or word.id == token.id
            ):  # children are the words that have the token as their head (or the token itself)
                head = word.id == token.id
                children.append((word, head))
        return children

    def is_head(self, token, doc) -> bool:
        siblings = [word for word in doc.words if word.head == token.head]
        head = token.head == 0 or any([word.head == token.id for word in siblings])
        return head

    def is_root(self, token) -> bool:
        root = token.deprel == "root"
        return root

    def is_terminal(self, token) -> bool:
        terminal = token.deps is None
        return terminal
