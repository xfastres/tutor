# 学习证据（Evidence Format）

> v9.1：一课一文件 `evidence/LNNNN.yaml`；新增 `interview` 类型与 `parts`/`followup` 字段；`attempts` 弃用、`verification_ref` 只服务 `execution`。

学习证据回答：**学习者实际做了什么，以及这件事足以支持哪个教学判断。**

它不是完整聊天记录，也不是主观评价。

## 文件组织（v9.1）

一课一个文件，课末一次写入（SKILL 规则 25：写入集中在课末，不要每答一题写一次）：`evidence/LNNNN.yaml`。

文件头放两个索引字段，`evidence:` 下是本课全部 EV（R0、P、E、面试口述、实操）：

```yaml
# evidence/L0013.yaml —— 一课一文件，课末一次写入
lesson_id: "L0013"                    # 必须与文件名一致
capability_ids: ["deduct-in-transaction", "locking-read"]   # 本课 KS：主能力 + 被复用的旧能力
evidence:
  - id: "EV-0139"
    lesson_id: "L0013"
    task_id: "0013-R0a"
    capability_id: "locking-read"
    facet_id: "lock-held-until-transaction-ends"
    type: "prediction"
    result: "passed"
    source: "review"
    assistance: "independent"
    observed_at: "2026-10-20T10:12:00+08:00"
    summary: "新表 swap_rate，READ COMMITTED 下第二次普通 SELECT 答 55，原因是读已提交。"

  - id: "EV-0140"
    lesson_id: "L0013"
    task_id: "0013-E2"
    capability_id: "deduct-in-transaction"
    facet_id: "decide-from-read-value"
    type: "interview"
    result: "partial"
    source: "examiner"
    assistance: "independent"
    observed_at: "2026-10-20T11:02:00+08:00"
    parts:
      conclusion: "pass"
      reason: "pass"
      boundary: "partial"
      example: "missing"
    followup: "partial"
    summary: "题库 IQ-0012「扣减怎么防超卖」；结论与原因完整，边界只说「要开事务」，缺一个具体例子；追问「不够扣时事务怎么结束」答得不完整。"
```

规则：

- 文件名 `LNNNN.yaml` 与 `lesson_id` 一致，一课只此一个文件。历史的多文件命名 `EV-NNNN-MMMM-<lesson>.yaml` 自 v9.1 停用；**历史文件保留、不批量迁移**（避免重写历史事实）。`learning/mysql/evidence/L0012.yaml` 是「旧文件合并成一课一文件」的演示：EV-0129～EV-0138 原样保留。
- `capability_ids` 只列本课主能力与 P5/迁移复用、需要回写 `used_in` 的旧能力（见 `KNOWLEDGE-STATE-FORMAT.md`）。
- 若项目刻意不设 `evidence/`，必须保证每条证据能从 learning-record 通过 `evidence.id` 恢复。

## 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 全局稳定 `EV-NNNN`，创建后不复用、不改号 |
| `lesson_id` | 是 | `LNNNN`，与文件头一致；校验器比对 |
| `task_id` | 是 | `NNNN-R0a`、`NNNN-P3`、`NNNN-E1`、`RQ-0010-R1`、实操 `NNNN-X-run1` |
| `capability_id` | 是 | KS 的 kebab-case id；早期用 `S1` 之类使命 id 的保持原样 |
| `facet_id` | 是（无则 `null`） | 命中的子事实；R0、复习、interview 证据应尽量填 |
| `type` | 是 | 见下节枚举 |
| `result` | 是 | `passed`、`partial`、`failed`、`inconclusive` |
| `source` | 是 | `lesson`、`examiner`、`review`、`delayed-examiner`、`offline-export`、`mock` |
| `assistance` | 是 | `independent`、`light_hint`、`strong_hint`、`answer_exposed`、`unknown` |
| `observed_at` | 是 | 实际产生证据的时间，带 offset 的 ISO 8601 |
| `summary` | 是 | 只记最能影响教学决策的观察，不抄整段答案 |
| `parts` / `followup` | `interview` 必填 | 四段评分与追问，见「面试口述证据」 |
| `verification_ref` | `execution` 必填 | 指向 `VER-NNNN` 验证记录；其他类型不填或 `null` |
| `attempts` | **deprecated** | 仅为兼容旧文件保留；新证据不填，多轮轨迹写 `summary` |

## 类型（type）

`recognition`、`explanation`、`prediction`、`diagnosis`、`generation`、`execution`、`transfer`、`boundary`、`interview`。

| 类型 | 回答什么 | 判分要点 |
|---|---|---|
| `recognition` | 认得出 | 只作辅助，不能单独支撑 `functional`/`transferable` |
| `explanation` | 讲得对机制 | 必须有原因；题目要原因只给结论 → 记 `prediction`/`recognition` 且 `result` 至多 `partial` |
| `prediction` | 猜得准结果 | 数值/形状对即可，不要求原因 |
| `diagnosis` | 看得出病因 | 从现象/执行计划定位到机制 |
| `generation` | 写得出产物 | 真实产物（SQL/DDL/命令/代码/文本） |
| `execution` | 真跑得出结果 | 必须 `verification_ref` 指向通过的 `VER` 记录 |
| `boundary` | 换一个关键条件后判断仍对 | 实例不得与讲解里的边界例子相同 |
| `transfer` | 换业务/结构/约束仍会用 | 只换数字、名字、措辞不算 |
| `interview` | 60 秒讲得清（表达） | 四段 + 追问，见下节 |

`interview` 与相邻类型的区别：`explanation` 评「机制说得对不对」（不限时、可只答一个点）；`generation` 评「能不能写出产物」；`transfer` 评「换表面后还会不会用」；`interview` 评「能不能在面试压力下，60 秒内把结论、原因、边界、例子组织完整并接住一次追问」。面试口述是**表达证据**，不替代生成/迁移/实操证据。

## 面试口述证据（interview）

- 结构固定四段：**结论 → 原因 → 边界 → 例子**。来源题目写进 `summary`（题库 id 或 URL + 题干一句话）。
- `parts` 四个键必须齐：`conclusion`、`reason`、`boundary`、`example`，取值 `pass | partial | missing`。
- `followup`：追加一次追问是否接住，取值 `pass | partial | missing`。追问只有一次机会，**不得夹带答案或方向**；带方向即按提示等级升级 `assistance`。
- `result` 映射：四段 `pass` 且 `followup: pass` → `passed`；缺 1 段、或 `reason` 只到 `partial`、或追问 `partial` → `partial`；结论错、`reason: missing`、或讲不成句 → `failed`。
- 四段里 `reason` 是门槛：`reason` 缺失/错误时，即使结论对也不能记 `passed`，也不得作为 `conceptual_understanding` 证据。
- 只给结论的 `interview`（`reason: missing`）按 `explanation` 的同一规则处理，`result: partial`。
- 提示或答案揭示后重新口述：按 `assistance` 记 `strong_hint` / `answer_exposed`，复述不得记 `passed`（见「支撑程度」）。
- 同一道题隔课复测要新 `EV`（新 `task_id`），不复用旧条目。

## 支撑程度（assistance）

`assistance` 区分独立表现与提示后订正，按老师该次作答前说过的**最强一句**判定：

- `light_hint`：只指出哪里不对或缩小范围（「等于 50 那行在不在锁里？」），没说改成什么
- `strong_hint`：给了结构、骨架，或点名缺哪个成分（「先锁定读，再在 PHP 里判断」）
- `answer_exposed`：说出了具体语句、值或关键词（「SET qty = qty - 3」）；指回讲解里已含答案的例子至少算 `strong_hint`
- `unknown`：仅兼容无法恢复支撑程度的历史证据，不用于新的状态升级

上限：

- `independent`：可用于独立能力与迁移判断；
- `light_hint`：可支持正在形成的能力，不能单独证明无提示独立完成；
- `strong_hint`：主要用于诊断和修复过程；
- `answer_exposed`：只记录纠正过程，**不得记作独立通过**，不能用于 `functional`/`transferable` 升级；`interview` 场景同理——老师先给过四段骨架再复述，不算表达达标。

关键答案暴露后，必须由新的 `task_id` 产生一个未见变形的 `independent` 重试证据；不能把同题订正改写为独立成功。变形须换业务情境或关键条件，不只换数字、变量名、表名；完整分支见 `lesson-design.md` §5.2。

同一 task 的多轮订正只记一条 EV：不填 `attempts`，把轮次与轨迹写进 `summary`（如「第 2 轮在 light_hint 后改对」），`assistance` 取用过的最强等级；新表面重试另起 `task_id`（P6 或新 E 编号）才记新 EV。X 探测（不计分）不建 EV，只写进 learning-record 的 probes。

v8.6 之前没有 `assistance` 的历史 Evidence 不要批量改写。能从原始学习记录确认支撑程度时按纠错流程补齐；无法确认时视为 `assistance: unknown`，不得单独用于新的状态升级。

## 一课的条数上限

计分交互 ≤6（R0 ≤1、开场口述 1、P ≤3、E ≤3，总数 6 为硬顶），因此一个 `LNNNN.yaml` 通常只有 **3–6 条计分 EV**；X 探测不进文件。旧课历史上超过 6 条的（如 L0011 有 17 条），合并时原样保留，不重写、不补删。

## EV 编号分配

- 开课前读 `WORKSPACE.yaml` 的 `last_ev`（全局已分配的最大 EV 序号，整数）。
- 没有该字段时：取现有 evidence 中最大 EV 序号 + 1，并在本次写入时把 `last_ev` 回写进 `WORKSPACE.yaml`。
- 本课 EV 从 `last_ev + 1` 起连续分配；课末把最后一条的序号回写 `last_ev`。
- EV id 一旦创建永不复用；发现断档不要补号（历史断档是分块预留造成的，属正常）。

## 与 Knowledge State 的关系

- 本文件保存**可引用的观察**；`KNOWLEDGE-STATE-FORMAT.md` 保存**当前压缩状态**。
- 状态升级/降级必须引用 `evidence.id`，不引用自然语言结论或文件名。
- 维度归属：`explanation` → `conceptual_understanding`；生成/诊断/实操 → `execution`；`boundary` → `boundary_awareness`；`transfer` → `transfer`；`interview` → `expression`（v9.1 新增，规则见 KS-FORMAT）。
- 完整学习记录仍写入 `learning-records/`；证据不替代学习记录。

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
  reason_evidence_ids: ["EV-0139"]
  observed_at: "2026-10-20T10:22:00+08:00"
```

若没有状态变化，不必制造 transition 记录。

## 验证诚实性（execution / verification_ref）

- 只有 `type: execution` 填 `verification_ref`，且必须指向同文件或引用文件里的 `VER-NNNN` 验证块；验证块结构按 `SEMANTIC-VERIFICATION.md` 的结果契约。
- 其他类型不填 `verification_ref`（或 `null`）；口述、预测、静态推导、LLM 语义判断都不构成执行通过。
- 没有真实执行时，不要写成 `type: execution`：改记 `prediction` / `explanation`，并在 `summary` 里注明「未在库上执行」。
- `verification_ref` 是自由文本、找不到对应 VER 记录、或 VER 的 `status` 非 `passed` 时，该证据不得用于 `execution` 或依赖它的状态升级；补 VER 或降级证据，不伪造。
- `inconclusive` 表示证据不足，不得用于暗示通过。
- 只允许只读/沙箱内执行；生产库上的 `FOR UPDATE`/`LOCK` 类语句即使有真实输出也不作为执行证据（见 `SEMANTIC-VERIFICATION.md` 允许清单）。

## 创建与引用规则

- 先判断现有证据是否已覆盖同一观察；能复用就引用，不重复创建。
- Evidence ID 一旦创建，内容只做纠错性修订，不因后续状态变化重写历史事实。
- 跨文件引用一律写 `EV-NNNN`，不写文件名、不写「某堂课考官」这类自然语言引用。
- `summary` 里出现的范围外正确补充照实记，但不写成错误（见 KS `misconceptions` 规则）。

## 课末机械校验（对应 G5 证据门）

```text
[ ] 文件名为 evidence/LNNNN.yaml，文件头 lesson_id 与文件名一致
[ ] 每条 EV 字段齐：id / lesson_id / task_id / capability_id / result / source / assistance / observed_at / summary
[ ] lesson_id 与文件头一致；capability_id 是本 workspace 存在的 KS id（或 legacy S id 白名单）
[ ] EV id 全局唯一、本课连续；与 WORKSPACE.yaml 的 last_ev 一致
[ ] type=interview 的条目 parts 四键齐全、followup 存在；type=execution 的条目 verification_ref 指向存在的 VER 记录
[ ] answer_exposed 的记录没有 result=passed，且没有被当作独立升级依据
[ ] KS / REVIEW-QUEUE / plan 引用的 EV id 都能在本文件找到
```
