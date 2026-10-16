

from contextvars import Token
import json
from pathlib import Path
from typing import Annotated, Dict, Optional, Self
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator


class TokenVocabulary(BaseModel):
    """Manages token-to-ID and ID-to-token mappings for constrained decoding."""

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True
    )

    vocabulary_path: Annotated[
        Path,
        Field(description="Path to the vocabulary JSON file.")
    ]

    _token_to_id: Annotated[
        Dict[str, int],
        PrivateAttr(default_factory=dict)
    ]
    
    _id_to_raw_token: Annotated[
        Dict[int, str],
        PrivateAttr(default_factory=dict)
    ]

    _id_to_clean_text: Annotated[
        Dict[int, str],
        PrivateAttr(default_factory=dict)
    ]

    @model_validator(mode="after")
    def _load_vocabulary(self) -> Self:
        """Load and parse vocabulary file after Pydantic validation."""
        path = Path(self.vocabulary_path)
        if not path.is_file():
            raise FileNotFoundError(f"Vocabulary file not found at: {path}")

        try:
            with open(path, "r", encoding="utf-8") as file:
                self._token_to_id = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Malformed vocabulary JSON in {path}: {exc}"
            ) from exc

        self._id_to_raw_token = {
            token_id: token for token, token_id in self._token_to_id.items()
        }

        self._id_to_clean_text = {
            token_id: self.clean_token(token)
            for token, token_id in self._token_to_id.items()
        }

        return self

    @staticmethod
    def clean_token(raw_token: str) -> str:
        """Clean BPE tokenizer special prefix characters.

        Replaces BPE leading space character ('Ġ') with a space and 'Ċ' with a newline.
        """
        return raw_token.replace("Ġ", " ").replace("Ċ", "\n")

    @property
    def vocab_size(self) -> int:
        """Return total number of tokens in the vocabulary."""
        return len(self._token_to_id)

    def get_raw_token(self, token_id: int) -> Optional[str]:
        """Get raw BPE token string for a given token ID."""
        return self._id_to_raw_token.get(token_id)

    def get_clean_text(self, token_id: int) -> Optional[str]:
        """Get cleaned text string for a given token ID."""
        return self._id_to_clean_text.get(token_id)

    def get_id(self, raw_token: str) -> Optional[int]:
        """Get token ID for an exact raw BPE token string."""
        return self._token_to_id.get(raw_token)
    
    def get_ids_for_text(self, text: str) -> list[int]:
        """Find all token IDs whose cleaned text matches input text."""
        return [
            token_id
            for token_id, clean_str in self._id_to_clean_text.items()
            if clean_str == text
        ]