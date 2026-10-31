from core import build_study_plan, split_task


def test_study_plan_distributes_time():
    result = build_study_plan(["数学", "英语", "物理"], 90)
    assert result["total_minutes"] == 90
    assert [block["minutes"] for block in result["blocks"]] == [30, 30, 30]


def test_study_plan_clamps_time_and_ignores_blank_subjects():
    result = build_study_plan([" 数学 ", "", "  "], 9999)
    assert result["total_minutes"] == 720
    assert len(result["blocks"]) == 1
    assert result["blocks"][0]["subject"] == "数学"


def test_study_plan_has_safe_fallback():
    result = build_study_plan([], 60)
    assert [block["subject"] for block in result["blocks"]] == ["数学", "英语"]


def test_split_task_limits_input():
    assert split_task("")["error"]
    assert split_task("x" * 1001)["error"]
    assert len(split_task("做一个网站")["steps"]) == 4
