# 知识状态（Knowledge State）

一个概念/技能一个条目，只保存**当前状态**，不写课程流水账。

## 数据结构

```yaml
knowledge_state:
  id: "<稳定 kebab-case id>"
  name: "<概念或技能>"
  mission_ids: ["S7"]            # 对应的使命成功标准；可多个

  # 能力层级：现在能做到什么，不是稳定性
  status: "functional"           # exposed | familiar | functional | transferable

  # 稳定性是独立维度；允许 functional + fragile
  stability: "unknown"           # unknown | fragile | stable

  dimensions:
    conceptual_understanding: "strong"   # weak | partial | strong | unknown
    execution: "strong"
    changed_case: "partial"
    transfer: "unknown"
    boundary_awareness: "partial"

  # 可单独验证的子事实；只列使命需要的，通常 2–6 条
  facets:
    - id: "secondary-index-carries-pk"
      claim: "二级索引叶子带主键，再回聚簇索引取整行"
      state: "ok"                # ok | decayed | untested
      last_verified: "2026-10-10"
      evidence_ids: ["EV-0085"]
    - id: "select-star-not-covered"
      claim: "SELECT * 通常盖不住窄的二级索引"
      state: "untested"
      last_verified: null
      evidence_ids: []

  evidence:
    - "EV-0087：考官新表，title 迫使回表，id 已在二级索引"
    - "EV-0088：Using index condition 分类对，机制未说清"

  misconceptions:
    - "<重要误解，原话化>"

  depends_on: ["indexes-basics"]
  used_in: []
  contrasts_with: ["index-condition-pushdown"]

  # 复习调度的唯一事实源是 REVIEW-QUEUE.md；这里只保存指针
  review_ref: "RQ-0010"          # 活动项 id；没有则 null

  last_examined: "2026-10-10"    # 最近一次 Examiner / 延迟考官 / R0 产生状态判断的日期

  # 只在状态真正变化时存在
  last_transition:
    from: { status: "exposed", stability: "unknown" }
    to: { status: "transferable", stability: "unknown" }
    reason_evidence_ids: ["EV-0084", "EV-0087"]
    observed_at: "2026-10-10T11:11:00+08:00"
```

`evidence` 列表只放压缩摘要与 id；原子证据在 `evidence/`。考官的 `examiner_result` 块不放这里（在该课 learning-record），本文件只更新 `last_examined` 与受影响的维度/facets/`review_ref`。

## 状态定义与进入标准

`status` 取当前**最高、证据足够支持**的层级：

| 状态 | 含义 | 最低进入证据 |
|---|---|---|
| `exposed` | 接触过，无可靠使用证据 | 仅出现、阅读、观察 |
| `familiar` | 能在熟悉表面识别、回忆或用自己的话解释核心关系 | 至少一次有意义的提取/解释，且无关键误解阻塞 |
| `functional` | 能独立完成熟悉任务 | 至少一次 `assistance: independent` 的生成/操作/诊断，并能解释关键步骤 |
| `transferable` | 换表面、结构、约束或情境后仍能使用模型 | 至少一次独立的变形/迁移证据，且失败不是由未解决的前置造成；使命有高价值边界时还需边界证据 |

这些是最低门槛，不是计数器。证据不足保持较低状态。

## 维度尺度

- `unknown`：尚无足够证据。
- `weak`：有证据，但存在影响后续使用的明显缺口、依赖提示或错误。
- `partial`：核心关系可用，仍有限定条件、边界或一致性缺口。
- `strong`：已测试条件下表现充分、连贯、无已知关键缺口。不表示跨时间稳定。

`execution` 表示使命定义的目标动作是否真正完成。目标依赖数据库、运行时、工具时，`execution: strong` 必须有通过的确定性执行引用（`verification_ref`）。口述命令、预测输出、静态推导不能证明运行能力。

`conceptual_understanding: strong` 需至少一条 `type: explanation` 且 `assistance: independent` 的证据；预测题数值正确不算。

## facets

- facet 是教学上会单独衰减、单独出题的子事实；不是课程大纲。
- `state`：`ok` = 最近一次在新表面独立通过；`decayed` = 最近一次 R0/复习/考官失败或只在提示后才对；`untested` = 从未单独验证。
- 任一 facet 为 `decayed` → 能力 `stability` 必须为 `fragile`，直到该 facet 在新 `task_id` 下 `assistance: independent` 通过。
- 升到 `stable` 时所有已测 facet 必须为 `ok`；`untested` 的 facet 不阻止 `stable`，但应在后续 R0 顺序 3 中优先出题。
- R0 命中某 facet 时，无论对错都更新 `last_verified` 与 `state`，并产生 evidence。

## 稳定性

- `unknown`：无延迟/交错证据。
- `fragile`：出现明确不稳定信号：延迟失败、重复失败、边界混淆、facet decayed；或 `stable` 被关键失败推翻。
- `stable`：至少一次有意义的延迟或交错检查仍可用，且建立在 `functional` 以上。
- 从 `fragile` / `unknown` 回到 `stable` 必须有新的延迟/交错正向证据；课内即时成功和讲解后立刻答对（`light_hint`）不能清除 `fragile`。

`stable` 不是比 `transferable` 更高的能力层级。

## 一致性规则

1. `transferable` 必须先满足 `functional` 的独立证据，再加独立的 `changed_case` 或 `transfer` 证据；有高价值边界时还需边界证据。
2. `functional` 至少需要一次 `assistance: independent` 的目标动作证据；识别、复述、强提示后完成、答案暴露后订正不能进入。
3. 运行时/工具操作是目标时，`execution: strong` 及依赖它的升级必须引用通过的确定性执行。
4. `answer_exposed` 只记录纠正过程；必须有新 `task_id` 的 `independent` 重试才算修复。
5. `stable` 必须有延迟或交错证据；课末一次成功不能产生。
6. 关键维度或 facet 与 `status` 冲突时，以更低、证据支持的一侧为准并记录原因。
7. 不为未测维度补填 `strong/partial/weak`；高层 `status` 不得跳过低层证据。
8. `review_ref` 只能指向 REVIEW-QUEUE 中 `scheduled|due|deferred` 的条目；`done|failed` 只能作历史。
9. 复习的原因、动作、到期、完成标准只属于 REVIEW-QUEUE；本文件不复制这些字段，也不保留旧版 `review:` 块。
10. `last_examined` 固定 `YYYY-MM-DD`。
11. P3 独立成功主要提供 `functional`/`execution` 证据；P4 提供 `changed_case`/`boundary_awareness`；P5 提供 `transfer`。P 编号本身不产生状态。
12. `misconceptions` 只收与事实相悖的说法。正确但超出本课范围的补充（如问页机制时答分库唯一性）不是误解，不进此列表；记在 EV summary 或 learning-record。学习者说不出本课机制这件事本身可以记为误解或弱维度。

## 状态转移

- 升级必须引用足以支持新状态的 evidence id；没有新证据不得升级。
- 关键反向证据允许降级，但不删除较高状态曾真实存在的历史；只更新当前状态并记录 `last_transition`。
- `stable → fragile` 必须引用关键延迟/交错失败或 facet decayed 的证据。
- `deferred` 本身不产生证据，也不改变状态。

## ID 与时间

- `id` 用稳定 kebab-case；同一概念跨课程复用。
- 到期时间只在 REVIEW-QUEUE 维护；本文件不存第二套。
- 详细证据结构见 `EVIDENCE-FORMAT.md`。

## 更新规则

- 只在新证据改变判断时更新。
- 保存最能改变后续教学决策的证据，不保存完整作答。
- 原始学习记录在 `learning-records/`；这里是压缩后的当前状态。
