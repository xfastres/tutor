# Mission: {主题}

## Why（为什么学）

{1–3 句。学习者追求的具体现实成果。避免「理解 X」；描述学会后生活/工作里会发生什么变化。}

## Success looks like（成功的样子）

- **S1:** {具体可观察的能力}
- **S2:** {另一个可观察的能力}

## Constraints（约束）

- {时间、既有安排、学习偏好、工具等}
- **目标环境/版本：** {技术主题填写数据库、运行时、框架或系统版本；未知时写“待确认”，不要猜测}
- **只读/沙箱实操环境：** {逐个列出可用工具与允许的动作，例如「MCP `user-mysql-td-oa`：只读，允许 EXPLAIN / SELECT ... LIMIT / SHOW」「docker 沙箱：可写」；没有则写「暂不可用」}

## Out of scope（暂不涉及）

- {刻意推迟的相邻主题}

## 成功标准 ID

成功标准使用稳定的 `S1`, `S2`… ID。Knowledge State 通过 `mission_ids` 关联；新增标准只追加，不重编号已有标准。

**追加 vs 修改：** 开一课而现有 S 列表没有对应项时，Agent 在对话里说一句「追加 S7：<一句话能力>」，学习者不反对即追加，并在该课 learning-record 记一行。改 Why、删 S、改范围才算修改使命，需要明确确认并写独立 learning-record。

时区、协议版本等元数据不放本文件，放 workspace 根目录的 `WORKSPACE.yaml`（见 `workspace.md`）。
