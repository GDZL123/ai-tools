from pathlib import Path


class PromptManager:
    def __init__(self, prompt_dir: str):
        self._prompt_dir = Path(prompt_dir)
        if not self._prompt_dir.is_dir():
            raise FileNotFoundError(f"提示词目录不存在: {self._prompt_dir}")
        self._templates: dict[str, str] = {}
        self._load_all()

    def _load_all(self):
        # Load root-level .txt files
        for fpath in self._prompt_dir.glob("*.txt"):
            name = fpath.stem
            if name not in self._templates:
                self._templates[name] = self._read(fpath)
        # Load tone-specific .txt files (e.g. tech/intro → key "tech/intro")
        for subdir in self._prompt_dir.iterdir():
            if subdir.is_dir():
                for fpath in subdir.glob("*.txt"):
                    key = f"{subdir.name}/{fpath.stem}"
                    if key not in self._templates:
                        self._templates[key] = self._read(fpath)

    def _read(self, path: Path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        lines = [line for line in raw.splitlines()
                 if not line.strip().startswith("#")]
        return "\n".join(lines)

    def render(self, template_name: str, tone: str = "", **kwargs) -> str:
        # Try tone-specific first, fall back to root
        key = f"{tone}/{template_name}" if tone else template_name
        template = self._templates.get(key) or self._templates.get(template_name)
        if template is None:
            available = ", ".join(sorted(self._templates.keys()))
            raise KeyError(f"模板 '{template_name}' 不存在。可用模板: {available}")
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise KeyError(
                f"模板 '{template_name}' 缺少占位符 {e} 。"
                f"请检查 prompts/{key}.txt"
            ) from e
