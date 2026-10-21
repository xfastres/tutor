# Workspace 指南

创建、迁移或修改教学 workspace 时读本文件。每课的读写顺序见 `RUNBOOK.md`。

## 结构

```text
WORKSPACE.yaml              # 元数据：timezone、locale、skill、protocol、migration
MISSION.md
RESOURCES.md
GLOSSARY.md                 # 推荐
NOTES.md                    # 只放偏好与运营备忘
REVIEW-QUEUE.md             # 定向复习项，唯一调度事实源
KNOWLEDGE-STATE/<id>.yaml   # 每个能力一个文件
evidence/LNNNN.yaml         # 原子证据：一课一文件，课末一次写
learning-records/NNNN-*.md  # 决策级记录
lessons/NNNN-slug.plan.md   # Agent 侧：课型、teaching_block、矩阵、答案钥匙、考官计划、门记录
lessons/NNNN-slug.html      # 学习者侧：讲解页（可课前，无答案）或复习页（考官后）
lessons/INTERVIEW-NOTES.md  # tutor 侧：面试题完整四段答案、追问、常见错答、fact-check
reference/<id>.html         # 压缩后的可复用知识
INTERVIEW-BANK.md           # 真实面试题库：来源、可信度、关联 S/facet、使用记录
exercises/                  # 可选：摸底卷、题库
assets/                     # lesson.css、theme.js、practice.js（从 skill 拷贝）
```

workspace 是持久状态。一个 workspace 一个使命；并行多个不相关主题用多个 workspace，跨 workspace 只通过链接衔接，不复制知识状态。

## 每类事实只写一处

| 事实 | 唯一位置 | 其他地方只能 |
|---|---|---|
| 时区、协议版本、迁移状态 | `WORKSPACE.yaml` | — |
| 为什么学、S id、环境 | `MISSION.md` | 链接 |
| 考官结论（decision / target / probes） | 该课 `learning-records/` | KS 只记 `last_examined` |
| 某能力现在什么状态、facet、misconceptions、used_in | `KNOWLEDGE-STATE/` | 引用 id |
| 什么时候复习什么、完成了没 | `REVIEW-QUEUE.md` | `review_ref` 指针 |
| 学习者做了什么、支撑程度 | `evidence/` | 引用 EV id |
| 真实面试题、来源、可信度、使用情况 | `INTERVIEW-BANK.md` | 引用 IQ id |
| 讲解块、矩阵、答案钥匙、门记录 | `lessons/*.plan.md` | 不复制 |
| 发生了什么持久变化、Decision、下一步 | `learning-records/` | 链接 |
| 课的矩阵、答案钥匙、考官计划 | `lessons/*.plan.md` | 不复制 |
| 规范用语 | `GLOSSARY.md` | 遵循 |
| 可信来源 | `RESOURCES.md` | 引用 |
| 学习者偏好、运营备忘 | `NOTES.md` | — |

违反示例：NOTES 里维护一张「课序与状态」表、根目录进度文件复制 due 日期、每日日志重复写 Decision。这些都会在第二次写入时漂移。需要总览时，从 KS + RQ 读，不另存。

## 文件职责

- **MISSION.md**：指南针。为什么、可观察成功标准（稳定 S id）、约束（含目标环境与只读/沙箱环境）、范围。追加 S id 只需在对话确认一句并在 learning-record 记一行；改 Why/范围才算改使命，需确认。
- **RESOURCES.md**：已审核来源。知识先落这里再进教学。面试/考核类使命的 Wisdom 栏至少一条真实题源。
- **GLOSSARY.md**：学习者理解之后再收词。
- **KNOWLEDGE-STATE/**：每个能力的当前状态、facets、证据摘要、弱点、链接、复习指针。按 `KNOWLEDGE-STATE-FORMAT.md`。
- **REVIEW-QUEUE.md**：定向复习项。按 `REVIEW-QUEUE-FORMAT.md`。会话开始先看 `REPAIR：` 项（不看日期），再看到期/相关项。
- **evidence/**：原子证据，一课一个文件 `evidence/LNNNN.yaml`（如 `L0013.yaml`），课末一次写入；一课内所有 EV 放同一文件，EV id 全局唯一。按 `EVIDENCE-FORMAT.md`。旧的多文件命名 `EV-NNNN-MMMM-<lesson>.yaml` 自 v9.1 起停用。
- **learning-records/**：只为「持久且影响决策」的变化写。按 `LEARNING-RECORD-FORMAT.md`。
- **lessons/*.plan.md**：写课前写；含课型、`teaching_block`、预算、五道门记录位；考官后补 X 探测结果与盲区变化。模板见 `lesson-design.md` §12.3。
- **lessons/*.html**：学习者页面。**讲解页**（可课前生成，只含讲解与案例，不含答案）；**复习页**（考官后生成，含学习者真实错误与纠正）。离线课件模式在课前生成并带导出。
- **INTERVIEW-BANK.md**：真实面试题库。按 `INTERVIEW-BANK-FORMAT.md`；题面给学习者，完整答题要点放 plan 侧，不泄题。每课末补 2–4 题，下节课口述取 1 题，每 3 课模拟面抽题。
- **reference/**：课程产出的压缩知识；不要把整节课复制进去。
- **NOTES.md**：偏好（答题风格、验收方式、偏好的业务类比）与运营日志（“10-10：v9 迁移完成”）。不放状态。
- **assets/**：首次创建时把 skill 的 `assets/lesson.css`、`theme.js`、`practice.js` 拷贝进来。HTML 在样式表之前加载 `theme.js`。同仓库多个 workspace 可用 `@import` 引 skill 的规范样式，相对路径按深度重算。

## ID 与命名

| 对象 | 文件名 | 对话/文档中引用 |
|---|---|---|
| 课 | `lessons/0008-covering-index.html` / `.plan.md` | `L0008` |
| 学习记录 | `learning-records/0012-lesson0008-examiner.md` | `LR0012` |
| 复习项 | — | `RQ-0010` |
| 证据 | `evidence/L0013.yaml` | `EV-0087` |
| 面试题 | — | `IQ-0007` |
| 验证 | — | `VER-0003` |
| 任务 | — | `0008-P3`、`0008-R0a`、`0008-E1`、`0008-X1`、`RQ-0010-R1` |
| 能力 | `KNOWLEDGE-STATE/covering-index.yaml` | `covering-index` |
| 使命标准 | — | `S7` |

课、学习记录、复习项三套序号各自独立，所以只说「0008」会歧义；提到时带前缀。

## WORKSPACE.yaml

workspace 根目录唯一的元数据文件：

```yaml
timezone: Asia/Shanghai
locale: zh-CN
skill: tutor          # 使用的 skill 目录名
protocol: v9.1        # 遵循的协议版本
platform: cursor      # cursor | dsh | other
migration: done       # pending | done；pending 时先过迁移清单
last_ev: 0            # 已分配的最大 EV 编号；下一课从这里 +1 开始
```

`YYYY-MM-DD` 的到期判断用该 timezone；完整 ISO 8601 尊重自身 offset；未声明时先补齐，不猜本地日期。`last_ev` 用于 EV 编号连续性校验。

## 写入纪律

1. 写文件前读对应 FORMAT 文件。
2. 持久状态写入前重新读取事实源；避免用陈旧快照覆盖。
3. 状态、证据、队列之间用稳定 id 关联，不用自然语言名称当引用键。
4. 不为「接触过」写记录；不在每节课重建共享资产。
5. 课程要能独立打开；引用紧贴事实性论断。
6. 一次更新内保持一致：活动 RQ 完成/失败与 `review_ref` 更新是同一逻辑写入。
7. **课末一次写**：evidence 一课一文件、plan 进度与门记录、KS、RQ、LR、INTERVIEW-BANK 在结课时集中写；不每答一题写一次文件（v9.1 起）。

## 课程排序

不要求单独的大纲文件。顺序来自：`MISSION + 学习记录 + KS/facets + 摸底或题库 + ZPD`。避免无视学习者证据的死板大纲。

## 从 v9.0 迁移到 v9.1

第一次用 v9.1 打开旧 workspace 时做一次，记一行到 NOTES 运营日志：

```text
[ ] WORKSPACE.yaml：protocol 改 v9.1；补 last_ev（取现有最大 EV 编号）
[ ] evidence/：新课改一课一文件 evidence/LNNNN.yaml；旧的多文件保留不迁移
[ ] 新课的 plan：补 课型 / teaching_block / 预算 / 五道门记录位 / 复用旧知 行
[ ] KNOWLEDGE-STATE/*.yaml：补 expression 维度（没有 interview 证据就写 unknown）
[ ] 建立 INTERVIEW-BANK.md（按 INTERVIEW-BANK-FORMAT.md），先补 2–4 道历史相关题
[ ] MISSION.md：补「面试线」一节（S-I1…），只追加不重编号
[ ] NOTES.md：偏好区补「先讲后练」「四段式口述」；运营区记 v9.1 迁移
[ ] REVIEW-QUEUE.md：普通项 > 4 时按 MEMORY-ENGINE 合并/转 R0 候选/推迟
[ ] 旧 HTML：不重写；下次触及时拆讲解页/复习页
```

## 从 v8.x 迁移到 v9

第一次用 v9 打开旧 workspace 时做一次，记一行到 NOTES 运营日志：

```text
[ ] WORKSPACE.yaml：补 skill / protocol / migration 三个字段；完成后把 migration 改为 done
[ ] assets/lesson.css 若用 @import 引 skill 样式：路径指向 .cursor/skills/tutor/assets/lesson.css
[ ] KNOWLEDGE-STATE/*.yaml：删除 review: 块，改为 review_ref（指向活动项或 null）
[ ] KNOWLEDGE-STATE/*.yaml：已有的 examiner_result 块保留为历史，不再追加；新课的考官结论写 learning-record
[ ] KNOWLEDGE-STATE/*.yaml：为每个能力补 2–6 条 facets；已有证据的标 ok/decayed，其余 untested
[ ] KNOWLEDGE-STATE/*.yaml：补 mission_ids
[ ] evidence/：缺 assistance 的历史条目不改写；在 KS 摘要里标 (legacy)，不用于新的升级
[ ] REVIEW-QUEUE.md：活动项 > 4 时按 MEMORY-ENGINE 合并/转 R0 候选/推迟
[ ] NOTES.md：删掉课序/状态表，只留偏好与运营日志
[ ] 已有 lessons/*.html：不重写；下一次触及该课时把矩阵与答案钥匙移到 .plan.md
[ ] assets/：拷贝 practice.js；旧 predict.js 可被替代（practice.js 兼容 .predict 与 .semantic-check 标记）
[ ] MISSION.md：为已开但没有 S id 的能力追加 S id
```
