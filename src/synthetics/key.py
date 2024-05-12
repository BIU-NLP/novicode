from typing import Optional
import re


class Key:
    def __init__(
        self,
        label: str,
        key: Optional[str] = None,
        index_prefix: Optional[str] = None,
        count: int = 1,
        key_regex: str = rf"^[^\[\.\:]+",
    ) -> None:
        self.key = key or re.search(key_regex, label).group(
            0
        )  # label.split(key_params_divider, 1)[0].split(key_index_divider)[0]
        self.label = label
        
        prefix = f"{index_prefix}_" if index_prefix else ""
        self.index = (
            f'{prefix}{str(label.split(".")[1])}' if len(label.split(".")) > 1 else None
        )

        self.count = count

    def __str__(self) -> str:
        return self.key

    def __repr__(self) -> str:
        return self.key
    
    def __eq__(self, __o: object) -> bool:
        return self.label == __o.label
