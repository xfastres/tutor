# 门禁（Gates）v9.1

本文件是五道门判据的**唯一来源**：`SKILL.md` 只列门名，`RUNBOOK.md` 只写执行顺序，`lesson-design.md` 只讲怎么设计课。判据冲突时以本文件为准，并回头修另一处。适用于 FULL 的 `NEW_CONCEPT`/`PRACTICE`/`REVIEW`/`MOCK`；轻量模式不走门。任一 gate 不过不结课，plan `gates` 写原因。

## 总表

| 门 | 何时 | 判据摘要 | 落盘 | 不过怎么办 |
|---|---|---|---|---|
| G1 结构门 | 写课前 | 能力/课型/教学块计划/矩阵/预算/门记录位 | plan 头部+`gates.G1` | 补 plan；太宽拆课 |
| G2 讲解门 | `NEW_CONCEPT` 首题前 | 讲解块已发出：7 元素、400–800 字、无答案泄漏 | `teaching_block`+`gates.G2` | 补讲/按 `PRACTICE` 收尾 |
| G3 练习门 | 课中每题后 | 计分交互≤6、独立产物、P5 嵌旧知、边界换实例 | 进度行+`gates.G3` | 砍题/补 P5/重判降级 |
| G4 考官门 | 课末 | 2–3 计分题+X、只考讲到位、E-F 必选、五选一 | LR `examiner_result`+题库 | 覆盖不足不 `ADVANCE` |
| G5 证据门 | 结课前 | 一课一文件、assistance 诚实、KS/RQ/used_in 对齐 | evidence/KS/RQ/LR | 停结课先补 |

## G1 结构门（写课前）

- [ ] 课型写 plan：`NEW_CONCEPT`（先讲后测）/`PRACTICE`/`REVIEW`（先测后讲）/`MOCK`；流程与课型一致（SKILL 规则 2）。
- [ ] 主能力唯一 + `capability_id` + 核心问题 + 使命 `S`/`S-I` id + 前置 KS。
- [ ] R0：`NEW_CONCEPT`≤1、`PRACTICE`/`REVIEW` 1–3；题干无答案；依据（`REPAIR：`/待重试>到期 RQ>fragile/decayed>今日前置）已写。
- [ ] 交付模式 + 预算 30/45/60 + 超预算保底课型（RUNBOOK §8）；目标环境/版本 + `RESOURCES.md` Probes 三类可用否 + 实操降级判断。
- [ ] `teaching_block`（新概念必填）：段落标题、7 元素、案例 A/B、边界实例、400–800 字、讲解禁止原句；其余课型写「豁免+理由」。
- [ ] 覆盖矩阵：核心能力/决定性变量/边界/迁移/实操/讲解深度/讲解段落/复用旧知（旧能力+用途+证据任务）/盲区；关键项→证据任务（盲区除外）。
- [ ] 答案钥匙（必须点/常见半对/失败模式/新增维度）；考官计划 2–3 题+X+E-F 题库题号；面试节奏（上节 2–4 题入库/本课口述题已选/模拟面是否满 3 课）；`gates` 五行位。
- 落盘：plan+`gates.G1: pass`（fail 写 reason）。不过：回写缺项再开课；7 元素或矩阵写不清=课太宽→拆课或改 `PRACTICE`；预算没选默认 45 分钟并说明。

## G2 讲解门（首题前；`NEW_CONCEPT`）

- [ ] 讲解块在**对话里**出现过（只在 plan/HTML 里不算），先于任何针对本课新能力的计分题，一次发完；R0 与开场 60 秒口述只考旧知，可以出现在讲解块之前。
- [ ] 7 元素齐全：真实场景 → 机制因果链 → 案例 A → 对照/反例 B（只改一个有意义变量）→ 边界/例外 → 怎么验证 → 一句话模型（结论+适用范围）。
- [ ] 400–800 字、2–3 段；每段夹案例或对照；不堆定义与相邻术语。
- [ ] 不含后续计分题答案原句/数值/关键词；计分边界题实例 ≠ 讲解实例。
- [ ] 首题在讲解块之后；讲解后至少一次提取（P1 预测或复述）；矩阵「讲解段落」能指到段落，指不到就改标「一句带过」。
- [ ] 实发讲解与 plan `teaching_block` 一致；不一致按实发回写 plan 并检查泄漏。
- 豁免：`PRACTICE`/`REVIEW`/`MOCK`，条件是本课不引入新能力（目标已 `functional` 及以上，或只做变式/诊断/重测）；再教内容 ≤200 字定向反馈（现象→机制→模型→下一动作），仍不含后续计分题答案。需要 7 元素级新讲解 → 转 `NEW_CONCEPT`，本场按练习收尾。
- 落盘：`gates.G2`；讲解页 HTML（如生成）不含答案；实发块摘要（与 plan 不同时）。不过：补讲一次或删相邻内容；课型标错按 `PRACTICE` 收尾并记修正；已泄漏题降为纠正过程、进「待重试」。

## G3 练习门（课中）

- [ ] 计分交互总数≤6（R0、开场 60 秒面试口述、P、E 都算；X 探测与订正轮次不计）；分类上限 R0≤1（`NEW_CONCEPT`）、P≤3、E≤3；超限先砍低信息 P 与 E 探测。
- [ ] 普通 RQ 不挤占 `NEW_CONCEPT`（`REPAIR：` 例外，只插 1 项并说明）；`PRACTICE`/`REVIEW` 以 R0/RQ 1–3 项为主体。
- [ ] ≥1 次无关键提示的独立生成/预测/诊断/操作；生成式/操作型使命 ≥1 真实产物；阶梯按 `lesson-design.md`（样例→补全→独立），每题只新增一个主要维度。
- [ ] P5/迁移嵌入至少一个旧能力（矩阵「复用旧知」写旧能力+用途），不是同表面换皮；边界证据实例 ≠ 讲解实例。
- [ ] 只读/沙箱可用即用：≥1 次真实执行并保存原始结果；不可用先对 Probes 三类再诚实降级。答案暴露/强提示/关键错误 → P6 新表面无提示重试（占 P 名额），复述不另计。
- [ ] 每题后更新 plan 进度行（last_done/待重试）；文件写入留到课末批量做。
- 落盘：进度行+`gates.G3`+P6/待重试。不过：砍题到上限内；补 P5/边界/独立题；实操误判按探针表重判。

## G4 考官门（课末）

- [ ] `NEW_CONCEPT`/`PRACTICE`/`REVIEW`：2–3 个计分题+可选 X（不计分、不计题数）；E-repair 占计分题名额。`MOCK` 按 `MEMORY-ENGINE.md` 模拟面协议 5–8 题、计时、追问 1 次，不受 2–3 限制。
- [ ] 只考「讲到位」；「一句带过」只作 X；「未讲」不出题。
- [ ] 新表面；边界/迁移实例 ≠ 课内实例；≥1 题测课内未充分验证的高价值维度。
- [ ] 一题一次判：不得拆 b/c/d 多轮追问；失败后最多 1 次新表面重试，再不过 → `REPAIR`/`REINFORCE`。
- [ ] 首答无泄漏；强提示/答案暴露后不作独立通过；解释题只给结论记 `partial`（见 `EXAMINER.md`）。
- [ ] 面试/考核类 E-F 必选（`INTERVIEW-BANK.md` 真题、60 秒、四段评分，缺段 `partial`、`type: interview`）；矩阵关键项都有题或课内证据；「待重试」都有 E-repair；输出五选一决策+`covered_points`。
- 落盘：LR 末尾 `examiner_result`（decision/evidence_ids/target/covered_points/probes）；`INTERVIEW-BANK.md` 追加本课 2–4 题（题面/来源/可信度/S-facet/类型/状态，格式见 `INTERVIEW-BANK-FORMAT.md`）；崩题建 `REPAIR：` 项。
- 不过：覆盖不足→补最小信息量任务，或降状态/`REPAIR`/记盲区；不得因其他题答对而 `ADVANCE`；答案暴露后的表现只能走 `REPAIR`/`REINFORCE`。

## G5 证据门（结课前）

- [ ] evidence：`evidence/LNNNN.yaml` 一课一文件、课末一次写、含 `lesson_id`；EV 全局唯一、本课内连续（历史断档不补号；与 `WORKSPACE.yaml` 的 `last_ev` 对齐）。
- [ ] 每条改变判断的 EV 有 `task_id`/`capability_id`/`assistance`/`result`/`type`/`source`；assistance 按作答前最强一句判，`unknown` 不用于升级，`answer_exposed` 只记纠正过程。
- [ ] 面试证据：`type: interview`，四段（结论/原因/边界/例子）逐段结果，缺段记 `partial`；开场口述与 E-F 都入库。
- [ ] KS：主能力与旧条目已更新；引用的 EV 存在；状态不超过独立性/执行方式/验证来源；facet 的 `state`/`last_verified` 有依据；`used_in` 回写（旧能力←本课 capability_id+evidence_id）；`expression` 维度按 interview 证据更新。
- [ ] RQ：到期项 `done`/`failed`/`deferred` 或写明去向；活动项≤上限；`REPAIR：` 项来源可追；KS `review_ref` 与活动项一致。
- [ ] plan：`gates` G1–G5 逐项 pass/fail+原因；进度行 last_done/待重试/考官一致；结课仍有待重试 → 转 `REPAIR：` 项。
- [ ] learning-record：Decision/Implications/probes/`examiner_result`（唯一存放处，含 `covered_points`）/`end_reason`（completed/budget_exceeded/fatigue/learner_stop）。
- [ ] `INTERVIEW-BANK.md`：本课 2–4 题已入库，下节课口述题已选（状态与上次使用）；验证诚实（未执行不写「已运行」，`execution: strong` 有确定性执行引用）。
- 落盘：以上全部+`WORKSPACE.yaml` `last_ev` 递增。不过：缺项停结课、先补写；不能诚实降级 → 降状态+记盲区；门 fail 原因同时写进 plan `gates` 与 learning-record，不宣布完成。

## 结课条件

G1–G5 全 pass（`PRACTICE`/`REVIEW`/`MOCK` 的 G2 写「豁免」同样算 pass）才能宣布结课。任一 fail：按各门「不过怎么办」处置；继续、修课或回退诊断，不得因为「内容讲完了」而跳过门。
