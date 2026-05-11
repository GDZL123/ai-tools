import os
import sys
from pathlib import Path
from dataclasses import dataclass

import yaml


def _load_dotenv(env_path: str = ".env"):
    """Load .env file into os.environ. No external dependency needed."""
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


@dataclass(frozen=True)
class LLMConfig:
    api_key_env: str
    base_url: str
    model: str
    temperature: float
    max_tokens: int
    request_timeout: int
    max_retries: int
    retry_base_delay: float
    retry_max_delay: float

    @property
    def api_key(self) -> str:
        return os.environ.get(self.api_key_env, "")


@dataclass(frozen=True)
class GenerationConfig:
    title_count: int
    min_chars_per_section: int
    max_chars_per_section: int
    target_total_chars: int
    language: str


@dataclass(frozen=True)
class PathsConfig:
    input_csv: str
    output_dir: str
    prompt_dir: str
    state_dir: str
    hugo_content_dir: str = ""  # 可选：自动输出到 Hugo content/posts/


@dataclass(frozen=True)
class Config:
    llm: LLMConfig
    generation: GenerationConfig
    paths: PathsConfig


def _load_raw(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        sys.exit(f"[ERROR] 配置文件不存在: {path}")
    with open(path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            sys.exit(f"[ERROR] 配置文件格式错误 ({config_path}): {e}")


def load_config(config_path: str = "config.yaml") -> Config:
    _load_dotenv()  # Load .env before accessing env vars
    raw = _load_raw(config_path)

    required_sections = ["llm", "generation", "paths"]
    for section in required_sections:
        if section not in raw:
            sys.exit(f"[ERROR] 配置文件缺少 [{section}] 节点")

    llm = LLMConfig(**raw["llm"])
    generation = GenerationConfig(**raw["generation"])
    paths = PathsConfig(**raw["paths"])

    # Ensure output and state dirs exist
    Path(paths.output_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.state_dir).mkdir(parents=True, exist_ok=True)

    return Config(llm=llm, generation=generation, paths=paths)
