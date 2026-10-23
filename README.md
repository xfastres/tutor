# Tutor — Teach Hybrid v9.4（中文版）

调用：`/tutor <想学什么 | 继续 | 开始训练 | 考我 L0008 | 复习 | 摸底 | 模拟面 | 今天只听 | 15 分钟>`

## 安装到任何 agent

skill 就是这个目录，没有运行时依赖（机判脚本可选，需要 Python 3）。不同 agent 扫描的目录不同，用脚本把本目录**链接**过去，一份源码所有 agent 共用：

```text
Windows        powershell -ExecutionPolicy Bypass -File scripts/install.ps1   [-Cursor] [-Project <项目路径>] [-Uninstall]
macOS / Linux  bash scripts/install.sh                                         [--cursor] [--project DIR] [--uninstall]
```

默认链接到 `~/.agents/skills/tutor`（Cursor、Codex 及读 `.agents/skills` 的 agent）、`~/.claude/skills/tutor`（Claude Code）、`~/.codex/skills/tutor`（Codex CLI）。`-Project` 再加到项目级 `.agents/skills` 与 `.claude/skills`。卸载只删链接，不碰真实目录。

- 调用：`/tutor 继续`；没有斜杠命令的 agent 说「用 tutor skill，继续」。
- agent 没列出这个 skill（目录没被扫描）：把路径直接给它——「读 `<skill 路径>/SKILL.md`，按 RUNBOOK 开课，workspace 在 `<项目>/learning/<topic>`」。skill 只是 markdown，能读文件就能用。
- workspace 默认在当前目录 `learning/<topic>/`；跨目录时设环境变量 `TUTOR_WORKSPACE`，或在对话里说路径。
- `disable-model-invocation: true`：只能由你调用，agent 不会在无关对话里自动套用它。

有状态教学系统。核心承诺：**学习者的证据改变后续教学**，而不是按大纲放课件。

v9.1 的一句话：**先讲明白，再练到会，最后考到稳；用真实面试题检验，用旧知识螺旋巩固。**

脉络：
- Matt Pocock：持久 workspace、使命、ZPD、可信资源、学习记录、reference。
- YJango：例子驱动建模、对比、反馈、分解、迁移。
- 学习科学：提取练习、间隔、交错、提取流畅度 ≠ 存储强度。
- v9.1 补上：讲解块（先讲后测）、真实面试题管线、旧知识螺旋复用、五道门。

## 怎么开始

```text
新主题    /tutor 我想系统学 Redis                   → 建 workspace，先写 MISSION；面试模式默认关
面试目标  /tutor 我想系统学 Redis，目标是面试       → 同上，并按 MISSION-FORMAT 启用面试模式
继续      /tutor 继续                               → 恢复未完成课；开场给选项
开始训练  /tutor 开始训练                           → 无主题：问「学什么」或给选项，不出考核题
考我      /tutor 考我 L0008                         → 本会话 Examiner；不改 MISSION
复习      /tutor 复习                               → 不开新课，清到期项与 decayed facet
模拟面    /tutor 模拟面                             → 本会话 MOCK；长期开启需明确改 MISSION
```

## 文件

| 文件 | 什么时候读 |
|---|---|
| `SKILL.md` | 入口路由（唯一定义）、课型、规则索引 |
| `RUNBOOK.md` | **完整课**才读。开场、课中顺序、写入集 |
| `GATES.md` | **五道门判据的唯一来源**；计分交互、作答成本、15 分钟两档 |
| `scripts/check-gates.py` | 结课前只读机判。`--self-test` 含入口契约与面试启用 |
| `scripts/scenarios.md` | 教学行为场景评审清单（不是 LLM 打分） |
| `scripts/install.ps1` / `install.sh` | 把本目录链接进各 agent 的 skills 目录；`-Uninstall` 只删链接 |
| `lesson-design.md` | 写课时。§2.2 教学深度（唯一来源）、矩阵、练习阶梯 |
| `EXAMINER.md` | 课末考官。题量按深度；E-F 仅面试模式启用 |
| `INTERVIEW-BANK-FORMAT.md` | 仅面试模式启用时读 |
| `MEMORY-ENGINE.md` | 复习。两条通道、模拟面、螺旋复用、复习债上限 |
| `learning-engine.md` | 学习怎么发生。证据阶梯、欠/过拟合、反馈、facet、流畅度 vs 存储、ZPD 判定 |
| `DIAGNOSTICS.md` | 效果差时。症状 → 原因 → 处置（含「全是题没讲解」「面试讲不出」） |
| `SEMANTIC-VERIFICATION.md` | 设计校验器与只读实跑清单 |
| `workspace.md` | 建/改 workspace。结构、每类事实写一处、WORKSPACE.yaml、ID 前缀、迁移 |

模板：`MISSION-FORMAT.md` `RESOURCES-FORMAT.md` `GLOSSARY-FORMAT.md` `KNOWLEDGE-STATE-FORMAT.md` `REVIEW-QUEUE-FORMAT.md` `EVIDENCE-FORMAT.md` `LEARNING-RECORD-FORMAT.md` `INTERVIEW-BANK-FORMAT.md`

资产（拷入 workspace `assets/`）：`lesson.css` 主题与小节样式；`theme.js` 亮/暗切换；`practice.js` 预测按钮、语义校验挂钩、自由作答、可变题库、答案揭示追踪、作答导出。

## 核心环

```text
入口路由（SKILL.md）分流意图
→ 有 workspace：开场选项；无主题：问一个问题，不出考核题
→ 定课型 + 教学深度 + 预算（15 分签到 / 15 分短时新知 / 30 / 45 / 60）
→ 面试模式未启用：不口述、不采题、不插模拟面
→ 新概念：先讲后测（深度档）→ 独立验证 → 按深度考官
→ 课末一次写入 evidence / KS / RQ / LR
```

## 与轻量版 `/teach` 的关系

`~/.agents/skills/teach` 是轻量版：HTML 为主要单元、强调提取流畅度 vs 存储强度与社区经验。本技能（原名也叫 `teach`，v9 改名 `tutor` 以消除同名冲突）把这两点吸收为 `learning-engine.md` 的 facet/流畅度段落、`RESOURCES-FORMAT.md` 的真实题源要求与 `INTERVIEW-BANK-FORMAT.md` 的题库管线；其余协议以本技能为准。判断一个 workspace 跟哪一版：有 `KNOWLEDGE-STATE/` 或 `WORKSPACE.yaml` 的就是本技能。

## 版本要点

- v5：清理引用残留；软化冷启动来源规则；会话收尾清单；`assets/lesson.css` 种子。
- v6：强制核心问题；生成预检契约；结构门 + 学习证据门；语义校验替代关键词检查。
- v7：恢复深度讲解、3–6 次练习阶梯、复习开场、`REVIEW-QUEUE.md`。
- v8：课末 LLM 考官、知识状态校准、自适应间隔复习、旧知识交错复用、延迟考官。
- v8.1–v8.6.1：消除阶梯/决策/状态漂移；Evidence 协议；真实执行与提示诚实性硬门槛；课件视觉层、主题跟随、打印样式。
- v9.0：改名 `teach`→`tutor`；RUNBOOK 一页化；对话优先；plan 侧文件；讲解深度/讲解段落；只读实操「可用即必用」；facet 衰减；复习双通道；写入集。
- **v9.1（本次）**：
  - **讲解优先**：课型二分（新概念课先讲后测 / 练习复习课先测后讲）；新增「讲解块」7 元素契约（400–800 字、位于任何计分题之前、每段夹案例/对照）；新增 **G2 讲解门**；「不生成文字墙」改写为「不得压缩讲解、也不得写纯理论长篇」。
  - **反题海**：计分交互只以 `GATES.md` 为准（一个教学块 ≤6，计划时最多先排 5 个），考官 2–3 题、不再一题拆 b/c/d 多轮；RQ 普通项不挤占新概念课；讲不清 / 讲太少按 DIAGNOSTICS 处置。
  - **面试管线**：新增 `INTERVIEW-BANK-FORMAT.md` 与 `INTERVIEW-BANK.md`；每课末采集 2–4 道真实面试题（来源 URL + 可信度 + 关联 S/facet）；面试线未写「不适用」时，下节课 1 道 60 秒四段口述（结论→原因→边界→例子）；每 3 课一次模拟面；崩题回流 `REPAIR：`；新增 `type: interview` 证据与 `expression` 维度。写「不适用」则不排每课口述和 E-F。
  - **螺旋复用**：矩阵新增「复用旧知」行；P5 必须嵌入旧能力；旧 KS 的 `used_in` 回写；每 3 课模拟面混合旧新。
  - **五道门**：四道门扩为结构/讲解/练习/考官/证据五道，判据、落盘产物、不过处置统一到 `GATES.md`；plan 增加 `课型 / teaching_block / 预算 / 门记录 / 复用旧知`。
  - **记账瘦身**：证据改为一课一文件 `evidence/LNNNN.yaml`（课末一次写，不再每答一题写一次）；`attempts` 降级、`verification_ref` 仅 execution 必填；plan 答案钥匙加「必须点/常见半对/失败模式」。
  - **交付**：HTML 拆「讲解页（可课前，无答案）」与「复习页（考官后，含真实错误）」；对话优先时讲解块必须在对话里出现。
  - 迁移：`workspace.md` §「从 v9.0 迁移到 v9.1」。
- **v9.1.1**：不改课型。收口 jobs四审计里的冲突与逃逸：口述 `result` 只以 `EVIDENCE-FORMAT.md` 为准（没追问最高 `partial`）；模拟面固定 5 题，已用-崩「有则必含、没有不阻断」；`decayed` facet 先于今日前置，开场口述考同一条；G2 禁止讲解说死计分题结论；G5 增加六条机判失败（含同题订正不得 `passed`、facet `ok` 必须有独立证据）；官方源不可达时不新增计分题。
- **v9.1.2**：计分交互只以 `GATES.md` 为唯一定义（一个教学块 ≤6，计划时最多先排 5 个给重试留位，重试不可取消）；其他文件不再另写一套数字。面试线写「不适用」时不排每课口述和 E-F。新增只读机判 `scripts/check-gates.py`。
- **v9.4**：教学优先于考核。入口路由区分继续/新主题/模糊「开始训练」/轻量/考我/模拟面；没有主题先问一个问题，不出高级考核题。面试模式改为显式启用（默认关；已有 `S-I*` 的旧 workspace 保持开）。教学深度 `micro|standard|deep`；15 分钟分签到与短时新知（允许范围合适的新概念）。计分上限不是配额。按入口按需读文档。
- **v9.3**：让人愿意回来。`GATES.md` 新增「开场、选择与收尾」唯一定义：先赢后债（开场先说上次达成，债务只是选项之一）、开场 2–3 个带分钟数的选项、真实上下文优先（`MISSION.md` 新增「真实上下文」一节，案例 A / P5 / E1 取学习者自己的代码和表）、不计分开胃预测、15 分钟档（来了就算）、结尾高点（最难题放中间）、成长叙事收尾、不催促。新增 `scripts/install.ps1` / `install.sh`：一键链接到 `~/.agents`、`~/.claude`、`~/.codex` 的 skills 目录，任何 agent 可用。
- **v9.2**：把学习者的作答成本当成要管理的资源。`GATES.md` 新增「作答成本与反馈」唯一定义：一次一题、题面过线行（判分只按它）、机制题短句过线（四段只用于面试口述）、对的立刻记过、同一缺口只 1 次新变式且重试前先 ≤200 字补救、追问当轮完成、开场不泄题、收尾第一句是达成项、学习者喊停不记负面、规则改版不追溯。G5 新增「系统失误修正」：记账错误改单条 EV（`corrected` 块）并告知一句，不转学习者重测。RUNBOOK 不再携带任何工作区状态。

目标不是更大的题库，而是一个「因学习者证据变化而改变后续教学」的学习系统——**并且每节课都真的把东西讲明白。**
