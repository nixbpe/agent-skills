---
name: orbit-assess-risk
description: "ประเมิน external risks และจัดทำ final planning baseline ของ Step 06 จาก approved resource plan พร้อม named contingency, P25/P50/P75/P90, management reserve และ cross-step checks ทั้ง 23 ข้อ ใช้เมื่อขอ risk assessment, contingency หรือ final baseline review โดยไม่แก้ upstream effort และไม่ทำ pricing"
---

# ประเมินความเสี่ยงและสรุป planning baseline

ก่อนตัดสินผล action รวมถึงการถามหรือหยุด ให้โหลด dependencies ตาม [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) โดยใช้รายการใน `กฎที่ต้องอ่าน` ด้านล่าง.

## ใช้เมื่อ

ใช้หลังอนุมัติ Step 05 เพื่อประเมินความไม่แน่นอนภายนอกทีมและเสนอ final planning baseline งานนี้รวม final consistency review ไว้ใน Step 06 แล้ว ไม่มี baseline-review action แยก

## สิ่งที่ต้องเตรียม

- Approved `output/step_05_resource_plan.md` พร้อม Adjusted MD, duration, capacity, critical path และ constraints
- `output/step_04_sizing_estimate.md` และ companion `output/step_04_sizing_review.md` พร้อม reconciliation evidence
- Approved Step 03 artifacts, scope และ architecture/integration constraints รวม assumption/decision logs จาก Step 00–05
- Risk appetite, selected delivery basis และ sponsor reserve policy ถ้ามีหลักฐาน

อ่าน revisions, approval metadata และ detail rows ที่จำเป็น ไม่ใช้ Snapshot แทน evidence ถ้า Step 05 ขาดหรือยังไม่อนุมัติ ให้หยุดและขอ prerequisite ผ่าน [orbit-plan-resources](../orbit-plan-resources/SKILL.md) ถ้า upstream numbers ไม่สอดคล้อง ให้ขอแก้ upstream หรือบันทึก finding ห้ามแก้เงียบ ๆ

`output/` และ project artifacts อ้างจาก working project ส่วน bundled references อ้างจาก installed skill นี้

## กฎที่ต้องอ่าน

อ่าน [Risk and final planning baseline contract](references/contract.md) ทั้งหมดก่อนเริ่ม แม้เรียก action โดยตรง สูตร defaults, output schema และ canonical 23 checks อยู่ใน contract นี้ แล้วอ่าน principles ต่อไปนี้ ไม่ต้องเรียก router ก่อน

- [Evidence and traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [Explicit approval](../principle-orbit-explicit-approval/SKILL.md)
- [Baseline and scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [Effort accounting](../principle-orbit-effort-accounting/SKILL.md) และ [estimation calibration](../principle-orbit-effort-accounting/references/estimation-calibration.md)
- [Risk and reserve](../principle-orbit-risk-and-reserve/SKILL.md)
- [Verify before publish](../principle-orbit-verify-before-publish/SKILL.md)
- [Reviewer-first](../principle-orbit-reviewer-first/SKILL.md)
- [Planning not pricing](../principle-orbit-planning-not-pricing/SKILL.md)

อ่าน [risk patterns](references/risk-patterns.md) เฉพาะเมื่อการค้นหา uncertainty ต้องการตัวอย่างเพิ่ม Patterns เป็นคำถามช่วยค้นหา ไม่ใช่ข้อเท็จจริงของโครงการ

## ขั้นตอนทำงาน

1. บันทึก approved baseline และ unresolved assumptions คง Step 04 Raw MD, Step 05 Adjusted MD, duration และ scope ตามต้นทาง ไม่ re-size หรือเปลี่ยน resource plan ใน action นี้
2. รวมคำถามสำคัญไม่เกิน 5 ข้อเป็น gate เดียวเท่าที่ทำได้ ใช้ ask tool เมื่อมี finite choices หรือ chat ถ้า tool ไม่มี ระบุ owner, needed-by และ fallback เฉพาะเมื่อผู้ใช้อนุญาต defaults ถ้าไม่มี blocker ให้ระบุ `No blocking confirmations; proceeding with approved baseline/defaults.`
3. คัดเฉพาะ uncertainty ที่อยู่นอก direct control ของ delivery team จัด register เป็นสอง themes เท่านั้น คือ `Integration / External Dependency` และ `Requirement Unconfirmed` เก็บ internal staffing, productivity และ capacity gaps เป็น Step 05 constraints หรือ validity conditions ไม่ใช่ external risks
4. ถ้า workflow, approval routing หรือ state model ยังไม่ยืนยัน ให้สร้าง standalone Requirement Unconfirmed risk ครบ decision/state lifecycle ตาม contract อธิบาย cause, impact, owner และ mitigation ที่ผู้อ่านเข้าใจได้โดยไม่ต้องเปิด ID อื่น ห้ามเพิ่ม risks เพื่อเติม pattern list และห้ามนับ uncertainty ซ้ำ
5. ใช้ triage 1–3 เพื่อคัด candidates แล้วให้คะแนน register ด้วย P×I แบบ 1–5 คำนวณ Expected MD จาก probability mapping ใน contract สร้าง named contingency adjustments เฉพาะ residual impact ที่ยังไม่ถูกนับ ทุก adjustment ต้องมี driver ID, workstream และเหตุผล
6. คำนวณ P25/P50/P75/P90 ตามสูตรเดิมทั้งหมด ระบุว่าเป็น planning heuristics ไม่ใช่ statistically validated percentiles เลือก P50 หรือ P75 พร้อม decision source แยก Recommended Contingency, Selected Commitment Uplift, delivery Contingency, Delivery Baseline, Management Reserve และ Planning Total ไม่รวม warranty/hypercare ซ้ำ
7. ตรวจ selected commitment capacity ถ้า uplift ยังไม่มีทีมรองรับ ให้ขอ Step 05 revision หรือบันทึก feasibility finding ห้ามเรียกแผนว่าพร้อม commitment ไม่แปลง reserve เป็น calendar duration อัตโนมัติ เก็บ scope-cut/MVP เป็น scenario แยกเฉพาะเมื่อร้องขอ
8. ประเมิน canonical Cross-step Consistency Check ทั้ง 23 แถวเป็น Pass / Warning / Fail พร้อมหลักฐานและ action ห้าม blanket pass และห้ามยุบตารางนี้ตาม output economy บันทึก Findings `F-XX`, severity H/M/L และ baseline impact กำหนด re-estimation triggers พร้อม threshold, action, SLA และ owner
9. คำนวณ arithmetic อิสระและบันทึก Verification Fallback ตาม contract ถ้าเครื่องมือไม่พร้อม ให้ระบุ `Not recalculated` หรือ `Not verified` และคง affected checks เป็น Warning/Fail เมื่อ planning number เปลี่ยนให้ทำ baseline correction sweep ก่อน publish

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้เฉพาะ `output/step_06_risk_contingency.md` ตาม template เต็ม วาง Step Summary, canonical Final Planning Baseline Snapshot, สิ่งที่เปลี่ยน, Warning/Fail, ประเด็นตัดสินใจไม่เกิน 3 ข้อ และ Post-step Review Gate เหนือ `ภาคผนวก` เก็บ risk register, formulas, 23 checks, findings และ verification limitations ครบด้านล่าง

ขอ `approve Step 06` หรือ `revise Step 06: ...` แล้วหยุด นี่คือ terminal planning action แม้อยู่ใน continuous mode ผลลัพธ์ยังเป็น proposed baseline จนมี approval record และ workflow authorization ไม่ใช่ contractual sign-off ห้ามสร้าง commercial costing, rate card หรือ pricing

## ตัวอย่างคำขอ

- "ประเมิน external risks จาก Step 05 แล้วเสนอ P75 และ management reserve แยกกัน"
- "ทำ Step 06 พร้อมตรวจ final baseline ทั้ง 23 ข้อ โดยไม่แก้ Raw MD หรือ Adjusted MD"
