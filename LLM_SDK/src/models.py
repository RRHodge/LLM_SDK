

from typing import Annotated, Any, Optional
from unicodedata import name
from pydantic import BaseModel, ConfigDict, Field


class ParameterProperty(BaseModel):
    """Schema for an individual parameter property in a function definition."""

    model_config = ConfigDict(extra="ignore")

    type: Annotated[
        str,
        Field(
            description="Data type of parameter (e.g., 'string', 'number', 'boolean').",
            alias="type",
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(
            description="Human-readable description of the parameter.",
        ),
    ]


class FunctionParameters(BaseModel):
    """Schema for the parameters object in a function definition."""

    model_config = ConfigDict(extra="ignore")

    type: Annotated[
        str,
        Field(
            default="object",
            description="Container type for parameters, usually 'object'.",
        ),
    ]
    properties: Annotated[
        dict[str, ParameterProperty],
        Field(
            default_factory=dict,
            description="Dictionary mapping parameter names to property schemas.",
        ),
    ]
    required: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of parameter names required for function execution.",
        ),
    ]


class FunctionReturns(BaseModel):
    """Schema for the return value of a function."""

    model_config = ConfigDict(extra="ignore")

    type: Annotated[
        str,
        Field(
            description="Data type of the return value (e.g., 'string', 'number', 'boolean').",
        ),
    ]


class FunctionSchema(BaseModel):
    """Complete schema definition for an executable tool function."""
    
    model_config = ConfigDict(extra="ignore")

    name: Annotated[str, Field(description="Unique identifier for the function, used in calls.")]
    description: Annotated[
        str,
        Field(
            description="Description of what the function does. Human-readable description of the function's purpose and behavior."
        ),
    ]
    
    parameters: Annotated[
        FunctionParameters,
        Field(
            default_factory=FunctionParameters,
            description="Parameters accepted by the function.",
        ),
    ]

    returns: Annotated[
        FunctionReturns,
        Field(
            default_factory=FunctionReturns,
            description="Schema for the return value of the function.",
        ),
    ]


class PromptSchema(BaseModel):
    """Schema for a prompt template used in function calls."""

    model_config = ConfigDict(extra="ignore")

    prompt: Annotated[
        str,
        Field(
            description="Natural language request prompt to be processed by the LLM.",
        ),
    ]


class FunctionResult(BaseModel):
    """Schema for the result of a function execution."""

    model_config = ConfigDict(extra="ignore")

    prompt: Annotated[
        str,
        Field(
            description="Natural language request prompt that was processed by the LLM.",
        ),
    ]

    name: Annotated[
        str,
        Field(description="Name of the function that was executed.")
    ]

    parameters: Annotated[
        dict[str, Any],
        Field(
            default_factory=dict,
            description="Dictionary of parameters passed to the function during execution.",
        ),
    ]