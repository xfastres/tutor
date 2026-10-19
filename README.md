# Tutor — Teach Hybrid v9.1（中文版）

调用：`/tutor <想学什么 | 继续 | 考我 L0008 | 复习 | 摸底 | 模拟面>`

有状态教学系统。核心承诺：**学习者的证据改变后续教学**，而不是按大纲放课件。

v9.1 的一句话：**先讲明白，再练到会，最后考到稳；用真实面试题检验，用旧知识螺旋巩固。**

脉络：
- Matt Pocock：持久 workspace、使命、ZPD、可信资源、学习记录、reference。
- YJango：例子驱动建模、对比、反馈、分解、迁移。
- 学习科学：提取练习、间隔、交错、提取流畅度 ≠ 存储强度。
- v9.1 补上：讲解块（先讲后测）、真实面试题管线、旧知识螺旋复用、五道门。

## 怎么开始

```text
新主题    /tutor 我想系统学 Redis，目标是面试      → 建 learning/<topic>/ workspace，先写 MISSION（含面试线），再开第一课
继续      /tutor 继续                               → 读 WORKSPACE → MISSION → 课型判定 → plan → 面试口述 → RQ，按 RUNBOOK 恢复优先级开课
考我      /tutor 考我 L0008                         → 只跑该课 Examiner（面试类含 E-F）
复习      /tutor 复习                               → 不开新课，清到期项与 decayed facet
模拟面    /tutor 模拟面                             → 题库 + RQ 崩题抽题，计时无提示，输出报告
```

## 文件

| 文件 | 什么时候读 |
|---|---|
| `SKILL.md` | 入口。课型、规则、五道门 |
| `RUNBOOK.md` | **每次完整课都读**。开场、课型、课中顺序、写入集、面试题采集 |
| `GATES.md` | **五道门判据的唯一来源**：结构/讲解/练习/考官/证据 |
| `lesson-design.md` | 写课时。讲解块、矩阵、练习阶梯、样例→补全→独立、plan 模板、两种页面 |
| `EXAMINER.md` | 课末考官。2–3 题、E-F 面试追问、X 探测、决策语义 |
| `INTERVIEW-BANK-FORMAT.md` | 题库格式与采集/使用协议（课后入库、下节课口述、模拟面） |
| `MEMORY-ENGINE.md` | 复习。两条通道、模拟面、螺旋复用、复习债上限 |
| `learning-engine.md` | 学习怎么发生。证据阶梯、欠/过拟合、反馈、facet、流畅度 vs 存储、ZPD 判定 |
| `DIAGNOSTICS.md` | 效果差时。症状 → 原因 → 处置（含「全是题没讲解」「面试讲不出」） |
| `SEMANTIC-VERIFICATION.md` | 设计校验器与只读实跑清单 |
| `workspace.md` | 建/改 workspace。结构、每类事实写一处、WORKSPACE.yaml、ID 前缀、迁移 |

模板：`MISSION-FORMAT.md` `RESOURCES-FORMAT.md` `GLOSSARY-FORMAT.md` `KNOWLEDGE-STATE-FORMAT.md` `REVIEW-QUEUE-FORMAT.md` `EVIDENCE-FORMAT.md` `LEARNING-RECORD-FORMAT.md` `INTERVIEW-BANK-FORMAT.md`

资产（拷入 workspace `assets/`）：`lesson.css` 主题与小节样式；`theme.js` 亮/暗切换；`practice.js` 预测按钮、语义校验挂钩、自由作答、可变题库、答案揭示追踪、作答导出。

## 核心环

```text
WORKSPACE.yaml + MISSION(含面试线) + KS/facets + 到期 RQ + 面试题库
→ 定课型（NEW_CONCEPT / PRACTICE / REVIEW / MOCK）
→ 开场：R0（新概念≤1）+ 1 道 60 秒面试口述（题库）
→ 新概念课：讲解块（7 元素，400–800 字）→ 完整样例 → 补全 → 独立 → 边界/迁移(嵌入旧知) → 实操
→ 考官 2–3 题（只考讲到位；面试类 E-F 必选）
→ 课末一次写入：evidence/LNNNN.yaml、KS、RQ、LR、plan gates、面试题库
→ 课后 5 分钟：检索真实面试题 2–4 道入库
→ 下节课 R0/口述取用；每 3 课模拟面；崩题回流 RQ
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
  - **反题海**：每课计分交互 ≤6（R0≤1、P≤3、E≤3），考官 2–3 题、不再一题拆 b/c/d 多轮；RQ 普通项不挤占新概念课；讲不清 / 讲太少按 DIAGNOSTICS 处置。
  - **面试管线**：新增 `INTERVIEW-BANK-FORMAT.md` 与 `INTERVIEW-BANK.md`；每课末采集 2–4 道真实面试题（来源 URL + 可信度 + 关联 S/facet）；下节课 1 道 60 秒四段口述（结论→原因→边界→例子）；每 3 课一次模拟面；崩题回流 `REPAIR：`；新增 `type: interview` 证据与 `expression` 维度。
  - **螺旋复用**：矩阵新增「复用旧知」行；P5 必须嵌入旧能力；旧 KS 的 `used_in` 回写；每 3 课模拟面混合旧新。
  - **五道门**：四道门扩为结构/讲解/练习/考官/证据五道，判据、落盘产物、不过处置统一到 `GATES.md`；plan 增加 `课型 / teaching_block / 预算 / 门记录 / 复用旧知`。
  - **记账瘦身**：证据改为一课一文件 `evidence/LNNNN.yaml`（课末一次写，不再每答一题写一次）；`attempts` 降级、`verification_ref` 仅 execution 必填；plan 答案钥匙加「必须点/常见半对/失败模式」。
  - **交付**：HTML 拆「讲解页（可课前，无答案）」与「复习页（考官后，含真实错误）」；对话优先时讲解块必须在对话里出现。
  - 迁移：`workspace.md` §「从 v9.0 迁移到 v9.1」。

目标不是更大的题库，而是一个「因学习者证据变化而改变后续教学」的学习系统——**并且每节课都真的把东西讲明白。**
