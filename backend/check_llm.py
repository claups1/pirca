"""One tiny test call to confirm the Portkey key and model work.

Run from the Final Project folder:
    .venv\\Scripts\\python.exe -m backend.check_llm
"""

from backend import config
from backend.llm import get_client


def main() -> None:
    response = get_client().chat.completions.create(
        model=config.MODEL_NAME,
        messages=[{"role": "user", "content": "Reply with the single word: OK"}],
    )
    usage = response.usage
    print(
        f"OK  model={config.MODEL_NAME}  "
        f"prompt_tokens={usage.prompt_tokens}  "
        f"completion_tokens={usage.completion_tokens}  "
        f"total_tokens={usage.total_tokens}"
    )


if __name__ == "__main__":
    main()
