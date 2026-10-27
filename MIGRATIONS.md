# 迁移（Migrations）

只在 `WORKSPACE.yaml` 的 `protocol` 比当前 skill 版本旧、或 `migration: pending` 时读本文件。从旧到新按顺序做；后面版本的规则覆盖前面的（例如 v9.4 起面试模式默认关：v9.1 清单里「补面试线」「建 INTERVIEW-BANK」两项，除非学习者要求面试训练，否则跳过）。所有迁移都不改写历史 Evidence / KS / RQ，不重审历史课。

## 从 v9.4 迁移到 v9.5

无结构迁移，不改历史。`MISSION.md` 约束可加一行「沙箱提议」（`MISSION-FORMAT.md`）；新课 plan 的「面试口述」行写开场或 E-F 之一，「真实上下文」行写来源或「无：原因」。已排好的未开课 plan 若同时排了开场口述和 E-F，开课前删掉其一。

## 从 v9.3 迁移到 v9.4

无结构迁移，**不改历史 Evidence / KS / RQ**。`WORKSPACE.yaml` 的 `protocol` 可改 `v9.4`（不改也不追溯）。新课 plan 多一行 `教学深度`。面试模式按 `MISSION-FORMAT.md` 解释已有 MISSION：已有 `S-I*` 或非「不适用」的面试安排 → 保持启用；本节缺失且无 `S-I*` → 视为关闭，不要补写面试线。新课按入口路由与深度档走；历史课不重审。

## 从 v9.1.x 迁移到 v9.3

无结构迁移。`WORKSPACE.yaml` 的 `protocol` 改 `v9.3`；EV 多一个可选的块式 `corrected`（见 `EVIDENCE-FORMAT.md`）；新课 plan 多「过线行」列、「开胃预测」与「真实上下文」两行；`MISSION.md` 可加「真实上下文」一节（按 `MISSION-FORMAT.md`，第一次开课时问学习者一句即可）。历史课、历史 EV、历史决策一律不按新版重审。

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
