---
name: size-effort
description: "ประเมิน Raw MD จาก atomic subfeature และ approved WBS พร้อม QA แบบ test-case-based และสร้าง Estimate/Review คู่ revision เดียวกัน ตรวจ calibration และ arithmetic โดยไม่รวม PM หรือ pricing"
---

# ประเมิน Raw MD และตรวจ sizing คู่กัน

ใช้ [วิธีอ่านร่วม](../principle-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อ Step 03.3 อนุมัติแล้ว และต้องการ Raw MD ตาม role/bucket หรือแก้ sizing baseline พร้อม companion review ไม่ต้องเรียก review skill แยก

## กฎที่ต้องอ่าน

อ่าน [contract ฉบับเต็ม](references/contract.md) รวม templates, gates และ appendices พร้อม principles ต่อไปนี้ตามวิธีอ่านร่วม ใช้ไฟล์ที่อ่านครบแล้วและไม่เปลี่ยนซ้ำได้.

- [หลักฐานและ traceability](../principle-evidence-and-traceability/SKILL.md)
- [การอนุมัติแต่ละ revision](../principle-explicit-approval/SKILL.md)
- [Baseline และ scenarios](../principle-baseline-and-scenarios/SKILL.md)
- [เอกสารสำหรับผู้ตรวจทาน](../principle-reviewer-first/SKILL.md)
- [Writing style](../principle-reviewer-first/references/writing-style.md)
- [Planning เท่านั้น ไม่ทำ pricing](../principle-planning-not-pricing/SKILL.md)
- [ตรวจสอบก่อนเผยแพร่](../principle-verify-before-publish/SKILL.md)
- [การนับ effort และ role boundaries](../principle-effort-accounting/SKILL.md)
- [Role boundary reference](../principle-effort-accounting/references/roles.md)
- [Risk และ reserve boundaries](../principle-risk-and-reserve/SKILL.md)
- [Estimation calibration](../principle-effort-accounting/references/estimation-calibration.md)

## สิ่งที่ต้องเตรียม

อ่าน `output/step_03_03_wbs_baseline.md`, `output/step_03_02_backlog_inventory.md`, `output/step_03_01_feature_inventory.md` และ approved architecture/integration artifact พร้อม revision ที่อนุมัติ ถ้า WBS ยังไม่อนุมัติ ให้หยุด

เส้นทาง `output/` และ input artifacts อ้างจาก working project ไม่ใช่โฟลเดอร์ skill ส่วน Markdown links อ้างจาก installed skill นี้

## ขั้นตอนทำงาน

1. ยืนยัน SG1-only หรือ SG1+SG2, seniority, warranty, inventory assumptions, QA basis และ confidence บันทึกค่าจริงใน Approved Inputs Consumed ค่าเริ่มต้นคือ 1 MD = 8 ชั่วโมง และประสบการณ์ 3-5 ปี
2. กำหนด sizing Cx เป็น L/M/H จาก implementation scope ก่อนให้ MD อย่าแปลง inventory S/M/C เป็น L/M/H โดยอัตโนมัติ สร้างหนึ่ง baseline row ต่อ approved FN-XX.NN พร้อม short name และ UI/API/INT refs ไม่ใช้ grouped ranges
3. แยก feature SG1/SG2, integration และ non-dev buckets ให้ shared work มีเจ้าของ sizing เพียงหนึ่งจุด เพิ่ม DE, DBA, Change หรือ specialist columns ตาม WBS ใน detail, summaries และ handoff ห้ามซ่อน effort ใต้ role อื่น
4. คำนวณ QA จากจำนวน test cases × MD/case โดย default S=0.1, M=0.2, C=0.4 ครอบคลุม functional, regression, integration และ UAT support นับแต่ละ case ครั้งเดียว ไม่คำนวณ QA จาก FE+BE ซึ่งใช้เป็น sanity check เท่านั้น
5. ไม่ใส่ PM, phasing, timeline, staffing, adjusted effort หรือ contingency ใน Step 04 รวม warranty เป็น non-dev row แยกโดย default หากยกเว้นต้องมีเหตุผลตรงกันทั้งคู่ SG2/AFN ที่ไม่อยู่ฐานต้องไม่เข้า Raw Grand Total, ROM หรือ handoff
6. สร้าง role/bucket summary, feature-only Surface Rollup, SG1-only view และ ROM ±25% จากฐานเดียวกัน แล้วทำ Review พร้อม QA reconciliation, inventory cross-check, calibration, scenario-only scope cuts และ Arithmetic Quality Gate ครบทุกแถว
7. ถามประเด็นผลกระทบสูงไม่เกิน 5 ข้อผ่าน ask tool หรือ chat fallback เมื่อแก้ตัวเลขให้ correction sweep ทั้งสองไฟล์และบันทึก Correction Log ห้ามเผยแพร่เป็น baseline ที่ผ่าน gate หาก mandatory check ไม่ผ่าน

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้ `output/step_04_sizing_estimate.md` และ `output/step_04_sizing_review.md` พร้อมกันเท่านั้น ทั้งคู่ต้องมี revision, date, Approved Baseline Scope, Approval State และ Approval Basis ตรงกัน พร้อม companion links ใช้ Handoff Note ใน Estimate เป็น canonical numeric block และเก็บ Review เป็น technical companion หยุดที่ `approve Step 04` หรือ `revise Step 04: ...` ส่งต่อให้ [plan-resources](../plan-resources/SKILL.md) โดยไม่รันต่อเอง

Approval ต้องผูกกับ revision ที่ตรวจจริง ความเงียบไม่ใช่ approval และ `use defaults` ใช้ได้เฉพาะ gate ปัจจุบัน แม้มี continuous authorization ก็ห้ามข้าม quality gate ทำเฉพาะ action นี้แล้วหยุด มีเพียง router ที่อนุญาต action ถัดไปได้ ไม่ขอหรือคำนวณ rate card, cost หรือราคา

## ตัวอย่างคำขอ

> ประเมิน Raw MD จาก Step 03 ที่อนุมัติแล้ว รวม warranty แยกแถว และส่ง Estimate กับ Review ที่ reconcile กันให้ตรวจ
