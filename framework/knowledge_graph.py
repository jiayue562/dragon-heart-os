#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心 OS 知识图谱模块 v1.0
双向链接 + 五行分类图谱 + 跨域映射

版本：v1.0
创建：2026-06-10
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class KnowledgeNode:
    """知识图谱节点"""
    node_id: str
    name: str
    category: str          # engine/scene/case/concept
    element: str           # 木/火/土/金/水
    description: str = ""
    linked_nodes: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


# 五行生克映射
FIVE_ELEMENT_CYCLE = {
    "木": {"generates": "火", "overcomes": "土", "generated_by": "水", "overcome_by": "金"},
    "火": {"generates": "土", "overcomes": "金", "generated_by": "木", "overcome_by": "水"},
    "土": {"generates": "金", "overcomes": "水", "generated_by": "火", "overcome_by": "木"},
    "金": {"generates": "水", "overcomes": "木", "generated_by": "土", "overcome_by": "火"},
    "水": {"generates": "木", "overcomes": "火", "generated_by": "金", "overcome_by": "土"}
}


class KnowledgeGraph:
    """龙心 OS 知识图谱"""

    # 引擎→五行映射
    ENGINE_ELEMENT_MAP = {
        "象思维": "木",
        "人机协同五象限": "火",
        "龙心OS": "土",
        "知行合一": "土",
        "五色光思维": "金",
        "知识学习": "水"
    }

    # 龙心 OS 核心节点（预定义）
    CORE_NODES = {
        "dragonheart_os": KnowledgeNode(
            node_id="dragonheart_os",
            name="龙心 OS",
            category="system",
            element="土",
            description="1+5模式智能体调度中枢",
            linked_nodes=["zhixing", "zhishi", "renji", "xiangsiwei", "wuseguang"],
            tags=["调度中枢", "1+5模式", "AIOS/L1"]
        ),
        "zhixing": KnowledgeNode(
            node_id="zhixing",
            name="知行合一",
            category="engine",
            element="土",
            description="概念落地转化引擎",
            linked_nodes=["dragonheart_os"],
            tags=["引擎", "落地", "执行"]
        ),
        "zhishi": KnowledgeNode(
            node_id="zhishi",
            name="知识学习",
            category="engine",
            element="水",
            description="深度认知学习引擎",
            linked_nodes=["dragonheart_os"],
            tags=["引擎", "认知", "编译"]
        ),
        "renji": KnowledgeNode(
            node_id="renji",
            name="人机协同五象限",
            category="engine",
            element="火",
            description="人机共生协作引擎",
            linked_nodes=["dragonheart_os"],
            tags=["引擎", "协同", "赋能"]
        ),
        "xiangsiwei": KnowledgeNode(
            node_id="xiangsiwei",
            name="象思维",
            category="engine",
            element="木",
            description="0→1原创思维引擎",
            linked_nodes=["dragonheart_os"],
            tags=["引擎", "原创", "类比"]
        ),
        "wuseguang": KnowledgeNode(
            node_id="wuseguang",
            name="五色光思维",
            category="engine",
            element="金",
            description="结构化决策引擎",
            linked_nodes=["dragonheart_os"],
            tags=["引擎", "决策", "结构"]
        )
    }

    def __init__(self, storage_path: Optional[Path] = None):
        """初始化知识图谱"""
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[Dict] = []
        self.cases: List[Dict] = []

        # 加载核心节点
        for node_id, node in self.CORE_NODES.items():
            self.nodes[node_id] = node

        # 设置存储路径
        if storage_path:
            self.storage_path = storage_path
        else:
            self.storage_path = Path(__file__).parent / "knowledge_graph_data.json"

        # 尝试从文件加载已有数据
        self._load_from_file()

    def get_element_for_engine(self, engine_name: str) -> str:
        """获取引擎对应的五行属性"""
        return self.ENGINE_ELEMENT_MAP.get(engine_name, "土")

    def get_element_cycle(self, element: str) -> Dict:
        """获取五行的生克关系"""
        return FIVE_ELEMENT_CYCLE.get(element, {})

    def get_linked_engines_by_element(self, element: str) -> List[Tuple[str, str, str]]:
        """
        按五行关系获取关联引擎

        Returns:
            List of (engine_name, relation, element)
            例: [("知识学习", "生我", "水"), ("五色光思维", "我生", "金")]
        """
        cycle = self.get_element_cycle(element)
        result = []

        # 生我（母）
        generated_by_elem = cycle.get("generated_by", "")
        for name, elem in self.ENGINE_ELEMENT_MAP.items():
            if elem == generated_by_elem:
                result.append((name, "生我", elem))

        # 我生（子）
        generates_elem = cycle.get("generates", "")
        for name, elem in self.ENGINE_ELEMENT_MAP.items():
            if elem == generates_elem:
                result.append((name, "我生", elem))

        return result

    def add_case(self, case_data: Dict) -> str:
        """
        添加案例到知识图谱

        Args:
            case_data: {
                "title": str,
                "scene": str,
                "engine": str,
                "output_type": str,
                "description": str,
                "linked_engines": List[str],
                "knowledge_graph_tags": List[str]
            }

        Returns:
            str: case_id
        """
        case_id = f"case_{len(self.cases) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        case = {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            **case_data
        }
        self.cases.append(case)

        # 自动建立节点关联
        engine = case_data.get("engine", "")
        element = self.get_element_for_engine(engine)
        if element:
            # 创建案例节点并关联到引擎
            case_node = KnowledgeNode(
                node_id=case_id,
                name=case_data.get("title", "未命名案例"),
                category="case",
                element=element,
                description=case_data.get("description", ""),
                linked_nodes=[engine],
                tags=[f"scene:{case_data.get('scene', '')}", f"engine:{engine}"]
            )
            self.nodes[case_id] = case_node

        self._save_to_file()
        return case_id

    def query_by_engine(self, engine_name: str) -> List[Dict]:
        """按引擎查询所有关联案例"""
        return [c for c in self.cases if c.get("engine") == engine_name]

    def query_by_scene(self, scene_code: str) -> List[Dict]:
        """按场景查询所有案例"""
        return [c for c in self.cases if c.get("scene") == scene_code]

    def query_by_element(self, element: str) -> List[Dict]:
        """按五行属性查询所有案例"""
        return [
            c for c in self.cases
            if self.get_element_for_engine(c.get("engine", "")) == element
        ]

    def query_by_tag(self, tag: str) -> List[Dict]:
        """按标签查询案例"""
        return [c for c in self.cases if tag in c.get("knowledge_graph_tags", [])]

    def get_graph_summary(self) -> Dict:
        """获取知识图谱摘要"""
        element_counts = {}
        for node in self.nodes.values():
            elem = node.element
            element_counts[elem] = element_counts.get(elem, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_cases": len(self.cases),
            "total_edges": len(self.edges),
            "element_distribution": element_counts,
            "engines": list(self.ENGINE_ELEMENT_MAP.keys()),
            "five_element_cycle": {k: v["generates"] for k, v in FIVE_ELEMENT_CYCLE.items()}
        }

    def export_mermaid(self) -> str:
        """导出 Mermaid 格式图谱"""
        lines = ["```mermaid", "graph TD"]

        for node_id, node in self.nodes.items():
            label = node.name.replace("(", "").replace(")", "")
            lines.append(f"    {node_id}[{label}]")

        lines.append("")
        for node_id, node in self.nodes.items():
            for linked_id in node.linked_nodes:
                if linked_id in self.nodes:
                    lines.append(f"    {node_id} --> {linked_id}")

        lines.append("```")
        return "\n".join(lines)

    def _save_to_file(self) -> None:
        """保存图谱数据到文件"""
        try:
            data = {
                "nodes": {k: v.__dict__ for k, v in self.nodes.items()},
                "edges": self.edges,
                "cases": self.cases,
                "updated_at": datetime.now().isoformat()
            }
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # 静默失败，不影响主流程

    def _load_from_file(self) -> None:
        """从文件加载图谱数据"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.edges = data.get("edges", [])
                self.cases = data.get("cases", [])
        except Exception:
            pass


def main():
    """测试知识图谱模块"""
    kg = KnowledgeGraph()

    print("=" * 70)
    print("龙心 OS 知识图谱模块测试")
    print("=" * 70)

    # 测试引擎→五行映射
    print("\n--- 引擎五行映射 ---")
    for engine, element in kg.ENGINE_ELEMENT_MAP.items():
        cycle = kg.get_element_cycle(element)
        print(f"  {engine} → {element}（{element}生{cycle['generates']}）")

    # 测试五行关联
    print("\n--- 五行生克联动 ---")
    for element in ["木", "火", "土", "金", "水"]:
        linked = kg.get_linked_engines_by_element(element)
        if linked:
            for name, rel, elem in linked:
                print(f"  {element} → {name}（{rel}，{elem}）")

    # 测试添加案例
    print("\n--- 案例添加 ---")
    case_id = kg.add_case({
        "title": "市场趋势分析",
        "scene": "S4",
        "engine": "五色光思维",
        "output_type": "分析报告",
        "description": "用五色光思维分析市场趋势",
        "linked_engines": ["知识学习", "象思维"],
        "knowledge_graph_tags": ["金生水", "水生木"]
    })
    print(f"  案例已添加: {case_id}")

    # 测试查询
    print("\n--- 查询 ---")
    cases_by_engine = kg.query_by_engine("五色光思维")
    print(f"  按引擎查: {len(cases_by_engine)} 条")

    cases_by_scene = kg.query_by_scene("S4")
    print(f"  按场景查: {len(cases_by_scene)} 条")

    cases_by_element = kg.query_by_element("金")
    print(f"  按五行查: {len(cases_by_element)} 条")

    # 图谱摘要
    print("\n--- 图谱摘要 ---")
    summary = kg.get_graph_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # Mermaid 导出
    print(f"\n--- Mermaid 格式 ---")
    print(kg.export_mermaid())


if __name__ == "__main__":
    main()