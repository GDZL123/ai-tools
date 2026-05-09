import random
import time
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError

from .config import Config


class LLMClient:
    def __init__(self, config: Config, system_prompt: str):
        self._config = config.llm
        self._system_prompt = system_prompt
        if not self._config.api_key:
            raise RuntimeError(
                f"环境变量 {self._config.api_key_env} 未设置。\n"
                f"请运行: set {self._config.api_key_env}=your-deepseek-key"
            )
        self._client = OpenAI(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
            timeout=float(self._config.request_timeout),
        )
        self._total_tokens = 0
        self._total_calls = 0

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def total_calls(self) -> int:
        return self._total_calls

    def chat(self, user_prompt: str, temperature: float | None = None,
             max_tokens: int | None = None) -> str:
        temp = temperature if temperature is not None else self._config.temperature
        max_tok = max_tokens if max_tokens is not None else self._config.max_tokens

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        last_error = None
        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._config.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=max_tok,
                )
                usage = response.usage
                if usage:
                    self._total_tokens += usage.total_tokens
                self._total_calls += 1
                content = response.choices[0].message.content
                if content is None:
                    raise RuntimeError("API 返回空内容")
                return content

            except (RateLimitError, APIConnectionError, APITimeoutError) as e:
                last_error = e
                if attempt < self._config.max_retries:
                    delay = min(
                        self._config.retry_base_delay * (2 ** attempt) + random.uniform(0, 1),
                        self._config.retry_max_delay,
                    )
                    print(f"  [重试] API错误 ({type(e).__name__})，{delay:.1f}s 后重试 (第{attempt+1}次)")
                    time.sleep(delay)
                else:
                    raise RuntimeError(
                        f"API 调用失败，已重试 {self._config.max_retries} 次。"
                        f"最后错误: {type(last_error).__name__}: {last_error}"
                    ) from last_error

        raise RuntimeError(f"API 调用失败: {last_error}")
