"""Prompt module for LLM SDK."""

import json
from typing import Annotated, Any, Dict
from pydantic import BaseModel, ConfigDict, Field

from src.models import FunctionSchema

DEFAULT_PROMPT_TEMPLATE = (
    "You are an expert function calling\n."
    "Your primary task is to analyze the user's request and select the single"

    "The most appropriate function from the appropriate tools.\n\n"
    "CRITICAL OUTPUT RULES:\n"
    "1. Respond ONLY with a JSON object matching this extract structure:\n"
    "   {\n"
    '        "name": "<selected_function_name>",\n'
    '        "parameters": {\n'
    '            "<parameter_name>": <parameter_value>\n'
    "        }\n"
    "   }\n"
    "2. Do NOT include any explanations, prose, or markdown code blocks(```json).\n"
    "3. Ensure all parameter names and data types strictly match the provided schema.\n\n"
    "Available tools:\n"
    "{tools_json}"
)

class PromptBuilder(BaseModel):
    """Class to build prompts for LLM function calls."""

    model_config = ConfigDict(extra="ignore")

    prompt_template: Annotated[
        str,
        Field(
            default=DEFAULT_PROMPT_TEMPLATE,
            description="Template for the prompt to be sent to the LLM.",
        ),
    ]

    @staticmethod
    def function_to_json(function_schema: FunctionSchema) -> Dict[str, Any]:
        """Convert a FunctionSchema instance to a JSON dictionary.""" 
        properties_dict: Dict[str, Any] = {}
        
        for param_name, param_schema in function_schema.parameters.properties.items():
            protocol_dict: Dict[str, Any] = {
                "type": param_schema.type
            }
            if param_schema.description:
                protocol_dict["description"] = param_schema.description
            properties_dict[param_name] = protocol_dict
        
        return {
            "type": "function",
            "function": {
                "name": function_schema.name,
                "description": function_schema.description,
                "parameters": {
                    "type": "object",
                    "properties": properties_dict,
                    "required": function_schema.parameters.required,
                },
            },
        }

    def build_system_prompt(self, tools: list[FunctionSchema]) -> str:
        """Build the system prompt with the provided tools."""

        schemas_list = [self.function_to_json(tool) for tool in tools]
        tools_json = json.dumps(schemas_list, indent=2, ensure_ascii=False)
        return self.prompt_template.format(tools_json=tools_json)

    def build_user_prompt(
        self,
        user_request: str,
        functions: list[FunctionSchema]
    ) -> str:

        """Build the user prompt with the provided request and functions."""

        system_prompt = self.build_system_prompt(functions)
        return (
            f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
            f"<|im_start|>user\n{user_request}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )