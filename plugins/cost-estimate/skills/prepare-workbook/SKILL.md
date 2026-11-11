---
name: prepare-workbook
description: "เตรียม Markdown workbook จาก planning artifacts Step 01-06 ที่อนุมัติแล้ว พร้อม schema 10 sheets, live formula expressions และ traceability เพื่อให้คนตรวจทานก่อนแปลงเป็น Excel. ใช้เมื่อขอเตรียม workbook summary หรือ refresh estimation_workbook.md. ไม่คำนวณราคาและไม่สร้าง .xlsx ใน action นี้."
---

# เตรียม workbook ให้ตรวจทานก่อนแปลง

## ใช้เมื่อ

ต้องการรวม approved planning baseline เป็น `output/estimation_workbook.md` หรือปรับไฟล์นี้หลัง upstream revision เปลี่ยน งานนี้เป็น reporting เท่านั้น ไม่แก้ Raw MD, Adjusted MD, contingency หรือ baseline scope

## สิ่งที่ต้องเตรียม

- Artifacts Step 01, 02, 03.1, 03.2, 03.3, Step 04 Estimate และ Review, Step 05 และ Step 06 ตาม [รายการ source](references/contract.md#2-required-source-artifacts)
- Revision, approval state และ approval basis ของทุก source รวมถึง scope basis และข้อมูลที่ใช้คำนวณจริง
- Step 00 เฉพาะ clarity score, assumptions และ traceability ที่ downstream อ้างถึงแล้ว

ทุก `output/` อ้างอิง working project ส่วน links ใน skill อ้างอิง installed skill

## กฎที่ต้องอ่าน

ใช้ [วิธีอ่านร่วม](../principle-explicit-approval/SKILL.md#การอ่าน-dependencies) กับ [workbook contract](references/contract.md) และ principles ด้านล่าง.

- [Evidence and traceability](../principle-evidence-and-traceability/SKILL.md)
- [Explicit approval](../principle-explicit-approval/SKILL.md)
- [Baseline and scenarios](../principle-baseline-and-scenarios/SKILL.md)
- [Effort accounting](../principle-effort-accounting/SKILL.md)
- [Risk and reserve](../principle-risk-and-reserve/SKILL.md)
- [Reviewer-first](../principle-reviewer-first/SKILL.md)
- [Planning, not pricing](../principle-planning-not-pricing/SKILL.md)
- [Verify before publish](../principle-verify-before-publish/SKILL.md)

## ขั้นตอนทำงาน

1. ตรวจ source และ approval ของ revision ที่จะใช้ หยุดเมื่อขาด prerequisite อนุญาต draft ได้เฉพาะเมื่อผู้ใช้ขอชัดเจน แล้วติด `DRAFT - source artifact not approved` ใน Markdown header และ README control พร้อมรายชื่อ source ที่ยังไม่อนุมัติ
2. ถามเฉพาะ decision ที่กระทบ baseline หรือการส่งออกจริง ใช้ ask tool พร้อมตัวเลือกเมื่อทำได้ ถ้าไม่มี tool ให้ใช้ตัวเลือกใน chat ไม่ถามข้อมูลที่อ่านจาก source ได้
3. สร้าง 10 sheet sections ตามลำดับใน contract คงชื่อ H2, `tbl_*`, headers, IDs และ column order ใส่ real rows ครบทุก sheet แยก baseline, scenarios และ exclusions โดยไม่สร้าง backlog หรือ scope เพิ่ม
4. วางตำแหน่งแถวจริงก่อนเขียนสูตร ใช้ A1 references ที่ resolve แล้ว คิด spacer ระหว่าง tables และ phase-band row ของ resource matrix ด้วย ใช้ `active` สำหรับ task timeline และเก็บ phase labels, week ranges, fills จาก Step 05 เป็น configuration metadata ใน Markdown
5. เขียน sourced literals สำหรับ inputs และ semantic judgments เขียน backtick-wrapped formulas สำหรับ arithmetic และ mechanical checks คง QA test-case inputs, role totals, PM, warranty, selected contingency และ reserve ตาม source. ใช้ actor/system และ source reference ของแต่ละ operation ไม่คัด actor เดียวทั้ง inventory. คง ASM refs และสถานะ Assumption/Default แม้ได้รับอนุญาตให้ใช้ใน baseline
6. ตรวจ formula safety ตาม §5.4 ข้อความที่เริ่มด้วย `=`, `+`, `-`, `@` ต้องไม่ถูกส่งเป็นสูตรโดยไม่ตั้งใจ หยุดเพื่อจัดการ literal อย่างปลอดภัยหรือใช้ textual prefix ที่บอกชัดเจน อย่าใช้ apostrophe escape เป็นหลักประกัน
7. ประเมิน VAL-01 ถึง VAL-14 พร้อม independent numeric reconciliation และ semantic source review ตาม §7. ตรวจ VAL-01 ทุก role × bucket และ VAL-08 ทุกสมการ ไม่ใช้ยอดรวมเดียวหรือ range ordering แทน. ส่งต่อ Warning/Fail จากแถวถึง README พร้อม row/cell evidence และ rationale/action. สูตรยังไม่ได้ recalculation จึงใช้ `Not recalculated` ไม่ประกาศ formula checks ผ่านเพราะเขียนไฟล์ได้
8. รัน [Markdown preflight](references/contract.md#markdown-preflight) กับไฟล์ที่บันทึกแล้ว แก้ทุก Fail ใน Markdown แล้วรันซ้ำจนไม่มี Fail. Preflight ตรวจชื่อแถวบังคับ, row widths, formula-like literals และ disclosure ของ literal Warning/Fail เท่านั้น ไม่แทนขั้น 7. ถ้ารันไม่ได้ ให้รายงาน `Preflight not run` พร้อมเหตุผลใน gate
9. วาง reviewer summary, source revisions, changed-since-last-review และ gate ให้คนตัดสินใจได้ โดยไม่เพิ่ม H2 ที่ converter จะเข้าใจเป็น sheet ใหม่ เก็บ schema 10 sheets ตาม contract และบันทึก approval ของ revision ปัจจุบัน

## ผลลัพธ์และจุดหยุด

ส่งเฉพาะ `output/estimation_workbook.md` พร้อมสถานะ checks และคำขอ review แล้วหยุด เสนอ `approve workbook Markdown`, `revise workbook Markdown: ...`, `continue to xlsx` และ `stop`

ไม่รัน converter ใน action นี้ Preflight อ่าน Markdown อย่างเดียวและไม่สร้าง `.xlsx` คำขอ `generate both` ให้ router เรียก [export-workbook](../export-workbook/SKILL.md) แยกหลัง mandatory gates ผ่าน หรือผู้ใช้เรียก export โดยตรงพร้อม authorization ได้ การอนุมัติไม่ข้าม quality gate

## ตัวอย่างคำขอ

- "เตรียม Markdown workbook จาก Step 01-06 ที่อนุมัติแล้ว ขอ review ก่อนทำ Excel"
- "Refresh estimation_workbook.md ตาม Step 05 revision ล่าสุด แยก scenario ออกจาก baseline"
