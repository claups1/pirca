"""Shared OpenAI client that routes through Portkey.

The API key is read from the environment at call time. It is never printed,
logged, or returned to the frontend.
"""

import os

from openai import OpenAI

from backend import config


def get_client() -> OpenAI:
    api_key = os.environ.get("PORTKEY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "PORTKEY_API_KEY is not set. Add it to Final Project/.env "
            "or the .env one folder above."
        )
    return OpenAI(
        api_key=api_key,
        base_url=config.PORTKEY_BASE_URL,
        default_headers={"x-portkey-provider": config.PORTKEY_PROVIDER},
    )
