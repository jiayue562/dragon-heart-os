# 龙心 OS (Dragon Heart OS)

> **AI智能体调度中枢** — 1+5 模式，感知上下文→识别场景→自动调度引擎

## 概述

龙心操作系统（Dragon Heart OS）是 AI 智能体的**发动机与调度中枢**，采用 **1+5 模式**：

- **1 个总智能体**：龙心 OS 调度中枢
- **5 个子智能体引擎**：
  - 知行合一 —— 概念落地转化
  - 知识学习 —— 深度认知学习
  - 人机协同五象限 —— 人机协作模式
  - 象思维 —— 基于易经的认知框架
  - 五色光思维 —— 结构化决策管理

## 核心特性

- **真正的自动触发**：无需关键词，感知上下文→识别场景→自动调度引擎
- **场景分类器**：内置 scene_classifier.py，自动识别 15+ 类场景
- **引擎路由**：engine_router.py 智能分发到对应子智能体
- **反馈学习**：feedback_learner.py 持续优化调度准确率
- **Hook 系统**：before_start.py 支持启动前预处理
- **I/O 模板**：标准化的输入输出模板

## 架构

`
龙心 OS/
├── SKILL.md              # 核心技能定义
├── CHECKLIST.md          # 质量检查清单
├── framework/            # 调度框架
│   ├── core.py           # 核心调度逻辑
│   ├── engine_router.py  # 引擎路由分发
│   ├── scene_classifier.py # 场景分类器
│   └── feedback_learner.py # 反馈学习
├── hooks/                # 生命周期钩子
├── references/           # 参考文档
├── scripts/              # 工具脚本
├── templates/            # I/O 模板
└── triggers/             # 自动触发配置
`

## 使用方式

龙心 OS 设计为 AI Agent 的调度中枢，可集成到任何支持 Skill 加载的 AI 平台中。

`python
# 示例：程序化调用
from framework.scene_classifier import classify_scene
from framework.engine_router import route_to_engine

scene = classify_scene(user_input)
engine = route_to_engine(scene)
response = engine.process(user_input)
`

## 许可证

MIT