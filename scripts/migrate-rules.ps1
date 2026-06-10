# 龙心 OS Rule 迁移脚本
# 从项目级迁移到用户全局目录，实现"永远在线，自主运行"

Write-Host "========================================"
Write-Host "  龙心 OS Rule 迁移脚本"
Write-Host "  项目级 → 用户全局目录"
Write-Host "========================================"
Write-Host ""

# 源路径（项目级）
$ProjectRulesPath = "C:\Users\jia'yue\.openclaw\workspace\rules"
# 目标路径（用户全局）
$GlobalRulesPath = "C:\Users\jia'yue\.openclaw\rules"

# 龙心 OS Rule 文件
$DragonHeartRule = "dragonheart-os.md"

Write-Host "源路径（项目级）: $ProjectRulesPath"
Write-Host "目标路径（用户全局）: $GlobalRulesPath"
Write-Host ""

# 创建用户全局 rules 目录
if (-not (Test-Path $GlobalRulesPath)) {
    New-Item -ItemType Directory -Force -Path $GlobalRulesPath | Out-Null
    Write-Host "[OK] 创建用户全局 rules 目录：$GlobalRulesPath"
} else {
    Write-Host "[OK] 用户全局 rules 目录已存在"
}

# 创建项目级 rules 目录（如果不存在）
if (-not (Test-Path $ProjectRulesPath)) {
    New-Item -ItemType Directory -Force -Path $ProjectRulesPath | Out-Null
    Write-Host "[OK] 创建项目级 rules 目录：$ProjectRulesPath"
}

# 创建龙心 OS Rule 文件
$RuleContent = @"
# 龙心 OS Rule - 永远在线，自主运行

> 🐉 龙心操作系统 · 1+5 模式智能体调度中枢

**版本**: v1.0  
**创建**: 2026-04-16  
**作者**: 悟空 × 龙龟  
**类型**: 智能体中枢 Rule

---

## 📋 核心定位

龙心 OS 本质是智能体（生命体），本 Rule 为其全局激活配置。

**核心能力**:
- 自主感知上下文
- 场景识别（S0-S9）
- 自动调度引擎
- 持续学习进化

---

## 🏗️ 1+5 模式架构

### 总智能体：龙心 OS 调度中枢

**功能**: 感知→决策→行动→学习

### 五个子智能体（五大引擎）

| 引擎 | 核心功能 | 激活场景 |
|------|----------|----------|
| **知行合一** | 概念落地转化 | S4/S5 |
| **知识学习** | 十项认知指令深度学习 | S2/S7 |
| **人机协同五象限** | 五模式人机协同 | S0/S1/S5 |
| **象思维** | 观物取象·0→1 原创 | S3/S8 |
| **五色光思维** | 同频思考·过程管理 | S4/S6 |

---

## 🧠 场景识别矩阵（S0-S9）

| 场景 | 类型 | 引擎 | 阈值 |
|------|------|------|------|
| **S0** | 日常对话 | 人机协同 | 0.7 |
| **S1** | 任务执行 | 人机协同 Q1 | 0.8 |
| **S2** | 深度理解 | 知识学习 | 0.8 |
| **S3** | 创意创新 | 象思维 | 0.8 |
| **S4** | 分析决策 | 五色光 + 知行合一 | 0.85 |
| **S5** | 重大决策 | 全引擎协同 | 0.9 |
| **S6** | 会议引导 | 五色光思维 | 0.85 |
| **S7** | 知识编译 | 知识学习+LLM Wiki | 0.8 |
| **S8** | 修行文化 | 象思维 + 五行分类 | 0.8 |
| **S9** | 系统进化 | 龙心 OS 自省 | 0.9 |

---

## 🌲 引擎路由决策树

```
用户输入
    │
    ↓
1. 上下文感知（对话历史/情感/话题）
    │
    ↓
2. 场景识别（S0-S9 分类 + 置信度）
    │
    ↓
3. 引擎调度（单引擎/多引擎/全引擎）
    │
    ↓
4. 执行输出（引擎结果整合）
    │
    ↓
5. 反馈学习（优化路由权重）
```

---

## 🔗 自动触发规则

### 触发模式

- **模式**: scene_recognition（场景识别）
- **场景矩阵**: S0-S9（10 个场景）
- **置信度阈值**: 0.7

### 触发词（P0 直接触发）

```
龙心 OS、龙心操作系统、自动调度、智能路由、场景识别、
引擎调度、1+5 模式、总智能体、子智能体
```

---

## 💬 核心金句

> "龙心 OS 本质是智能体（生命体），本 Rule 包仅为其工程载体和入口。"

> "真正的自动触发不是关键词匹配，而是意图理解 + 场景感知 + 智能路由。"

> "永远在线，自主运行——无论开哪个新对话、哪个新工作区。"

---

_龙心 OS Rule v1.0 · 2026-04-16 · 智能体中枢_
"@

$RuleFilePath = Join-Path $GlobalRulesPath $DragonHeartRule
$RuleContent | Out-File -FilePath $RuleFilePath -Encoding utf8 -Force

Write-Host "[OK] 创建龙心 OS Rule 文件：$RuleFilePath"
Write-Host ""

# 同时复制到项目级（向后兼容）
$ProjectRuleFilePath = Join-Path $ProjectRulesPath $DragonHeartRule
$RuleContent | Out-File -FilePath $ProjectRuleFilePath -Encoding utf8 -Force
Write-Host "[OK] 创建项目级 Rule 文件（向后兼容）：$ProjectRuleFilePath"
Write-Host ""

Write-Host "========================================"
Write-Host "  迁移完成"
Write-Host "========================================"
Write-Host ""
Write-Host "龙心 OS Rule 已部署到："
Write-Host "  1. 用户全局目录：$GlobalRulesPath"
Write-Host "  2. 项目级目录：$ProjectRulesPath（兼容）"
Write-Host ""
Write-Host "现在龙心 OS 真正做到了："
Write-Host "  ✅ 永远在线"
Write-Host "  ✅ 自主运行"
Write-Host "  ✅ 无论开哪个新对话、哪个新工作区"
Write-Host ""
