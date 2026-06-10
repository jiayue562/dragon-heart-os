#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心 OS 分层动员模块 v1.0
根据场景置信度动态选择动员级别：轻载/标准/深度

版本：v1.0
创建：2026-06-10
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MobilizationLevel(Enum):
    """动员级别"""
    LIGHT = "light"       # 轻载模式：单引擎，最快响应
    STANDARD = "standard"  # 标准模式：多引擎+AIOS核心层
    DEEP = "deep"          # 深度模式：全引擎+全AIOS联动


@dataclass
class MobilizationConfig:
    """分层动员配置"""
    level: MobilizationLevel
    name: str
    description: str
    max_engines: int
    brain_os: str          # none/core/extended/full
    claw_os: str           # none/targeted/all
    threshold_base: float
    scenes: List[str] = field(default_factory=list)
    response_style: str = ""


class MobilizationEngine:
    """分层动员引擎"""

    # 三级动员配置
    LEVELS = {
        MobilizationLevel.LIGHT: MobilizationConfig(
            level=MobilizationLevel.LIGHT,
            name="轻载模式",
            description="日常对话/简单任务，单引擎响应，最快速度",
            max_engines=1,
            brain_os="none",
            claw_os="none",
            threshold_base=0.7,
            scenes=["S0", "S1", "S2"],
            response_style="简洁直接"
        ),
        MobilizationLevel.STANDARD: MobilizationConfig(
            level=MobilizationLevel.STANDARD,
            name="标准模式",
            description="分析决策/创意创造，多引擎协同，调用龙脑OS核心模型",
            max_engines=3,
            brain_os="core",
            claw_os="targeted",
            threshold_base=0.8,
            scenes=["S3", "S4", "S6", "S7", "S8"],
            response_style="结构化深度"
        ),
        MobilizationLevel.DEEP: MobilizationConfig(
            level=MobilizationLevel.DEEP,
            name="深度模式",
            description="重大决策/系统进化，全引擎+全AIOS层联动",
            max_engines=5,
            brain_os="full",
            claw_os="all",
            threshold_base=0.9,
            scenes=["S5", "S9"],
            response_style="全景深度剖析"
        )
    }

    def __init__(self):
        """初始化动员引擎"""
        self.activation_history: List[Dict] = []
        self.last_level: Optional[MobilizationLevel] = None

    def determine_level(self, scene_code: str, confidence: float,
                        input_length: int = 0, context: Dict = None) -> MobilizationConfig:
        """
        根据场景代码和置信度判定动员级别

        Args:
            scene_code: 场景代码 (S0-S9)
            confidence: 识别置信度 (0.0-1.0)
            input_length: 输入文本长度
            context: 上下文信息（可选）

        Returns:
            MobilizationConfig: 动员配置
        """
        # 1. 预先判定：深度场景直接使用深度模式
        if scene_code in ("S5", "S9"):
            selected = self.LEVELS[MobilizationLevel.DEEP]
        # 2. 标准场景
        elif scene_code in ("S3", "S4", "S6", "S7", "S8"):
            selected = self.LEVELS[MobilizationLevel.STANDARD]
        # 3. 轻载场景
        else:
            selected = self.LEVELS[MobilizationLevel.LIGHT]

        # 4. 置信度调整
        effective_confidence = min(confidence + 0.1, 1.0)

        # 5. 如果有历史，检查是否需要升级
        if self.last_level and context:
            history_bonus = self._calc_history_bonus(context)
            if history_bonus > 0.15 and selected.max_engines < 3:
                # 历史上下文丰富 → 升级到标准模式
                selected = self.LEVELS[MobilizationLevel.STANDARD]

        # 6. 输入长度调整（长文本自动升级）
        if input_length > 500 and selected.level == MobilizationLevel.LIGHT:
            selected = self.LEVELS[MobilizationLevel.STANDARD]

        return selected

    def _calc_history_bonus(self, context: Dict) -> float:
        """计算历史上下文加成分"""
        bonus = 0.0

        if not context:
            return bonus

        # 历史对话轮次加成
        if "history_length" in context:
            if context["history_length"] > 5:
                bonus += 0.05
            if context["history_length"] > 10:
                bonus += 0.05

        # 话题深度加成
        if "topic_depth" in context:
            bonus += min(context["topic_depth"] * 0.1, 0.15)

        # 情绪强度加成
        if "emotion_intensity" in context:
            if context["emotion_intensity"] > 0.7:
                bonus += 0.05

        return bonus

    def get_aios_level(self, level: MobilizationLevel) -> Dict:
        """
        获取 AIOS 联动配置

        Returns:
            Dict: {brain_os: str, claw_os: str, description: str}
        """
        config = self.LEVELS[level]

        brain_desc = {
            "none": "不联动龙脑OS",
            "core": "联动龙脑OS核心层（MECE/金字塔/第一性原理等）",
            "extended": "联动龙脑OS扩展层（决策矩阵/7S等）",
            "full": "联动龙脑OS全层（核心+扩展+教员方法论）"
        }

        claw_desc = {
            "none": "不联动龙爪OS",
            "targeted": "联动龙爪OS对应子系统",
            "all": "联动龙爪OS全部子系统"
        }

        return {
            "brain_os": config.brain_os,
            "claw_os": config.claw_os,
            "brain_os_description": brain_desc.get(config.brain_os, ""),
            "claw_os_description": claw_desc.get(config.claw_os, ""),
            "max_engines": config.max_engines,
            "response_style": config.response_style
        }

    def log_activation(self, scene_code: str, confidence: float,
                       level: MobilizationLevel, engines: List[str]) -> None:
        """记录动员激活"""
        record = {
            "scene_code": scene_code,
            "confidence": confidence,
            "level": level.value,
            "level_name": self.LEVELS[level].name,
            "engines": engines,
            "max_engines": self.LEVELS[level].max_engines
        }
        self.activation_history.append(record)
        self.last_level = level

    def export_report(self) -> str:
        """导出动员报告"""
        if not self.activation_history:
            return "## 分层动员\n\n暂无动员记录。\n"

        lines = ["## 分层动员\n"]
        for i, record in enumerate(self.activation_history[-10:], 1):
            lines.append(
                f"- 第{i}次: {record['scene_code']} "
                f"| 动员: {record['level_name']} "
                f"| 引擎: {', '.join(record['engines'][:3])}"
            )

        return "\n".join(lines)


def main():
    """测试分层动员模块"""
    engine = MobilizationEngine()

    test_cases = [
        ("S0", 0.75, "你好"),
        ("S1", 0.82, "帮我写个脚本"),
        ("S2", 0.85, "深度学习这篇文章"),
        ("S3", 0.80, "创意创新问题"),
        ("S4", 0.75, "如何落地实施"),
        ("S5", 0.70, "人生重大决策"),
        ("S6", 0.85, "开会跑题"),
        ("S7", 0.80, "编译知识库"),
        ("S8", 0.70, "修行文化"),
        ("S9", 0.65, "系统进化")
    ]

    print("=" * 70)
    print("龙心 OS 分层动员模块测试")
    print("=" * 70)

    for scene_code, confidence, text in test_cases:
        config = engine.determine_level(scene_code, confidence, len(text))
        aios = engine.get_aios_level(config.level)

        print(f"\n场景: {scene_code} | 置信度: {confidence:.0%}")
        print(f"  动员级别: {config.name}")
        print(f"  最大引擎: {config.max_engines}")
        print(f"  龙脑OS: {aios['brain_os_description']}")
        print(f"  龙爪OS: {aios['claw_os_description']}")
        print(f"  响应风格: {config.response_style}")

        engine.log_activation(scene_code, confidence, config.level, ["引擎A", "引擎B", "引擎C"][:config.max_engines])

    print(f"\n{'='*70}")
    print(engine.export_report())


if __name__ == "__main__":
    main()