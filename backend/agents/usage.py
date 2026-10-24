"""Token usage and cost (USD) for every model call, using the prices in config.py."""

from dataclasses import asdict, dataclass

from backend import config


@dataclass
class Usage:
    input_tokens: int = 0  # all input tokens, including cached and cache-write tokens
    cached_input_tokens: int = 0
    cache_write_tokens: int = 0
    output_tokens: int = 0  # includes reasoning tokens
    reasoning_tokens: int = 0
    model_calls: int = 0
    cost_usd: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def add(self, other: "Usage") -> None:
        for field in ("input_tokens", "cached_input_tokens", "cache_write_tokens", "output_tokens",
                      "reasoning_tokens", "model_calls", "cost_usd"):
            setattr(self, field, getattr(self, field) + getattr(other, field))

    def as_dict(self) -> dict:
        d = asdict(self)
        d["total_tokens"] = self.total_tokens
        d["cost_usd"] = round(self.cost_usd, 6)
        return d


def cost_usd(input_tokens: int, cached: int, cache_write: int, output_tokens: int) -> float:
    """Charge each kind of token at its own rate (USD per 1M tokens)."""
    p = config.PRICES_PER_MILLION
    regular = max(0, input_tokens - cached - cache_write)
    return (regular * p["input"] + cached * p["cached_input"] + cache_write * p["cache_write"]
            + output_tokens * p["output"]) / 1_000_000


def _get(obj, name, default=0):
    if obj is None:
        return default
    value = obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)
    return default if value is None else value


def usage_from_response(response) -> Usage:
    """Read input_tokens, output_tokens and input_tokens_details.{cached_tokens, cache_write_tokens}."""
    u = _get(response, "usage", None)
    details = _get(u, "input_tokens_details", None)
    out_details = _get(u, "output_tokens_details", None)
    inp, out = int(_get(u, "input_tokens")), int(_get(u, "output_tokens"))
    cached, write = int(_get(details, "cached_tokens")), int(_get(details, "cache_write_tokens"))
    return Usage(input_tokens=inp, cached_input_tokens=cached, cache_write_tokens=write, output_tokens=out,
                 reasoning_tokens=int(_get(out_details, "reasoning_tokens")), model_calls=1,
                 cost_usd=cost_usd(inp, cached, write, out))
