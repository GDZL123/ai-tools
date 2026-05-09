from pathlib import Path


class PromptManager:
    def __init__(self, prompt_dir: str):
        self._prompt_dir = Path(prompt_dir)
        if not self._prompt_dir.is_dir():
            raise FileNotFoundError(f"提示词目录不存在: {self._prompt_dir}")
        self._templates: dict[str, str] = {}
        self._load_all()

    def _load_all(self):
        for fpath in self._prompt_dir.glob("*.txt"):
            name = fpath.stem  # filename without .txt
            with open(fpath, "r", encoding="utf-8") as f:
                raw = f.read()
            # Strip comment lines starting with #
            lines = [line for line in raw.splitlines() if not line.strip().startswith("#")]
            self._templates[name] = "\n".join(lines)

    def render(self, template_name: str, **kwargs) -> str:
        template = self._templates.get(template_name)
        if template is None:
            available = ", ".join(sorted(self._templates.keys()))
            raise KeyError(f"模板 '{template_name}' 不存在。可用模板: {available}")
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise KeyError(
                f"模板 '{template_name}' 缺少占位符 {e} 。"
                f"请检查 prompts/{template_name}.txt"
            ) from e
