# 龙心 OS 架构指南

> framework/ 目录对应代码架构说明

## 三层架构

`
概念层（概念澄清）
  ├── 声明：龙心 OS 本质是智能体（生命体）
  └── 区分"智能体" vs "普通 Skill"

架构层（Framework 突破）
  ├── core.py              — 核心调度循环（感知→决策→行动）
  ├── scene_classifier.py  — S0-S9 场景分类器
  ├── engine_router.py     — 引擎路由决策
  └── feedback_learner.py  — 反馈学习与优化

载体层（Skill 结构）
  ├── triggers/            — 自动触发配置
  ├── templates/           — 输出模板
  └── scripts/             — 运维脚本
`

## 核心文件说明

| 文件 | 功能 | 关键类/函数 |
|------|------|-------------|
| ramework/core.py | 核心调度循环 | schedule_loop(), perceive(), decide(), ct() |
| ramework/scene_classifier.py | S0-S9 场景分类 | classify(context) -> (scene, confidence) |
| ramework/engine_router.py | 引擎路由分配 | oute(scene, context) -> [engine_ids] |
| ramework/feedback_learner.py | 反馈学习 | learn(feedback), optimize_routing() |

## 数据流

`
用户输入
  → perceive()     [context, sentiment, topic]
    → classify()   [S0-S9 + confidence]
      → route()    [engine list + priority]
        → execute() [engine output]
          → present() [integrated response]
            → learn() [feedback → optimize]
`
"@ | Set-Content -LiteralPath "C:\Users\jia'yue\.agents\skills\龙心 OS\references\architecture-guide.md" -Encoding UTF8

# 2. scene-classification-guide.md
@"
# 场景分类指南（S0-S9）

## 分类依据

| 维度 | 说明 | 取值 |
|------|------|------|
| 任务复杂度 | 是否需要多步推理 | 低/中/高 |
| 情感强度 | 用户情绪卷入程度 | 0-10 |
| 确定性 | 用户是否明确需求 | 清晰/模糊/未知 |
| 创造性 | 是否需要原创输出 | 否/是/高度 |

## S0-S9 快速判断表

| 代码 | 场景 | 关键信号 | 置信度要求 |
|:----:|------|---------|:---------:|
| S0 | 日常对话 | 问候、闲聊、简单问答 | >= 0.7 |
| S1 | 任务执行 | 帮我/写/做/发 | >= 0.8 |
| S2 | 深度理解 | 深度学习/分析这篇文章 | >= 0.8 |
| S3 | 创意创新 | 本质/根源/原创/突破 | >= 0.8 |
| S4 | 分析决策 | 方案/决策/选择/评估 | >= 0.85 |
| S5 | 重大决策 | 人生/重大/关键选择 | >= 0.9 |
| S6 | 会议引导 | 会议/讨论/团队/效率 | >= 0.85 |
| S7 | 知识编译 | Wiki/编译/知识库 | >= 0.8 |
| S8 | 修行文化 | 心文化/大圆满/修行 | >= 0.8 |
| S9 | 系统进化 | 错误/优化/学习/自省 | >= 0.9 |

## 多引擎协同规则

| 场景 | 激活引擎 | 协同模式 |
|------|----------|----------|
| S4 | 五色光 + 知行合一 | 串行：先分析，后转化 |
| S5 | 全引擎 | 并行 + 整合 |
| S7 | 知识学习 + LLM Wiki | 串行：理解后编译 |
| S8 | 象思维 + 五行分类 | 并行：右脑+左脑 |
