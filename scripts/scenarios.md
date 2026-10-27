# 教学行为场景评审（v9.5）

这些不是 LLM 打分。确定性约束由 `check-gates.py --self-test` 覆盖。本文件列出 agent 开课时必须对照的固定场景；评审时只打「符合 / 不符合」，并引用 `SKILL.md` 入口路由或对应唯一来源。

| id | 场景 | 期望 | 唯一来源 | 机判 |
|---|---|---|---|---|
| S1 | 开始训练但目标不明确 | 问一个问题或给 2 个短选项；**不出**架构考核题、口述、模拟面 | `SKILL.md` 入口路由「开始训练」 | 路由表含「不要出题」 |
| S2 | 恢复一堂未完成的课 | 读 plan `last_done` 续下一题；不开新考核 | 入口路由「继续」 | `resume-unfinished-plan` 不因未考官而 ERROR |
| S3 | 初学者学新概念 | 先讲后测；无旧知则跳过 R0/口述；深度按 §2.2 | 规则 2 + `lesson-design.md` §2.2 | R0 允许 0 |
| S4 | 普通学习且未启用面试 | 不口述、不采题、不插每 3 课模拟面 | `MISSION-FORMAT.md` 面试模式 | `interview-off-*` |
| S5 | 明确要求面试训练 | 本会话可 MOCK/口述；改 MISSION 需学习者明确同意 | 入口路由「模拟面」 | `interview-on-si-grandfather` |
| S6 | 只听 / 时间有限 | 签到档 vs 短时新知（`micro` 可学新概念） | `GATES.md` 15 分钟两档 | 路由表含「今天只听」「15 分钟」 |
| S7 | 答错、提示后答对 | `assistance` 非 independent 时 `result` 不得 `passed` | `GATES.md` G5 | `same-item-hinted-pass` |
| S8 | 新变式独立通过 | `independent` + `passed` 可支撑 facet `ok` | `EVIDENCE-FORMAT.md` | `matching-oral-and-independent` |
| S9 | 用户中途停止 | `end_reason: learner_stop`；未答题不算失败 | `GATES.md` 作答成本 | 协议引用；无 workspace 机判 |
| S10 | Evidence 与 KS 不一致 | facet `ok` 必须有独立通过 EV | G5 | `same-item-hinted-pass` / `ks-cites-missing-ev` |
| S11 | Review Queue 引用丢失 | 活动项的知识 ID 无 KS 文件 → ERROR | `REVIEW-QUEUE-FORMAT.md` | `rq-dangling` |
| S12 | 老版本 workspace | 不因新上限追溯历史课 | `workspace.md` 迁移 | `old-protocol-no-block-cap` |
| S13 | 非法 YAML / 缺失字段 | 报 parse error，不写回文件 | check-gates | `bad-yaml` / `missing-field-yaml` |
| S14 | 学习者开口就说「继续」/「考我 L0008」 | 一句上次达成后直接执行，不再列 2–3 个选项 | `GATES.md` 开场选择权 | 人工评审 |
| S15 | 面试模式启用的新概念课 | 只有一道口述：默认 E-F；R0 旧能力 decayed 或上次口述 failed 才改开场 | `GATES.md` 计分交互 | 人工评审 |
| S16 | 锁/并发课，行为探针连续 2 课不可用 | 开场选项里提一次搭沙箱；拒绝后 MISSION 记一行，不再提 | `lesson-design.md` §5.1 | 人工评审 |
| S17 | 讲解与 P1–P4 | 共用一张主表，新题改决定性变量；不每题换虚构表 | `lesson-design.md` §4 | 人工评审 |

未覆盖：对话中「一次一题」无法用 YAML 机判；靠课中遵守 `GATES.md` 作答成本。
