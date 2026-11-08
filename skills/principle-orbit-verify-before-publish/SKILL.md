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
| Workbook | ตรวจ VAL-01–14, cell references, baseline/scenario separation และ numeric reconciliation ตาม [workbook contract](../orbit-prepare-workbook/references/contract.md) |
| Diagram | Nodes/edges ตรงกับ source, XML valid, embedded assets, PNG size และภาพที่ render จริงผ่าน layout checklist |

## ข้อจำกัดที่ต้องรายงาน

- Validator ตรวจโครงสร้างเอกสารไม่ใช่การตรวจ estimate, stakeholder approval หรือ Excel results.
- XLSX ที่เขียนสูตรสำเร็จยังไม่มีผลคำนวณยืนยัน. ใช้ Excel/LibreOffice เมื่อมี และเทียบกับ independent numeric reconciliation. ถ้าไม่มี ให้ระบุ `Not recalculated`, วิธีตรวจและ limitations.
- อย่าใช้ formula ตรวจว่าช่องไม่ว่างแล้วสรุปว่า atomicity, acceptance หรือ readiness ถูกต้อง. เรื่องเหล่านี้ต้องมี semantic evidence.
- ถ้าไม่สามารถ export หรือ inspect PNG ให้รายงาน `SVG-only` และ PNG checks เป็น `Not verified`. อย่าอ้างว่าผ่านครบ.
- Formula-like source text ที่ขึ้นต้นด้วย `=`, `+`, `-` หรือ `@` ต้องผ่าน safe literal handling หรือ labelled nonformula text. ห้ามให้ข้อมูลต้นทางกลายเป็น executable spreadsheet formula โดยไม่ตั้งใจ.

## เมื่อพบปัญหา

บันทึก finding พร้อม evidence, severity, action และ baseline impact. ห้าม suppress Warning/Fail เพียงเพราะมีไฟล์ output หรือผู้ใช้อนุมัติให้เดินต่อ. Failed mandatory gate หยุด advancement. ตรวจซ้ำหลังแก้ artifact เจ้าของและ affected downstream views.
