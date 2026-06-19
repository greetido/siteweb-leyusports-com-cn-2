from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.updated_at is None:
            self.updated_at = self.created_at

    def update(self, note: Optional[str] = None, tags: Optional[List[str]] = None):
        if note is not None:
            self.note = note
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "source_url": self.source_url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote):
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def remove(self, keyword: str) -> bool:
        original_len = len(self.notes)
        self.notes = [n for n in self.notes if n.keyword != keyword]
        return len(self.notes) < original_len

    def export_json(self) -> str:
        return json.dumps([note.to_dict() for note in self.notes], ensure_ascii=False, indent=2)

    def format_summary(self) -> str:
        lines = ["Keyword Notes Summary:", "=" * 40]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. [{note.keyword}] - {note.note[:50]}...")
            lines.append(f"   Source: {note.source_url}")
            lines.append(f"   Tags: {', '.join(note.tags) if note.tags else 'none'}")
            lines.append(f"   Created: {note.created_at}")
            lines.append("")
        return "\n".join(lines)

    def format_detailed(self) -> str:
        lines = ["Detailed Keyword Notes:", "=" * 50]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"\n--- Note {i} ---")
            lines.append(f"Keyword    : {note.keyword}")
            lines.append(f"Source URL : {note.source_url}")
            lines.append(f"Note       : {note.note}")
            lines.append(f"Tags       : {', '.join(note.tags) if note.tags else 'none'}")
            lines.append(f"Created at : {note.created_at}")
            lines.append(f"Updated at : {note.updated_at}")
        return "\n".join(lines)


def demo_usage():
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://siteweb-leyusports.com.cn",
        note="乐鱼体育是一个综合体育赛事平台，提供多种体育项目的数据和资讯服务。",
        tags=["体育", "平台", "资讯"]
    )

    note2 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://siteweb-leyusports.com.cn/live",
        note="实时赛事直播功能，用户可在线观看各类体育比赛。",
        tags=["直播", "体育", "实时"]
    )

    note3 = KeywordNote(
        keyword="数据分析",
        source_url="https://siteweb-leyusports.com.cn/stats",
        note="平台提供详细的赛事统计和历史数据分析工具。",
        tags=["数据", "统计", "分析"]
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)

    print(collection.format_summary())
    print("\n")
    print(collection.format_detailed())
    print("\nJSON export:")
    print(collection.export_json())

    print("\nSearch by keyword '乐鱼体育':")
    found = collection.find_by_keyword("乐鱼体育")
    for n in found:
        print(f"  - {n.note[:40]}...")

    print("\nSearch by tag '体育':")
    tagged = collection.find_by_tag("体育")
    for n in tagged:
        print(f"  - {n.keyword}: {n.note[:40]}...")


if __name__ == "__main__":
    demo_usage()