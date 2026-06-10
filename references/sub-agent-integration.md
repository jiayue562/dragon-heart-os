# 五大子智能体集成指南

## 调度协议

每个子智能体 Skill 必须实现以下接口：

`
trigger_conditions:  # 触发条件列表
  - trigger: "关键词/模式"
    scene: "所属 S 场景"
    action: "执行动作描述"
  - trigger: "..."
    scene: "..."
    action: "..."

output_format:  # 输出格式
  - type: "Markdown/JSON/Text"
  - structure: "核心输出结构"
`

## 注册流程

1. 子智能体 Skill 放在 ~/.agents/skills/ 下
2. 在 frontmatter 中声明 parent_skill: 龙心 OS
3. 在 sub_skills: 中添加
4. 在场景识别矩阵中添加对应 S 代码

## 当前注册的子智能体

| Skill | 场景 | 触发模式 |
|-------|------|----------|
| 知行合一 | S4/S5 | 自动调度 |
| 知识学习 | S2/S7 | 自动调度 |
| 人机协同五象限 | S0/S1/S5 | 自动调度 |
| 象思维 | S3/S8 | 自动调度 |
| 五色光思维 | S4/S6 | 自动调度 |
