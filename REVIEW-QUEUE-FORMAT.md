# 复习队列（Review Queue）

只保留高价值的**定向**延迟复习项（MEMORY-ENGINE 通道 A）。复习项描述下一次要产生什么学习证据，不是“再看一遍笔记”。普通稳定性检查走下一课 R0，不进队列。

## 形式

表格或条目块二选一，一个 workspace 内保持一致。

**表格（推荐，适合短项）**

```md
| id | 知识 ID | due | 做什么（含完成标准） | status | 结果 |
|----|---------|-----|----------------------|--------|------|
| RQ-0010 | covering-index | 2026-10-13 | 无提示说出 Using index condition 不是覆盖、筛完仍可能读整行；完成标准：独立说出差别 | scheduled | |
| RQ-0008 | composite-leftmost-prefix | 2026-10-10 | 新表面：跳过中间列仍可用最左列 | done | EV-0083（light_hint） |
| RQ-0012 | atomic-decrement | 2026-10-14 | REPAIR：答案揭示后未独立重试。换业务情境无提示写出整段扣减事务；完成标准：独立写出且锁盖住读与改 | scheduled | |
```

**条目块（适合需要间隔依据的项）**

```text
ID：RQ-0001
知识 ID：<kebab-case>
facet：<可选>
为何复习：
做什么：
完成标准：<可观察条件>
到期时间：YYYY-MM-DD 或带 offset 的 ISO 8601
间隔依据：<可选；只作生成时记录>
状态：scheduled | due | done | failed | deferred
结果：<EV id / 新 RQ id>
```

执行时在任务内部用稳定 `task_id`（如 `RQ-0010-R1` 或承载它的 `0010-R0a`），Evidence 通过该 id 回链。

## 状态

- `scheduled`：等待到期。
- `due`：当前日期 ≥ 到期时间，应执行。
- `done`：按本项完成标准达成并产出证据。
- `failed`：未达完成标准；部分完成也记 `failed`，必要时建新项。
- `deferred`：暂缓，但必须同时写新的绝对到期时间，不能只写“以后”。到期后重新进入 `due`。

仅日期 `YYYY-MM-DD` 按 workspace 的 timezone 解释。外部 scheduler 只负责触发检查，不拥有状态。

**修复项**：「做什么」以 `REPAIR：` 开头，来源是考官 `REPAIR` / `REINFORCE` 的 target，或课结束时仍未清的「待重试」。选取时不看到期日（`MEMORY-ENGINE.md` 顺序 0），不转 R0 候选、不推迟。

**面试崩题回流（v9.1）**：`INTERVIEW-BANK.md` 中口述/模拟面判定「崩」的题，建一条 `REPAIR：` 项并写明缺段（如 `REPAIR：缺边界`）；判定「部分」不建队列项，只把结果写回题库。修复方式优先换一道同 capability 的新题，而不是重背原题。

## 完成标准与结果

`done`/`failed` 依据条目自己的完成标准判定，不依据“学习者参与过”。完成标准尽量写可观察结果，例如“无关键提示独立判断并说出决定性条件”。提示后答对的，按 `EVIDENCE-FORMAT.md` 判别记 `light_hint` / `strong_hint`，可以 `done`，但结果栏必须注明等级，且不能单独清除 `fragile`；`answer_exposed` 不能 `done`。`REPAIR：` 项只有 `independent` 才能 `done`。

## 延迟考官协议

复习项要求延迟后的独立、变形或边界证据时，它就是一次延迟考官：

```text
到期项 → 新表面短任务 → 学习者先作答 → 按目标维度/facet 分析 → 更新 KS → 按 MEMORY-ENGINE 定下一步
```

成功达标 → `done`；部分成功 → `failed` + 定向后续；关键失败 → `failed` + 修复；暂时无法执行 → `deferred`。

## 规则

- 复习模型/技能，不复习笔记；优先提取、对照、变形、真实应用。
- 具体间隔与复习债控制只由 `MEMORY-ENGINE.md` 决定；活动项上限默认 4。
- 同一知识 ID 默认最多一个活动项（`scheduled|due|deferred`）。完成或失败后仍需复习时新建条目并更新 KS 的 `review_ref`；历史条目保留。
- `review_ref` 不得指向 `done`/`failed`。活动项进入 `done`/`failed` 的同一更新里，必须把 `review_ref` 清空或指向新活动项。
- 写入前重读队列；同一知识 ID 已有活动项时更新/复用，不重复创建。
- `ADVANCE` 不创建条目。只有 `REVIEW` / `REPAIR` / `REINFORCE` 的 target、复习失败项、以及 R0 中发现的 facet decayed 才创建。
- 跨会话以绝对到期时间为准；“3 天后”只能是生成时的计算依据。
- 到期项在某次会话没执行必须记去向：当次做掉 / `deferred` + 新日期 / 保持 `due` 并在当课 plan 进度行写「顺延到下次开场」。不能静默跳过。
- 删除低价值条目。每个条目都必须能改变后续教学或稳定性判断。
