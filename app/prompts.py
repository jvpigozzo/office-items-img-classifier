import os
import string
import tiktoken
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Any
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()
MAX_TOKENS = os.environ.get("MAX_TOKENS")


class PromptValidator:
    def __init__(self, prompt: str, encoding_name: str = "cl100k_base"):
        self.prompt_txt = prompt.text
        self.encoding_name = encoding_name
        self.num_tokens = self._count_tokens()
        self.is_valid = self._is_valid()

    def _count_tokens(self):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(self.encoding_name)
        return len(encoding.encode(self.prompt_txt))

    def _is_valid(self):
        return self.num_tokens <= int(MAX_TOKENS)


class PromptGenerator:
    def __init__(self, template: str, model_class: BaseModel, **kwargs):
        self.template: str = template
        self.model_class: BaseModel = model_class
        self.input_variables: Optional[List[str]] = None
        self.partial_variables: Optional[dict[str, Any]] = None
        self.parser: Optional[PydanticOutputParser] = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._get_input_variables()
        self.prompt = self._build_prompt()

    def _get_input_variables(self) -> None:
        self.input_variables = [
            v[1]
            for v in string.Formatter().parse(self.template)
            if v[1] is not None and v[1] != "format_instructions"
        ]
        self._get_parser()

    def _get_parser(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=self.model_class)
        if self.parser:
            self._get_partial_variables()

    def _get_partial_variables(self) -> None:
        if self.parser:
            self.partial_variables = {
                "format_instructions": self.parser.get_format_instructions()
            }

    def _append_inputs(self, **kwargs) -> None:
        self.input_values = {}
        for var in self.input_variables:
            self.input_values[var] = getattr(self, var)

    def _build_prompt(self) -> Optional[str]:
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=self.input_variables,
            partial_variables=self.partial_variables,
        )
        self._append_inputs()
        self.prompt_formatted = self.prompt.format_prompt(**self.input_values)
        self.prompt_validation = PromptValidator(self.prompt_formatted)
        if self.prompt_validation.is_valid:
            return self.prompt_formatted
        else:
            print(
                f"Prompt not valid. Number of tokens: {self.prompt_validation.num_tokens}"
            )
            return None
