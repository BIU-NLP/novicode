
class BaseParser:
    
    def __init__(self, name) -> None:
        self.name = name
        
    def parse(self, text):
        raise NotImplementedError()
    
    def get_root(self, doc):
        raise NotImplementedError()