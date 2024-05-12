# from typing import Optional, Any, List, Tuple, Iterable
# from representations.parsers.base_parser import BaseParser
# # import spacy


# class SpacyParser(BaseParser):
#     def __init__(self, model="en_core_web_trf") -> None:
#         super().__init__(name="spacy")
#         self.nlp = spacy.load(model)  # download English model

#     def parse(self, text) -> List[Iterable]:
#         doc = self.nlp(text)
#         return [doc]

#     def get_root(self, doc) -> Optional[Iterable]:
#         for token in doc:
#             if self.is_root(token):
#                 return token
#         return None

#     def get_token_info(self, token, doc) -> Tuple[Any, Any, Any, Any, Any]:
#         return (
#             token.i,  # id (str)
#             token.text,  # label (str)
#             token.dep_,  # dep label (str)
#             self.is_head(token),  # head (bool)
#             self.is_root(token),  # root (bool)
#         )

#     def get_token_children(self, token, tokens) -> List[Tuple[Any, Any]]:
#         children = []
#         for t in tokens:
#             if t.head == token or t == token:
#                 head = t == token
#                 children.append((t, head))
#         return children

#     def is_head(self, token) -> bool:
#         return token == token.head

#     def is_root(self, token) -> bool:
#         return token.head == token
