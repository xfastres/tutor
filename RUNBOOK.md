# 运行手册（一页）

每次完整课按本页走。本页只列动作与读写清单，规则细节在各专属文件。

## 1. 开场：读（按序，只读需要的）

```text
0. WORKSPACE.yaml                   timezone、protocol、migration（pending 则先过 workspace.md 迁移清单）
1. MISSION.md                       使命、S id、目标环境、只读/沙箱环境
2. REVIEW-QUEUE.md                  先找 `REPAIR：` 项（不看日期），再看 due / scheduled 近 3 天 / deferred 到期
3. KNOWLEDGE-STATE/<目标与前置>.yaml  status、stability、facets、misconceptions、review_ref
4. learning-records/ 最近 1–2 条     上一次的 Decision 与 Implications
5. lessons/ 已有课与 plan            避免重做；取 task_id 序号。plan「进度」未 done = 续课：从 last_done 下一题起，「待重试」先于新题
6. RESOURCES.md 相关条目             要教的事实有没有来源；面试类使命看 Wisdom；Probes 三类探针各自可用否
7. 工具                              配置/状态类只读探针能跑就必跑；行为类只在沙箱；写「降级」前先对 Probes
```

不盲扫整个 workspace。`MISSION.md` 不存在时按 `MISSION-FORMAT.md` 只问影响计划的信息。

**恢复优先级**（每段会话开始都过一遍，不只在一课的第一次开场；进度以 plan「进度」行为准，不凭聊天记录猜）：

```text
① `REPAIR：` 项与「待重试」   不看到期日。是今天内容的前置 → 没过不开新内容
② 上次课未完成的任务          从 last_done 下一题续
③ 到期 RQ                     当次做掉，或按 REVIEW-QUEUE-FORMAT 记去向
④ 新内容
```

## 2. 决定

```text
模式       轻量 | 完整
主能力     唯一；对应一个 S id（没有就按 MISSION-FORMAT 追加一条并在对话确认）
交付模式   对话优先（默认）| 离线课件（学习者独自做，必须导出作答）
R0         1–3 项，按 MEMORY-ENGINE 的选取顺序：REPAIR/待重试 > 到期 RQ > decayed/fragile facet > 今天前置且 last_examined 最旧
实操       使命含运行/排查且只读环境可用 → 本课必含一次实跑
```

## 3. 写课前：plan 侧文件（结构门）

写 `lessons/NNNN-slug.plan.md`（模板见 `lesson-design.md` §12.3）：预检（含探针三类可用否）、覆盖矩阵（含讲解深度、讲解段落）、任务与答案钥匙（含新增维度）、进度行、考官计划、盲区。学习者页面里不放这些。

## 4. 课中

```text
R0（对话作答，结果回写旧条目）
→ 真实问题 + 核心问题
→ Case A → P1 预测（先答再讲）
→ 讲解：直觉 → 机制 → 边界 → 模型 → 怎么验证（不含后续 P 的答案原句）
→ 对一遍 plan 矩阵的「讲解段落」列：标讲到位的项都讲了，才出 P2 起的题
→ Case B 对照 → P2 轻支撑
→ P3 独立（无提示；生成式使命要产出产物）
→ P4 边界/辨析（与讲解里的边界实例不同）
→ 实操（可用时）：预测 → 执行只读动作 → 保存原始结果 → 解释 → 改一个条件再执行
→ P5 迁移（换结构/约束/业务情境，结尾落到产物）
→ P6 仅在关键错误、强提示、答案暴露后：换业务情境/关键条件、无提示重试（lesson-design §5.2）
   P6 失败不再揭示：并排对比 → 补全题 → 新变形；再失败停本课对它的新题
每完成一个 task：更新 plan「进度」行；答案揭示的题进「待重试」，P6 独立通过后移除
「待重试」未清：不进依赖它的新能力；考官必须含它的 E-repair
```

反馈按 `lesson-design.md` §12.1 层级：现象 → 机制 → 模型 → 下一动作。先不给答案。

## 5. 课末：考官

2–4 题，新表面，按矩阵采样，只计分「讲到位」项；「一句带过」项可做不计分探测。面试/考核类使命可用一题真实追问。plan「待重试」未清的机制必须有一题 E-repair，没出或没过只能 REPAIR / REINFORCE。解释题要结论 + 原因，只给结论记 partial。决策五选一，语义见 `EXAMINER.md`。

## 6. 写入集（每课固定）

**必写**

| 文件 | 内容 |
|---|---|
| `evidence/EV-NNNN-MMMM-<lesson>.yaml` | 本课所有改变判断的证据：R0、P、E、实操 |
| `KNOWLEDGE-STATE/<capability>.yaml` | 主能力条目；被 R0 触及的旧条目（facet 更新、必要时 stability 降级） |
| `learning-records/NNNN-<slug>.md` | 一条决策级记录：变化、Decision、Implications，末尾附 `examiner_result` 块（唯一存放处） |
| `REVIEW-QUEUE.md` | 到期项结果（done/failed/deferred）或去向；REVIEW/REPAIR/REINFORCE 决策产生的定向项（修复项以 `REPAIR：` 开头）；检查活动项上限 |
| `lessons/NNNN-slug.plan.md` 进度行 | last_done / 待重试 / 考官；课结束仍有「待重试」→ 转 `REPAIR：` 项并把进度写 done |

**视情况**

| 文件 | 条件 |
|---|---|
| `lessons/NNNN-slug.html` | 对话优先模式：考官后生成，含学习者真实错误与可变题库；离线课件模式：课前生成，含导出 |
| `reference/<capability>.html` | 本课产生了可复用的压缩知识 |
| `GLOSSARY.md` | 学习者已理解的新规范用语 |
| `RESOURCES.md` | 新来源，先按验证标准写注释 |
| `MISSION.md` | 追加 S id（只追加，不重编号） |

**不写**

- `NOTES.md` 里的课序/状态表。NOTES 只放学习者偏好与运营备忘；状态从 KS + RQ 读。
- workspace 外的进度索引（如根目录 `progress.md`）只改链接与里程碑勾选，不复制 due 日期或状态。
- 每日日志不是事实源；要写也只写一句指针。

## 7. 结束自检

```text
[ ] 每条进 Evidence 的观察都有 task_id / capability_id / assistance
[ ] 关键答案曾暴露的题，有没有新的独立重试证据；plan「待重试」已清或已转 `REPAIR：` 项
[ ] 到期没做的 RQ 写了去向
[ ] 实操是真的跑了并有原始结果，还是已对过 Probes 三类后诚实降级
[ ] R0 结果回写了旧条目
[ ] KS 的 review_ref 指向活动项；done/failed 项没有悬空指针
[ ] 活动 RQ ≤ 上限；超了就合并/推迟/转 R0 候选
[ ] learning-record 写了 Decision 与下一 ZPD 步
```
