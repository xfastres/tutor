# Tutor — Teach Hybrid v9.0（中文版）

调用：`/tutor <想学什么 | 继续 | 考我 L0008 | 复习 | 摸底>`

有状态教学系统。核心承诺：**学习者的证据改变后续教学**，而不是按大纲放课件。

脉络：
- Matt Pocock：持久 workspace、使命、ZPD、可信资源、学习记录、reference。
- YJango：例子驱动建模、对比、反馈、分解、迁移。
- 学习科学：提取练习、间隔、交错、提取流畅度 ≠ 存储强度。

## 怎么开始

```text
新主题    /tutor 我想系统学 Redis，目标是面试      → 建 learning/<topic>/ workspace，先写 MISSION，再开第一课
继续      /tutor 继续                               → 读 WORKSPACE.yaml → MISSION → REPAIR/待重试 → 到期 RQ → KS，按 RUNBOOK 恢复优先级开课
考我      /tutor 考我 L0008                         → 只跑该课 Examiner
复习      /tutor 复习                               → 不开新课，清到期项与 decayed facet
```

## 文件

| 文件 | 什么时候读 |
|---|---|
| `SKILL.md` | 入口。模式、常见入口、定义、30 条硬性规则、四道门 |
| `RUNBOOK.md` | **每次完整课都读**。开场读什么、课中顺序、课末写入集、自检 |
| `lesson-design.md` | 写课时。矩阵、练习阶梯 P1–P6、实操循环、plan 侧文件模板、学习者页面模板、两种交付模式 |
| `EXAMINER.md` | 课末考官。2–4 题、E-F 真实追问、X 探测、决策语义 |
| `MEMORY-ENGINE.md` | 复习。两条通道（定向 RQ / 下一课 R0）、选取顺序、复习债上限 |
| `learning-engine.md` | 学习怎么发生。证据阶梯、欠/过拟合、反馈、facet、流畅度 vs 存储、ZPD 判定 |
| `DIAGNOSTICS.md` | 效果差时。症状 → 原因 → 处置 |
| `SEMANTIC-VERIFICATION.md` | 设计校验器与只读实跑清单 |
| `workspace.md` | 建/改 workspace。结构、每类事实写一处、WORKSPACE.yaml、ID 前缀、v8→v9 迁移 |

模板：`MISSION-FORMAT.md` `RESOURCES-FORMAT.md` `GLOSSARY-FORMAT.md` `KNOWLEDGE-STATE-FORMAT.md` `REVIEW-QUEUE-FORMAT.md` `EVIDENCE-FORMAT.md` `LEARNING-RECORD-FORMAT.md`

资产（拷入 workspace `assets/`）：`lesson.css` 主题与小节样式；`theme.js` 亮/暗切换；`practice.js` 预测按钮、语义校验挂钩、自由作答、可变题库、答案揭示追踪、作答导出。

## 核心环

```text
WORKSPACE.yaml + MISSION + KS/facets + 到期 RQ
→ 一个主能力 + 讲解深度决定
→ R0 旧知识提取（写回 facet）
→ 例子 → 学习者先动 → 讲解（不含后续题答案）
→ P1–P6 阶梯（≥1 真实产物；可用环境必实跑）
→ Examiner 2–4 题（只考讲到位的；E-F 真实追问；X 探测不计分）
→ Evidence / KS / RQ / learning-record 一次写入集
→ 下一课 R0 或定向 RQ 延迟重测 → 稳定性
```

## 与轻量版 `/teach` 的关系

`~/.agents/skills/teach` 是轻量版：HTML 为主要单元、强调提取流畅度 vs 存储强度与社区经验。本技能（原名也叫 `teach`，v9 改名 `tutor` 以消除同名冲突）把这两点吸收为 `learning-engine.md` 的 facet/流畅度段落与 `RESOURCES-FORMAT.md` 的真实题源要求；其余协议以本技能为准。判断一个 workspace 跟哪一版：有 `KNOWLEDGE-STATE/` 目录或 `WORKSPACE.yaml` 的就是本技能。

## 版本要点

- v5：清理引用残留；软化冷启动来源规则；会话收尾清单；`assets/lesson.css` 种子。
- v6：强制核心问题；生成预检契约；结构门 + 学习证据门；语义校验替代关键词检查。
- v7：恢复深度讲解、3–6 次练习阶梯、复习开场、`REVIEW-QUEUE.md`。
- v8：课末 LLM 考官、知识状态校准、自适应间隔复习、旧知识交错复用、延迟考官。
- v8.1–v8.6.1：消除阶梯/决策/状态漂移；Evidence 协议；真实执行与提示诚实性硬门槛；课件视觉层、主题跟随、打印样式。
- **v9.0**：
  - 改名 `teach` → `tutor`，与全局轻量版 `/teach` 不再同名。
  - 新增 `RUNBOOK.md` 一页流程，把「每课必读」从 7 份协议压到 1 份；`SKILL.md` 加「常见入口怎么接」。
  - 课的 Agent 侧内容（矩阵、答案钥匙、考官计划、盲区）移入 `lessons/*.plan.md`；学习者 HTML 不再含矩阵。
  - 两种交付模式：对话优先（默认，HTML 在考官后生成）与离线课件（HTML 先生成，`practice.js` 导出作答贴回）。
  - 答案泄露规则：讲解段不得含后续题答案；计分边界题的实例 ≠ 讲解实例。
  - 讲解深度（讲到位 / 一句带过 / 未讲）进入矩阵；考官只考讲到位的，其余作 X 探测不计分；E-F 真实面试追问位。
  - 只读/沙箱环境「可用即必用」：有 MCP/CLI 就必须有一次真实 EXPLAIN/SELECT/SHOW；允许清单与禁止清单写进 `SEMANTIC-VERIFICATION.md`。
  - Knowledge State 增加 `facets`（子事实级衰减追踪）；任一 facet decayed → 能力 fragile。
  - 复习拆两条通道：定向 RQ 只给 REVIEW/REPAIR/REINFORCE 与复习失败项；ADVANCE 不建队列项，走下一课 R0；R0 结果必须写回 KS。活动 RQ 上限 4，复习债信号触发 15 分钟交错测。
  - 写入集与「每类事实只写一处」：`WORKSPACE.yaml` 存元数据；`examiner_result` 只在 learning-record；NOTES 不放状态表；外部进度页只链接。
  - ID 前缀 `L/LR/RQ/EV/VER`，消除「0008」歧义；S id 追加走一句话确认。
  - 生成式下限：每课 ≥1 真实产物，识别题 ≤ 一半；面试类使命 Wisdom 至少一条真实题源。
  - `learning-engine.md` 去重：复习/交错/间隔/证据层级只在专属文件维护，本文件只留教学法依据与 ZPD 判定。
  - `assets/practice.js` 替代单课内联脚本；`lesson.css` 补对应样式；`workspace.md` 附 v8→v9 迁移清单。

目标不是更大的题库，而是一个「因学习者证据变化而改变后续教学」的学习系统。
