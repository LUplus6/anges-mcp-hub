"""Dependency-light deterministic helper functions used by the MCP tools."""
from __future__ import annotations
from typing import Any


def build_study_plan(subjects: list[str], available_minutes: int = 180) -> dict[str, Any]:
    cleaned = [subject.strip()[:40] for subject in subjects if subject and subject.strip()]
    if not cleaned:
        cleaned = ["数学", "英语"]
    cleaned = cleaned[:8]
    minutes = max(30, min(int(available_minutes), 720))
    quotient, remainder = divmod(minutes, len(cleaned))
    blocks = []
    for index, subject in enumerate(cleaned):
        blocks.append({
            "subject": subject,
            "minutes": quotient + (1 if index < remainder else 0),
            "task": "先独立完成基础/中档题，再订正错题并写下卡点",
        })
    return {
        "total_minutes": minutes,
        "blocks": blocks,
        "method": "每完成一个学习块休息 5–10 分钟；优先复盘错题，不追求盲目刷题量。",
        "note": "这是模板计划，请根据学校作息、考试安排和真实掌握情况调整。",
    }


def split_task(task: str) -> dict[str, Any]:
    task = (task or "").strip()
    if not task:
        return {"error": "请提供一个具体目标。"}
    if len(task) > 1000:
        return {"error": "目标最多 1000 个字符。"}
    return {
        "goal": task,
        "steps": [
            "明确完成标准和限制条件",
            "收集完成任务所需的信息或材料",
            "先完成一个 10–20 分钟内可验证的小步骤",
            "检查结果并记录尚未解决的问题",
        ],
        "warning": "本工具只生成建议，不会自动访问文件、运行命令或修改外部系统。",
    }
