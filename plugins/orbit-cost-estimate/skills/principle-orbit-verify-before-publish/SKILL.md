---
name: principle-orbit-verify-before-publish
description: "Use before publishing Orbit planning artifacts, workbook formulas or architecture diagrams as verified outputs."
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
| Final baseline | ประเมินครบ 23 rows ใน [Step 06 contract](../orbit-assess-risk/references/contract.md) เป็น Pass/Warning/Fail พร้อม evidence |
| Workbook | ตรวจ VAL-01 ถึง VAL-14 ตาม [workbook contract](../orbit-prepare-workbook/references/contract.md). Reconcile VAL-01 ทุก role × bucket และ VAL-08 ทุกสมการแยกจาก ordering. รัน [verifier CLI](../orbit-export-workbook/references/contract.md#independent-workbook-verifier) หลัง final recalculation กับ XLSX ที่ส่งจริง พร้อม report และ input hashes |
| Diagram | Nodes/edges ตรงกับ source, XML valid, embedded assets, PNG size และภาพที่ render จริงผ่าน layout checklist |

## ข้อจำกัดที่ต้องรายงาน

- Validator ตรวจโครงสร้างเอกสารไม่ใช่การตรวจ estimate, stakeholder approval หรือ Excel results.
- XLSX ที่เขียนสูตรสำเร็จยังไม่มีผลคำนวณยืนยัน. ใช้ Excel/LibreOffice เมื่อมี แล้วรัน verifier กับไฟล์ที่ save/recalculate ครั้งสุดท้าย. ถ้าไม่มี ให้ระบุ `Not recalculated`, รัน verifier และคง missing-cache warnings. เมื่อ input/config/workbook เปลี่ยน ต้องสร้าง report ใหม่.
- Verifier เปรียบเทียบ numeric expectations กับ formulas/cached values จริง ไม่ใช่ formula evaluator และไม่ตรวจ semantics ทุกข้อ. คง independent source review ของ atomicity, acceptance, readiness, actor/system ของแต่ละ operation และ source revision. Approval ให้ใช้ assumption ไม่ใช่ evidence ว่า Confirmed.
- ตรวจ installed font และ glyph ไทย/อังกฤษที่ใช้ แล้ว inspect workbook/rendered pages หลัง layout adjustment ครั้งสุดท้าย. Row-height estimate และ font config ไม่รับประกันว่าไม่มี clipping. ถ้า inspect ไม่ได้ ให้ระบุ `Not visually verified` พร้อมข้อจำกัด.
- ถ้าไม่สามารถ export หรือ inspect PNG ให้รายงาน `SVG-only` และ PNG checks เป็น `Not verified`. อย่าอ้างว่าผ่านครบ.
- Formula-like source text ที่ขึ้นต้นด้วย `=`, `+`, `-` หรือ `@` ต้องผ่าน safe literal handling หรือ labelled nonformula text. ห้ามให้ข้อมูลต้นทางกลายเป็น executable spreadsheet formula โดยไม่ตั้งใจ.

## เมื่อพบปัญหา

บันทึก finding พร้อม evidence, severity, action และ baseline impact. สำหรับ workbook ใช้ [canonical warning disclosure](../orbit-prepare-workbook/references/contract.md#402-tbl_validation_summary) พร้อม finding key, row/cell, expected/actual, source และ rationale/action. ส่งต่อ `Fail > Warning > Pass` จากแถวถึง validation summary, README และ final handoff. ห้าม suppress Warning/Fail เพียงเพราะมีไฟล์ output, มี rationale หรือผู้ใช้อนุมัติให้เดินต่อ. Failed mandatory gate หยุด advancement. ตรวจซ้ำหลังแก้ artifact เจ้าของและ affected downstream views.
