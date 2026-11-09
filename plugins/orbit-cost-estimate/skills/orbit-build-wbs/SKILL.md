---
name: orbit-build-wbs
description: "สร้าง dev และ non-dev WBS จาก backlog/inventory ที่อนุมัติแล้ว พร้อม atomic subfeature mapping, role ownership, DoD และ milestone sequence โดยไม่ใส่ MD หรือ timeline"
---

# จัด WBS จาก backlog ที่อนุมัติแล้ว

ใช้ [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อ Step 03.2 อนุมัติแล้ว และต้องการ work packages ที่พร้อมส่งให้ sizing โดยรักษา ownership และ atomic traceability

## สิ่งที่ต้องเตรียม

อ่าน `output/step_03_02_backlog_inventory.md` พร้อม approved revision เป็น controlling input อ่าน feature และ architecture เฉพาะส่วนที่ controlling input อ้างถึง หากยังไม่อนุมัติ ให้หยุดและขอ upstream approval

เส้นทาง `output/` และ input artifacts อ้างจาก working project ไม่ใช่โฟลเดอร์ skill ส่วน Markdown links อ้างจาก installed skill นี้

## กฎที่ต้องอ่าน

อ่าน [contract ฉบับเต็ม](references/contract.md) รวม templates, gates และ appendices พร้อม principles ต่อไปนี้ตามวิธีอ่านร่วม ใช้ไฟล์ที่อ่านครบแล้วและไม่เปลี่ยนซ้ำได้.

- [หลักฐานและ traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [การอนุมัติแต่ละ revision](../principle-orbit-explicit-approval/SKILL.md)
- [Baseline และ scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [เอกสารสำหรับผู้ตรวจทาน](../principle-orbit-reviewer-first/SKILL.md)
- [Planning เท่านั้น ไม่ทำ pricing](../principle-orbit-planning-not-pricing/SKILL.md)
- [ตรวจสอบก่อนเผยแพร่](../principle-orbit-verify-before-publish/SKILL.md)
- [การนับ effort และ role boundaries](../principle-orbit-effort-accounting/SKILL.md)
- [Role boundary reference](../principle-orbit-effort-accounting/references/roles.md)

## ขั้นตอนทำงาน

1. ยืนยัน Approved Baseline Scope เดิม ตรวจ integration gaps, count flags และ blockers โดยไม่เปลี่ยน feature grouping หรือเอา deferred OS เข้าฐาน
2. จัด WBS ตาม 11 domains ใน contract ใช้ SG1 `1.X.XX` และ SG2 `2.X.XX` แยก scenario-only ชัดเจน งานต้อง estimable แต่ห้ามใส่ days, MD, points, t-shirt size หรือ capacity percentage
3. กำหนด owner role และ deliverable ให้ dev/non-dev packages รวม DE, DBA และ specialist ตาม approved scope อย่าซ่อนงาน specialist ใต้ BE หรือ DevOps ให้ shared screen/API implementation มีเจ้าของ WBS เพียงหนึ่ง package
4. สร้าง §5.1 หนึ่งแถวต่อ atomic subfeature โดยเพิ่มเฉพาะ BI-ID, WBS refs และ coverage เก็บ outcome/acceptance ที่ Step 03.1 และ SG/SCR/API/INT refs ที่ Step 03.2 คง blocker ที่ยังไม่ปิด
5. บันทึกเฉพาะข้อแตกต่างจาก Default DoD และ milestone sequence M0-M8 ไม่ใส่วันที่หรือระยะเวลา ระบุ exclusions/hand-offs รวม training, hypercare, warranty, hardware/license และ change management
6. ตรวจ scope/INT traceability และ screen/API coverage ระบุ Missing อย่างเปิดเผย PM packages ส่งให้ Step 05 sizing ส่วนทุก non-PM package ต้องมี Step 04 sizing owner
7. ถามประเด็นผลกระทบสูงไม่เกิน 5 ข้อผ่าน ask tool หรือ chat fallback ปรับ mapping, summary และ handoff ให้ตรงกัน แล้วตรวจ Internal Review

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้เฉพาะ `output/step_03_03_wbs_baseline.md` ตาม Full Template พร้อม reviewer view และภาคผนวก หยุดที่ `approve Step 03.3` หรือ `revise Step 03.3: ...` ส่ง refs ให้ [orbit-size-effort](../orbit-size-effort/SKILL.md) แต่ไม่เริ่ม sizing เอง

Approval ต้องผูกกับ revision ที่ตรวจจริง ความเงียบไม่ใช่ approval และ `use defaults` ใช้ได้เฉพาะ gate ปัจจุบัน แม้มี continuous authorization ก็ห้ามข้าม quality gate ทำเฉพาะ action นี้แล้วหยุด มีเพียง router ที่อนุญาต action ถัดไปได้ ไม่ขอหรือคำนวณ rate card, cost หรือราคา

## ตัวอย่างคำขอ

> สร้าง WBS จาก Step 03.2 ที่อนุมัติแล้ว แยก shared work และ specialist owners โดยยังไม่ใส่ effort
