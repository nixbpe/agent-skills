# Writing Style Guidance

Applies to prose in Step 00-06 outputs: Step Summary, Handoff Note, Final Planning Baseline narrative, and the notes, rationale, impact, and mitigation text inside tables. State the fact, number, or decision directly so a Sponsor or delivery lead can act on it.

## Keep As Is

These are contract tokens, not style. Never rewrite or remove them for readability:

| Token | Reason |
|---|---|
| Headings and section names from each command's Output Contract | Downstream steps and [workbook converter](../../orbit-export-workbook/scripts/md_to_workbook.py) parse them |
| IDs (`REQ-`, `INT-`, `ASM-`, `DEC-`, `RSK-`, `SCN-`, ...), numbers, dates, formulas | Traceability and arithmetic checks |
| Inline code, code blocks, file paths | Machine-readable references |
| Bold field labels such as `**Source**:` and `**Approval State**:` | Output Contract fields |
| `N/A — [reason]` and template placeholder `—` | N/A requires a reason. The standalone placeholder may remain in templates or intentional spacer/total cells, not as a substitute for a required value in generated artifacts. |
| `Assumption:` / `Default:` labels and status words (Confirmed, Assumption, Open, Excluded, Scenario, Pass, Warning, Fail) | Required labels |
| Terms Raw MD, Adjusted MD, Delivery Baseline, Management Reserve, Planning Total | Defined terms in the [effort-accounting principle](../../principle-orbit-effort-accounting/SKILL.md) |

## Avoid In Prose

| Pattern | Example to avoid | Write instead |
|---|---|---|
| Not-X-but-Y contrast | "ไม่ใช่แค่ปัญหา integration แต่เป็นความเสี่ยงของทั้งโครงการ" | State the actual impact: "KPGW spec ล่าช้าทำให้ INT และ QA เลื่อนตาม" |
| Filler transitions | นอกจากนี้, อย่างไรก็ตาม, Additionally, Moreover at the start of every sentence | Start with the subject or the fact |
| Inflated words | ยกระดับ, ครอบคลุมอย่างครบถ้วน, สำคัญอย่างยิ่ง, robust, comprehensive, crucial, seamless, leverage | Name what is covered or why it matters, with the number or ID |
| Stacked qualifiers | "อาจจะมีแนวโน้มที่อาจส่งผล" | One qualifier only where the uncertainty is real, and link it to an `ASM-`/`RSK-` ID |
| Closers that restate | A final sentence that repeats the paragraph | End on the last concrete fact |
| Prose dashes | "Scope — ตามที่ตกลง — ไม่รวม warranty" | Comma, colon, or parentheses (the `N/A —` token is exempt) |
| Decorative bold or emoji | Bold on every bullet label | Bold only contract field labels and totals |
| Chat residue | "หวังว่าจะเป็นประโยชน์", "Let me know" | Remove |

Required summaries, calculation inputs, and workbook exports may repeat sourced values. Keep a source pointer and run the correction sweep after any numeric change; do not delete required inputs merely to avoid repetition.

Do not add facts, sources, owners, or dates while tightening prose. If a sentence needs a detail that is missing, log it as an Open item instead.
