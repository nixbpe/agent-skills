---
name: principle-orbit-reviewer-first
description: "Use when Orbit writes a stakeholder-facing summary, decision gate, handoff or final planning baseline."
---

# Reviewer-first output

## ใช้เมื่อ

ใช้กับทุก action เพื่อให้คนอ่านตัดสินใจได้ก่อนเปิด working tables. อ่าน [Writing style guidance](references/writing-style.md) และรักษา contract tokens เดิม.

## ลำดับเอกสาร

วางส่วนต่อไปนี้ก่อน `ภาคผนวก`.

1. Step Summary.
2. สิ่งที่เปลี่ยนจากรอบก่อน.
3. Open decisions ไม่เกิน 3 ข้อที่ผู้ทบทวนต้องตัดสินใจ.
4. Warning/Fail findings พร้อม evidence และ action.
5. Canonical numeric block ของขั้นนั้น ถ้าไม่ได้อยู่ใน Step Summary.
6. Post-step Review Gate.

เก็บ working tables เต็มตาม contract ไว้ในภาคผนวก. Step 04 companion Review เป็น technical view และลิงก์กลับ Estimation reviewer view.

## ตัวเลขมีที่อ้างอิงหลัก

| ขั้น | Canonical numeric block |
|---|---|
| Step 00–03 และแต่ละ Step 03 substep | Step Summary |
| Step 04–05 | Handoff Note |
| Step 06 | Final Planning Baseline Snapshot |

ที่อื่นอ้าง block นี้แทนการเขียน headline numbers ซ้ำ. Calculation inputs, reconciliation และ workbook exports คัดค่าพร้อม source ได้ แต่ต้องไม่กลายเป็น baseline อีกชุด. Review gate บอกผลลัพธ์สำคัญโดยไม่ซ้ำตัวเลข.

Self-check tables สรุป passing checks หนึ่งบรรทัดและทำตารางเฉพาะ Warning/Fail. ข้อยกเว้นคือ Step 06 final checks ต้องแสดงครบ 23 rows. ไม่ตรวจเรื่องเดียวซ้ำหลาย gate ใน artifact เดียว.

แสดง MD และ FTE ด้วยทศนิยมสั้น โดยทั่วไปไม่เกิน 2 ตำแหน่ง ตัดศูนย์ท้ายที่ไม่จำเป็น. คำนวณและตรวจ gates ด้วยค่าความละเอียดเต็ม ไม่ใช้ค่าปัดเศษกลับไปคำนวณ. ถ้า contract ระบุ precision เฉพาะ ให้ใช้ตามนั้น. แสดง ratio เป็นเปอร์เซ็นต์จริง เช่น `0.975` แสดง `97.5%` ไม่ใช่ `0.975%`. รายการราย role ใช้ตารางหรือ `SA 12 MD, BA 8 MD` ไม่แสดง dict/object repr.

## Metadata ของ artifact

- Title ระบุ project และ step.
- Header ใช้ `Source`, `Version`, `Approval State`, `Approval Basis`.
- เพิ่ม `Approved Baseline Scope` ตั้งแต่ Step 03.1. ไม่ assign SG ใน Step 00–02.
- `Source` ระบุ upstream path และ approved revision ข้าง path ไม่แก้ filename เพื่อใส่ revision.
- Step 06 เก็บ version/date ใน Final Planning Baseline Snapshot ไม่สร้าง header record ซ้ำ.
- Step 04 Estimate/Review ต้องมี revision, date, scope และ approval เดียวกัน พร้อม companion links.
- Approval metadata ใช้กับ current revision. Revision date ไม่ใช่ approval date.
- MD unit, seniority, QA rates, warranty treatment และ delivery factors อยู่ใน calculation inputs พร้อม authorized overrides. Conversion provenance ใส่เมื่อมี conversion attempt เท่านั้น.

## ภาษาและความครบถ้วน

เมื่อ source, project context หรือผู้ใช้เป็นภาษาไทย ให้ stakeholder-facing prose เป็นภาษาไทย. คง technical terms, identifiers, headings, formulas และ status words ตาม contract. ใช้ business names ใน executive prose และเก็บ IDs ไว้เมื่อจำเป็นต่อ traceability.

Step 00–05 ส่ง Full Template + Step Summary + Handoff Note เว้นแต่ผู้ใช้เลือก depth อื่นชัดเจน. Step 06 ส่ง Full Template + Step Summary + Final Planning Baseline Snapshot. การย่อ prose ไม่ยกเลิก mandatory evidence หรือ checks.
