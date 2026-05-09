import csv
import os
from pathlib import Path


class CSVManager:
    COLUMNS = ["keyword", "search_volume", "difficulty", "category", "status",
               "generated_title", "output_file"]

    def __init__(self, csv_path: str):
        self._csv_path = csv_path
        self._ensure_file()

    def _ensure_file(self):
        p = Path(self._csv_path)
        if p.exists():
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.COLUMNS)

    def _read_rows(self) -> list[dict]:
        try:
            with open(self._csv_path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []

    def _write_rows(self, rows: list[dict]):
        temp = self._csv_path + ".tmp"
        with open(temp, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.COLUMNS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temp, self._csv_path)

    def get_pending_keywords(self) -> list[dict]:
        rows = self._read_rows()
        pending = []
        for r in rows:
            status = r.get("status", "").strip()
            if status in ("", "pending", "in_progress"):
                # Normalize missing fields
                r.setdefault("status", "pending")
                r.setdefault("generated_title", "")
                r.setdefault("output_file", "")
                pending.append(r)
        return pending

    def update_status(self, keyword: str, status: str, **extra):
        rows = self._read_rows()
        for r in rows:
            if r["keyword"].strip() == keyword.strip():
                r["status"] = status
                for k, v in extra.items():
                    r[k] = str(v)
                break
        self._write_rows(rows)

    def is_done(self, keyword: str) -> bool:
        rows = self._read_rows()
        for r in rows:
            if r["keyword"].strip() == keyword.strip():
                return r.get("status", "").strip() == "done"
        return False

    def status_summary(self) -> dict:
        rows = self._read_rows()
        counts = {"total": len(rows), "pending": 0, "done": 0, "error": 0, "in_progress": 0}
        for r in rows:
            s = r.get("status", "pending").strip()
            counts[s] = counts.get(s, 0) + 1
        return counts
