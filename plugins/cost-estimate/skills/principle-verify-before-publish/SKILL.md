---
name: principle-verify-before-publish
description: "Use before publishing estimation planning artifacts, workbook formulas or architecture diagrams as verified outputs."
---

# Verify before publish

## ใช้เมื่อ

ใช้ก่อนเผยแพร่ artifact, ขอ approval หรือ export. ตรวจผลงานจริงและบอกข้อจำกัดของวิธีตรวจ.

## ตรวจตามชนิดงาน

| งาน | หลักฐานที่ต้องมี |
|---|---|
| Scope/feature/backlog/WBS | Coverage และ IDs ย้อนถึง approved inputs ได้. Counts ไม่ปน semantic groups กับ physical inventory |
| Sizing | Role totals, bucket totals, QA cases, ROM, drivers และ scenario totals reconcile. Estimate/Review เป็น revision และ approval เดียวกัน |
| Resource | Effective capacity ต่อ role และ total ตรงกับ demand ใน horizon เดียวกัน พร้อม dependencies และ warranty schedule |
| Final baseline | ประเมินครบ 23 rows ใน [Step 06 contract](../assess-risk/references/contract.md) เป็น Pass/Warning/Fail พร้อม evidence |
| Workbook | รัน [Markdown preflight](../prepare-workbook/references/contract.md#markdown-preflight) ก่อน Markdown review gate. ตรวจ VAL-01 ถึง VAL-14 ตาม [workbook contract](../prepare-workbook/references/contract.md). Reconcile VAL-01 ทุก role × bucket และ VAL-08 ทุกสมการแยกจาก ordering. รัน [verifier CLI](../export-workbook/references/contract.md#independent-workbook-verifier) หลัง final recalculation กับ XLSX ที่ส่งจริง พร้อม report และ input hashes |
| Diagram | Nodes/edges ตรงกับ source, XML valid, embedded assets, PNG size และภาพที่ render จริงผ่าน layout checklist |

## Self-review ก่อน review gate

ทำหลังบันทึก artifact และก่อนเผยแพร่ review gate ทุกครั้ง รวม workbook Markdown และ revision ที่สร้างใหม่. ทำไม่เกิน 3 รอบ. หยุดก่อนได้เมื่อรอบนั้นไม่พบประเด็น.

แต่ละรอบเปิดอ่านไฟล์ที่บันทึกแล้วจาก disk. ไม่ตรวจจากความจำ, generator source หรือ diff. ถ้าไฟล์ใหญ่เกินอ่านครบ ให้อ่านส่วนเหนือ `ภาคผนวก` ครบ แล้วระบุช่วงที่อ่านและช่วงที่ตรวจด้วย search เท่านั้น.

| ตรวจ | ผ่านเมื่อ |
|---|---|
| สอดคล้องกับ upstream | Counts, totals, IDs, baseline scope และ revision labels ตรงกับ approved inputs และ artifact ปัจจุบันของขั้นก่อนหน้า. ไม่มีตัวเลขหรือคำอธิบายของ revision เก่า |
| อ่านรู้เรื่อง | ไม่มีประโยคหรือ cell ที่ถูกตัด, placeholder, dict/object repr หรือ ID ที่เรียงสลับ |
| IDs | ส่วนเหนือ `ภาคผนวก` ใช้ ID ตาม [กฎ ID ของ reviewer-first](../principle-reviewer-first/SKILL.md#ภาษาและความครบถ้วน) |
| กระชับ | ผู้ทบทวนตัดสินใจได้จากส่วนเหนือ `ภาคผนวก` โดยไม่ต้องเปิดภาคผนวก. ไม่มีตัวเลขหรือข้อความซ้ำ |

แก้ที่ artifact เจ้าของ แล้ว rerun mechanical checks ที่ได้รับผลก่อนเริ่มรอบถัดไป. ประเด็นที่เหลือหลังรอบที่ 3 ให้บันทึกเป็น Warning/Fail finding.

รายงานใน review gate message: จำนวนรอบ, สิ่งที่แก้, สิ่งที่ยังเหลือ และช่วงที่ไม่ได้อ่าน. ไม่เพิ่มตาราง self-review ใน artifact. ตัวเลขใน message คัดจากไฟล์หลังแก้ครั้งสุดท้าย. Self-review ไม่แทน mandatory checks ของ contract และไม่ใช่ approval.

## เมื่อใช้ script สร้าง artifact

Script เป็น working file ไม่ใช่ deliverable. Output ต้องผ่าน checks เดียวกับ artifact ที่เขียนเอง.

- เก็บ script และ data ใต้ `output/_generators/` ของ working project แล้วบอก path ใน handoff. Temp หรือ scratch directory หายเมื่อจบ session ทำให้ revision ถัดไป regenerate ไม่ได้.
- แยกข้อมูล (rows, counts, MD) ออกจากข้อความ. Prose ที่ขึ้นกับ revision เช่น delivery model, counts และ headline numbers ต้องมาจากข้อมูล ไม่ hard-code ใน script.
- Script เขียนไฟล์เฉพาะเมื่อรันเป็น main. การ import ต้องไม่เขียนทับ artifact.
- เมื่อ revision เปลี่ยน ให้แก้ data แล้ว regenerate จากนั้นทำ [stale sweep](../principle-baseline-and-scenarios/SKILL.md#เมื่อ-baseline-เปลี่ยน).
- Assertion ใน generator ไม่ใช่ independent verification. คง reconciliation แยกตามตารางด้านบน.

## ข้อจำกัดที่ต้องรายงาน

- Validator ตรวจโครงสร้างเอกสารไม่ใช่การตรวจ estimate, stakeholder approval หรือ Excel results.
- XLSX ที่เขียนสูตรสำเร็จยังไม่มีผลคำนวณยืนยัน. ใช้ Excel/LibreOffice เมื่อมี แล้วรัน verifier กับไฟล์ที่ save/recalculate ครั้งสุดท้าย. ถ้าไม่มี ให้ระบุ `Not recalculated`, รัน verifier และคง missing-cache warnings. เมื่อ input/config/workbook เปลี่ยน ต้องสร้าง report ใหม่.
- Verifier เปรียบเทียบ numeric expectations กับ formulas/cached values จริง ไม่ใช่ formula evaluator และไม่ตรวจ semantics ทุกข้อ. คง independent source review ของ atomicity, acceptance, readiness, actor/system ของแต่ละ operation และ source revision. Approval ให้ใช้ assumption ไม่ใช่ evidence ว่า Confirmed.
- ตรวจ installed font และ glyph ไทย/อังกฤษที่ใช้ แล้ว inspect workbook/rendered pages หลัง layout adjustment ครั้งสุดท้าย. Row-height estimate และ font config ไม่รับประกันว่าไม่มี clipping. ถ้า inspect ไม่ได้ ให้ระบุ `Not visually verified` พร้อมข้อจำกัด.
- ถ้าไม่สามารถ export หรือ inspect PNG ให้รายงาน `SVG-only` และ PNG checks เป็น `Not verified`. อย่าอ้างว่าผ่านครบ.
- Formula-like source text ที่ขึ้นต้นด้วย `=`, `+`, `-` หรือ `@` ต้องผ่าน safe literal handling หรือ labelled nonformula text. ห้ามให้ข้อมูลต้นทางกลายเป็น executable spreadsheet formula โดยไม่ตั้งใจ.

## เมื่อพบปัญหา

บันทึก finding พร้อม evidence, severity, action และ baseline impact. สำหรับ workbook ใช้ [canonical warning disclosure](../prepare-workbook/references/contract.md#402-tbl_validation_summary) พร้อม finding key, row/cell, expected/actual, source และ rationale/action. ส่งต่อ `Fail > Warning > Pass` จากแถวถึง validation summary, README และ final handoff. ห้าม suppress Warning/Fail เพียงเพราะมีไฟล์ output, มี rationale หรือผู้ใช้อนุมัติให้เดินต่อ. Failed mandatory gate หยุด advancement. ตรวจซ้ำหลังแก้ artifact เจ้าของและ affected downstream views.
