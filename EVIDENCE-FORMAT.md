# 学习证据（Evidence Format）

学习证据回答：**学习者实际做了什么，以及这件事足以支持哪个教学判断。**

它不是完整聊天记录，也不是主观评价。

## 最小结构

```yaml
evidence:
  - id: "EV-0001"
    task_id: "0001-P3-01"
    capability_id: "left-join-on-vs-where"
    facet_id: null
    type: "generation"
    result: "passed"
    source: "lesson"
    assistance: "independent"
    observed_at: "2026-09-08T10:22:00+08:00"
    summary: "无关键提示下生成目标产物，并解释决定性条件。"
    verification_ref: null
```

## 字段

- `id`：全局稳定证据 ID，格式 `EV-NNNN`；同一证据不重复创建。
- `task_id`：产生这份证据的任务 ID：`NNNN-P3`、`NNNN-R0a`、`NNNN-E1`、`RQ-0010-R1`、实操 `NNNN-X-run1`。X 探测（不计分）不建 Evidence，只写进 learning-record。同一 task 的多轮订正只记一条 EV：`attempts` 记轮数，`assistance` 取用过的最强等级，轨迹写进 summary；新表面重试另起 task_id（如 P6）才是新 EV。
- `attempts`（可选）：同一 task 的作答轮数，缺省 1。
- `capability_id`：Knowledge State 的 id（kebab-case）；早期 workspace 用 `S1` 之类使命 id 的保持原样，新证据用能力 id，S id 由 KS 的 `mission_ids` 关联。
- `facet_id`：命中的子事实 id；没有则 `null`。R0 与复习证据通常应填。
- `type`：`recognition`、`explanation`、`prediction`、`diagnosis`、`execution`、`generation`、`transfer`、`boundary`。`explanation` 要求作答含机制原因；题目要原因而只给了结论的，记 `prediction` / `recognition`，`result` 至多 `partial`。学习者给出的范围外正确补充写进 summary，不写成错误。
- `result`：`passed`、`partial`、`failed`、`inconclusive`。
- `source`：`lesson`、`examiner`、`review`（含 R0）、`delayed-examiner`、`offline-export`（学习者离线作答后贴回的导出）。
- `assistance`：`independent`、`light_hint`、`strong_hint`、`answer_exposed`、`unknown`；所有会改变状态的 Evidence 必须填写且不能为 `unknown`，用来区分独立表现与提示后订正。判别按老师在该次作答前说过的最强一句：
  - `light_hint`：只指出哪里不对或缩小范围（「等于 50 那行在不在锁里？」），没说改成什么
  - `strong_hint`：给了结构、骨架，或点名缺哪个成分（「先锁定读，再在 PHP 里判断」）
  - `answer_exposed`：说出了具体语句、值或关键词（「SET qty = qty - 3」「START TRANSACTION 写在 SELECT 前」）
  - 指回讲解里已含答案的例子，至少算 `strong_hint`
- `observed_at`：实际产生证据的时间；跨会话时使用带 offset 的 ISO 8601。
- `summary`：只记录最能影响教学决策的观察，不抄整段答案。
- `verification_ref`：若有确定性执行/外部校验，指向对应验证结果；没有则为 `null`。验证结果必须符合 `SEMANTIC-VERIFICATION.md` 的结果契约。

## 证据等级

优先级由任务性质决定，但一般遵循：

```text
实际生成/操作结果
> 变形/边界行为
> 对照/预测
> 解释
> 识别
```

不得把较弱证据伪装成较强证据。

支撑程度影响证据上限：

- `independent`：可用于独立能力与迁移判断；
- `light_hint`：可支持正在形成的能力，但不能单独证明无提示独立完成；
- `strong_hint`：主要用于诊断和修复过程；
- `answer_exposed`：只记录纠正过程，不能用于 `functional` / `transferable` 升级。
- `unknown`：仅兼容无法恢复支撑程度的历史证据，不能用于新的状态升级。

关键答案暴露后，必须由新的 task_id 产生一个未见变形的 `independent` 重试证据；不能把同题订正改写为独立成功。变形须换业务情境或关键条件，不只换数字、变量名、表名；完整分支见 `lesson-design.md` §5.2。

v8.6 之前没有 `assistance` 的历史 Evidence 不要批量改写。能从原始学习记录确认支撑程度时按纠错流程补齐；无法确认时视为 `assistance: unknown`，不得单独用于新的状态升级。

## 与 Knowledge State 的关系

- `EVIDENCE-FORMAT` 保存**可引用的观察**；`KNOWLEDGE-STATE-FORMAT` 保存**当前压缩状态**。
- 状态升级/降级应引用相关 `evidence.id`，不要只写自然语言理由。
- 完整学习记录仍写入 `learning-records/`；证据本身不替代学习记录。
- 独立性是状态门槛的一部分：提示后成功与同题订正不能替代独立生成/操作或迁移证据。

## 状态变化引用

Knowledge State 可保留最近一次有效变化：

```yaml
last_transition:
  from:
    status: "functional"
    stability: "unknown"
  to:
    status: "transferable"
    stability: "unknown"
  reason_evidence_ids: ["EV-0007"]
  observed_at: "2026-09-08T10:22:00+08:00"
```

若没有状态变化，不必制造 transition 记录。

## 验证诚实性

- `verification_ref` 只能指向实际执行或明确的外部验证结果。
- 没有执行环境时，证据可以是静态推导或人工解释，但不得写成“已运行通过”。
- `inconclusive` 表示当前证据不足以支持状态变化，不得用于暗示通过。
- 运行时/工具操作目标只有在 `verification_ref` 指向通过的确定性执行/外部验证时，才能形成“实操通过”类 Evidence；口述命令、预测输出和 LLM 语义判断不够。

## 持久化位置

一课一个文件：`evidence/EV-NNNN-MMMM-<lesson>.yaml`（如 `EV-0084-0088-lesson0008.yaml`），内含该课全部证据（R0、P、实操、E）。Knowledge State 只保留摘要与引用。若项目刻意不设 `evidence/`，必须保证 Evidence 能从 learning-records 通过 `evidence.id` 恢复。

`offline-export` 来源的证据，`summary` 要注明导出里的 `attempts` 与 `revealed`；`revealed: true` 的作答按 `answer_exposed` 记。

## 创建与引用规则

- 先判断现有任务/证据是否已经覆盖同一观察；能复用就引用，不重复创建。
- evidence ID 一旦创建，内容只做纠错性修订，不因后续状态变化重写历史事实。
- 后续状态判断引用旧证据；不要把历史证据直接改成新的结果。
