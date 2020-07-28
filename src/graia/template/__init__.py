from typing import List, Union
from graia.application.protocol.entities.message import ExternalElement, InternalElement
from graia.application.protocol.entities.message.elements.internal import Plain
import regex
from pydantic import validate_arguments
from graia.application.protocol.entities.message.chain import MessageChain

def list_get(l, index, default):
    if len(l)-1 >= index:
        return l[index]
    return default

class Template:
    template: str

    def __init__(self, template: str) -> None:
        self.template = template

    def split_template(self) -> List[str]:
        return regex.split(r"(?|(\$[a-zA-Z_][a-zA-Z0-9_]*)|(\$[0-9]*))", self.template)

    @validate_arguments
    def render(self,
        *args: Union[InternalElement, ExternalElement],
        **kwargs: Union[InternalElement, ExternalElement]
    ) -> MessageChain:
        patterns = []
        for pattern in self.split_template():
            if pattern:
                if not pattern.startswith("$"):
                    patterns.append(Plain(pattern))
                else:
                    if regex.match(r"\$[a-zA-Z_][a-zA-Z0-9_]*", pattern):
                        patterns.append(kwargs.get(pattern[1:], Plain(pattern)))
                    elif regex.match(r"\$[0-9]*", pattern):
                        patterns.append(list_get(args, int(pattern[1:])))
        return MessageChain.create(patterns)