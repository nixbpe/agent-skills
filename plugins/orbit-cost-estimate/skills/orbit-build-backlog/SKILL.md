---
name: orbit-build-backlog
description: "แตก feature inventory ที่อนุมัติแล้วเป็น backlog หนึ่ง BI ต่อ atomic subfeature พร้อม UI/API inventory, integration coverage และจำนวน S/M/C โดยไม่สร้าง WBS หรือประเมิน MD"
---

# แตก backlog และ UI/API inventory

ใช้ [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อ Step 03.1 อนุมัติแล้ว และต้องการแปลง atomic subfeature เป็น backlog พร้อม screen/API coverage สำหรับสร้าง WBS

## สิ่งที่ต้องเตรียม

อ่าน `output/step_03_01_feature_inventory.md` เป็น controlling source พร้อม approved revision ใช้ scope, architecture และ TOR/RFP เพียงตรวจ traceability ที่ Step 03.1 อ้างถึง หากยังไม่อนุมัติ ให้หยุดก่อนสร้าง inventory

เส้นทาง `output/` และ input artifacts อ้างจาก working project ไม่ใช่โฟลเดอร์ skill ส่วน Markdown links อ้างจาก installed skill นี้

## กฎที่ต้องอ่าน

อ่าน [contract ฉบับเต็ม](references/contract.md) รวม templates, gates และ appendices พร้อม principles ต่อไปนี้ตามวิธีอ่านร่วม ใช้ไฟล์ที่อ่านครบแล้วและไม่เปลี่ยนซ้ำได้.

- [หลักฐานและ traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [การอนุมัติแต่ละ revision](../principle-orbit-explicit-approval/SKILL.md)
- [Baseline และ scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [เอกสารสำหรับผู้ตรวจทาน](../principle-orbit-reviewer-first/SKILL.md)
- [Planning เท่านั้น ไม่ทำ pricing](../principle-orbit-planning-not-pricing/SKILL.md)
- [ตรวจสอบก่อนเผยแพร่](../principle-orbit-verify-before-publish/SKILL.md)

## ขั้นตอนทำงาน

1. คัดลอก Approved Baseline Scope โดยไม่เปลี่ยน SG รับ enterprise resolution, deferred items, integration boundaries และ data assumptions จาก Step 03.1 ไม่เปิด feature scope ใหม่
2. สร้าง coverage matrix หนึ่ง `BI-XX` ต่อ atomic subfeature เก็บ refs และ blocker เท่านั้น Outcome และ acceptance ยังมีเจ้าของที่ Step 03.1 §1.2 ถ้า readiness ยัง Needs clarification ให้คง blocker และไม่อ้างว่า coverage Complete
3. สร้าง `SCR-XX` ต่อ semantic page หรือ independently operated modal พร้อม in-page activities, Surface, reuse และ S/M/C อย่านับ filter value, responsive variant หรือ menu group เป็น screen ใหม่ ถ้าต้องมี sitemap ให้ทุก SCR อยู่ครั้งเดียว
4. สร้าง API inventory ครบชนิด CRUD/BIZ/INTG/BATCH/FILE/RT ตาม scope พร้อม atomic refs และ INT coverage ใช้ API เดียวสำหรับหลาย consumer พร้อมระบุ Multi-consumer แทนการเพิ่มจำนวนซ้ำ
5. ใช้ inventory complexity S/M/C ตาม Coding Reference ซึ่งต่างจาก sizing L/M/H นับ shared screen/API ครั้งเดียว แยก baseline กับ scenario และอ้าง canonical SCR สำหรับ exact reuse
6. คำนวณ Countable Summary, weighted screen equivalent และ screen:API ratio ตาม contract จำนวนเหล่านี้ไม่ใช่ effort หรือ MD ไม่สร้าง 5W1H ซ้ำใน artifact นี้
7. ถามประเด็นผลกระทบสูงไม่เกิน 5 ข้อผ่าน ask tool หรือ chat fallback แล้วทำ count sync sweep ทุก inventory, coverage, summary และ handoff ตรวจ Internal Review ก่อนเผยแพร่

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้เฉพาะ `output/step_03_02_backlog_inventory.md` ตาม Full Template พร้อม reviewer view และภาคผนวก หยุดที่ `approve Step 03.2` หรือ `revise Step 03.2: ...` ไม่สร้าง WBS, MD หรือ timeline ส่วน 5W1H เป็นของ [workbook contract](../orbit-prepare-workbook/references/contract.md) เท่านั้น ส่งต่อข้อมูลให้ [orbit-build-wbs](../orbit-build-wbs/SKILL.md) โดยไม่รันต่อเอง

Approval ต้องผูกกับ revision ที่ตรวจจริง ความเงียบไม่ใช่ approval และ `use defaults` ใช้ได้เฉพาะ gate ปัจจุบัน แม้มี continuous authorization ก็ห้ามข้าม quality gate ทำเฉพาะ action นี้แล้วหยุด มีเพียง router ที่อนุญาต action ถัดไปได้ ไม่ขอหรือคำนวณ rate card, cost หรือราคา

## ตัวอย่างคำขอ

> แตก Step 03.1 ที่อนุมัติแล้วเป็น backlog และ UI/API inventory ตรวจ shared API และหยุดที่ review gate
