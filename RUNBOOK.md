# 运行手册（一页）v9.1.1

每次完整课按本页走。本页只列动作与读写清单；判据以 `GATES.md` 为唯一来源，规则细节在各专属文件。

## 1. 开场：读（按序，只读需要的）

```text
0. WORKSPACE.yaml                   timezone、protocol、platform、last_ev（pending 则先过 workspace.md 迁移清单）
1. MISSION.md                       使命、S id、目标环境、面试线（S-I*）、只读/沙箱环境
2. plan（本课或续课）                课型、teaching_block、gates、进度行、待重试
3. learning-records/ 最近 1–2 条     上一次的 Decision 与 Implications
4. KNOWLEDGE-STATE/<目标与前置>.yaml  status、stability、facets、misconceptions、used_in、review_ref
5. INTERVIEW-BANK.md                取 1 道下节课口述题（优先上次课/弱 facet）；看有没有崩题待回流
6. REVIEW-QUEUE.md                  先找 `REPAIR：` 项（不看日期），再看 due / 近 3 天 / deferred 到期
7. RESOURCES.md 相关条目             要教的事实有没有来源；面试类使命看 Wisdom；Probes 三类探针可用否
8. 工具                              配置/状态类只读探针能跑就必跑；行为类只在沙箱
```

不盲扫整个 workspace。`MISSION.md` 不存在时按 `MISSION-FORMAT.md` 只问影响计划的信息。

**恢复优先级**（每段会话开始都过一遍；进度以 plan「进度」行为准，不凭聊天记录猜）：

```text
① `REPAIR：` 项与「待重试」   不看到期日。是今天内容的前置 → 没过不开新内容
② 上次课未完成的任务          从 last_done 下一题续。续课的新会话先重跑本段，再续题
③ decayed facet               先于到期 RQ；新概念课的 1 个 R0 名额用在这里
④ 到期 RQ                     当次做掉，或按 REVIEW-QUEUE-FORMAT 记去向（普通 RQ 不挤占新概念课）
⑤ 新内容
```

## 2. 决定（先定课型，再定内容）

```text
课型       NEW_CONCEPT | PRACTICE | REVIEW | MOCK
主能力     唯一；对应一个 S id（没有就按 MISSION-FORMAT 追加一条并在对话确认）
交付模式   对话优先（默认）| 讲解页（课前，无答案）| 复习页（考官后）| 离线课件（必须导出作答）
预算       30 / 45 / 60 分钟三档（按当天实际选一档，写进 plan）
讲解块     新概念课必写：7 元素 + 400–800 字 + 2–3 段 + 每段夹案例
R0         新概念课 ≤1 项；练习/复习课 1–3 项。选取顺序见 MEMORY-ENGINE
面试口述   每课开场 1 题（60 秒，四段评分），来自 INTERVIEW-BANK
实操       使命含运行/排查且只读环境可用 → 本课必含一次实跑
计分上限   R0≤1 + 开场口述 1 + P≤3 + E≤3，总数 6 为硬顶；X 探测不计；普通 RQ 不进新概念课
```

## 3. 写课前：plan 侧文件（结构门 G1）

写 `lessons/NNNN-slug.plan.md`（模板见 `lesson-design.md` §12.3），必须包含：

```text
课型 / 能力 / capability_id / 使命标准 S id / 核心问题 / 前置 KS
R0：1 项（新概念）或 1–3 项（练习复习）
交付模式 / 预算 / 环境与探针三类可用否
teaching_block：段落标题 + 7 元素 checklist + 覆盖的矩阵项（新概念课必填）
覆盖矩阵：含讲解深度、讲解段落、复用旧知（旧能力 + 用途）、边界、实操、盲区
任务与答案钥匙：含新增维度、必须点/常见半对/失败模式
考官计划：2–3 计分题 + X 探测；面试类使命含 E-F（题库题号）
门：G1..G5 记录位（未过写原因与处置）
进度：last_done | 待重试 | 考官
```

学习者页面（讲解页/复习页）里不放矩阵、答案钥匙、考官计划。

## 4. 课中（按课型）

**A. 新概念课（先讲后测，默认）**

```text
1. R0（≤1 题，只考旧知）→ 结果回写旧条目
2. 面试口述（60 秒，考 R0 那条旧能力；有 decayed facet 就考它。计入 G3 上限）→ 按 EVIDENCE-FORMAT 定 result，source 写 review
3. 讲解块（7 元素；首题之前必须发出；含案例 A 与反例 B）
4. 完整样例：老师带做一遍，逐步讲为什么（§5.3）
5. 局部补全：挖掉一个机制让学习者补
6. 独立：无提示、生成式使命要产出真实产物（P3）
7. 边界/迁移：换实例/换业务，迁移任务嵌入一个旧能力（P4/P5，矩阵「复用旧知」行）
8. 实操（可用时）：预测 → 执行只读动作 → 保存原始结果 → 解释 → 改一个条件再执行
9. 考官：2–3 题（新表面，只考讲到位；面试类含 E-F）
10. 课末：写入集一次完成 + 5 分钟面试题采集
```

**B. 练习/复习课（先测后讲）**

```text
1. R0/RQ（1–3 题）→ 变式练习 → 诊断 → 最小补讲
2. 发现新能力缺口 → 转 NEW_CONCEPT 或 REPAIR，不硬凑
3. 考官 2–3 题 + X 探测；写入集同 A
```

**C. MOCK 模拟面**

```text
按 MEMORY-ENGINE 抽 5 题（旧:新 ≈ 2:1，三类各至少 1；已用-崩有则必含）→ 计时 60–120 秒 → 追问 → 按 EVIDENCE-FORMAT 定 result → 报告
```

**反馈与修复**

- 反馈层级：现象 → 机制 → 模型 → 下一动作（`lesson-design.md` §12.1）；先不给答案。
- 提示分级：概念混淆→对照案例；执行错误→给骨架；边界遗漏→单变量反例；同题最多 2 级，第 3 级直接揭示并触发 P6。
- P6（答案暴露/强提示/关键错误后）：换业务情境或关键条件、无提示重试；P6 失败不再逐条揭示：并排对比 → 补全 → 新变形；再失败停本课新题，进 REPAIR。
- 「待重试」未清：不进依赖它的新能力；考官必须含 E-repair。
- **每完成一个 task 更新 plan 进度行；文件写入留到课末批量做**，不每答一题写一次。

## 5. 课末：考官（G4）

2–3 个计分题 + 可选 X 探测（不计分、不计入题数），新表面，按矩阵采样，只计分「讲到位」项；「一句带过」项只作 X 探测。面试/考核类使命必须含 1 题真实追问（E-F，来自 INTERVIEW-BANK），按四段评分。解释题要结论 + 原因，只给结论记 `partial`。决策五选一（语义见 `EXAMINER.md`），写进 learning-record 的 `examiner_result`（含 `covered_points`）。

## 6. 课后 5 分钟：面试题采集（R20）

```text
1. 检索 2–3 次：中文「<主题> 面试题 / 面经」+ 英文「<topic> interview questions」
2. 筛选 2–4 题：命中本课 capability/facet 或已知弱 facet；难度匹配目标档位（如 15–18k PHP 后端）
3. 核对来源：官方文档/权威题库优先；不确定标 unverified，不判分
4. 写入 INTERVIEW-BANK.md：题面摘要、来源 URL、可信度、关联 S/facet、类型(knowledge/project/hr)、状态「未用」
5. 同一题不重复入库；不复制大段原文
```

## 7. 写入集（每课固定，课末一次完成）

**必写**

| 文件 | 内容 |
|---|---|
| `evidence/LNNNN.yaml` | 本课所有改变判断的证据：R0、面试口述、P、E、实操；一课一文件，含 lesson_id |
| `KNOWLEDGE-STATE/<capability>.yaml` | 主能力条目；被 R0/复用触及的旧条目（facet 更新、used_in 回写、必要时 stability 降级） |
| `learning-records/NNNN-<slug>.md` | 一条决策级记录：变化、Decision、Implications、`examiner_result` 块（唯一存放处） |
| `REVIEW-QUEUE.md` | 到期项结果（done/failed/deferred）或去向；REVIEW/REPAIR/REINFORCE 的定向项（修复项以 `REPAIR：` 开头）；活动项上限 |
| `lessons/NNNN-slug.plan.md` 进度行 + 门记录 | last_done / 待重试 / 考官 / gates；课结束仍有「待重试」→ 转 `REPAIR：` 项并把进度写 done |
| `INTERVIEW-BANK.md` | 本课新采集的 2–4 题；下节课口述题的「上次使用/结果」 |

**视情况**

| 文件 | 条件 |
|---|---|
| `lessons/NNNN-slug.html` | 复习页：考官后生成，含真实错误与可变题库；讲解页：可课前生成，无答案 |
| `reference/<capability>.html` | 本课产生了可复用的压缩知识 |
| `GLOSSARY.md` | 学习者已理解的新规范用语 |
| `RESOURCES.md` | 新来源，先按验证标准写注释 |
| `MISSION.md` | 追加 S / S-I id（只追加，不重编号） |
| `WORKSPACE.yaml` | `last_ev` 递增；平台/迁移字段 |

**不写**

- `NOTES.md` 里的课序/状态表。NOTES 只放学习者偏好与运营备忘；状态从 KS + RQ 读。
- workspace 外的进度索引只改链接与里程碑勾选，不复制 due 日期或状态。
- 每日日志不是事实源；要写也只写一句指针。

## 8. 预算与降级

```text
预算三档：30 分钟（保底课型）/ 45 分钟（标准）/ 60 分钟（完整新概念课）
超预算：考官压到 2 题；跳过 P4/P6（记录原因）；普通 RQ 顺延（写去向）
连续两题失败 / 学习者说「太难/算了」/ 明显疲劳：停新内容 → 回看讲解块最小段 → 补全题 → 收尾记录 end_reason
会话结束原因：completed | budget_exceeded | fatigue | learner_stop（写进 learning-record）
```

## 9. 结束自检

以 `GATES.md` 的 G1–G5 为准逐条勾；另外确认：

```text
[ ] 讲解块真的在对话里出现过（新概念课），不是只在 plan 里
[ ] 计分交互 ≤6；考官 2–3 题；E-F（面试类）已跑
[ ] 面试题已入库 2–4 道；下节课口述题已选
[ ] P5 迁移嵌入了旧能力；旧 KS 的 used_in 已回写
[ ] evidence/LNNNN.yaml 一课一文件；EV 编号连续、无重复
[ ] 到期没做的 RQ 写了去向；KS review_ref 与 RQ 一致
[ ] 实操是真跑了并有原始结果，或已对过 Probes 三类后诚实降级
[ ] learning-record 写了 Decision 与下一 ZPD 步
```
