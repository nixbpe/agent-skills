---
name: orbit-define-scope
description: "กำหนด Step 01 intake และ scope จาก Step 00 ที่อนุมัติแล้ว แยก confirmed, needs confirmation และ out of scope พร้อม assumptions, constraints และ scope counts โดยยังไม่กำหนด SG1/SG2"
---

# กำหนด intake และขอบเขตงาน

ใช้ [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อ Step 00 ได้รับอนุมัติแล้วและต้องแปลงข้อเท็จจริงกับมติเป็นขอบเขตงานที่ตรวจนับและส่งต่อให้ออกแบบ architecture ได้

## สิ่งที่ต้องเตรียม

อ่าน `output/step_00_confirmation_baseline.md` revision ที่อนุมัติ รวม confirmed decisions, defaults, open items และ `Step01_Handoff` เตรียม TOR หรือหลักฐาน scope ที่อ้างอิง หากไฟล์หาย อ่านไม่ได้ หรือยังไม่อนุมัติ ให้หยุดและระบุว่าต้องทำ orbit-analyze-tor ให้ผ่านก่อน

## กฎที่ต้องอ่าน

อ่าน [contract ของ action นี้](references/contract.md) และ principles ทุกข้อด้านล่างก่อนทำงาน แม้ผู้ใช้เรียก action โดยตรง ไม่ต้องผ่าน router ก่อน

- [หลักฐานและ traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [การอนุมัติและ decision gate](../principle-orbit-explicit-approval/SKILL.md)
- [baseline และ scenario](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [เอกสารสำหรับ reviewer](../principle-orbit-reviewer-first/SKILL.md)
- [planning เท่านั้น ไม่คำนวณราคา](../principle-orbit-planning-not-pricing/SKILL.md)
- [ตรวจคุณภาพก่อนเผยแพร่](../principle-orbit-verify-before-publish/SKILL.md)

ใช้ asking tool ที่ระบบมีสำหรับคำถามแบบตัวเลือก หากไม่มีให้ถามใน chat พร้อมตัวเลือกที่มีหมายเลข ถามเฉพาะเรื่องที่เปลี่ยน scope, effort, timeline, resource, risk หรือ commitment ไม่เกิน 5 เรื่องต่อ gate และไม่ถามมติที่ปิดแล้วซ้ำ

ไฟล์ input และ `output/` อ้างจาก working project ของผู้ใช้ ส่วนลิงก์ references อ้างจาก skill ที่ติดตั้ง ห้ามนำตัวอย่างมาใช้เป็นหลักฐานของโครงการ ห้ามกำหนด SG1/SG2 หรือเพิ่ม Approved Baseline Scope ก่อน Step 03.1

## ขั้นตอนทำงาน

1. ตรวจ approval record ของ Step 00 และรับมติเดิมโดยไม่ถามซ้ำ ยกทุก `Open_HighImpact` มาเป็น Step 01 `OQ-XX` โดยอ้าง `DEC-XX` ต้นทาง พร้อม owner, impact และ needed-by
2. ถามเฉพาะช่องว่างใหม่ที่กระทบ architecture หรือ scope หากขอบเขตยังไม่ชัด เสนอ Core, Full, Phased หรือ Excluded ใน §1.1 เป็น scenario alternatives ไม่ใช่ SG1/SG2 และไม่รวมเข้าขอบเขตที่ยืนยันแล้วโดยอัตโนมัติ
3. บันทึก Project Intake และ business goals 3-5 ข้อ พร้อม KPI หรือ TBD ที่มีเหตุผล จัดรายการใน `In Scope (Confirmed)`, `In Scope (Needs Confirmation)` และ `Out of Scope` ใช้ MoSCoW กับ confirmed scope
4. ใช้ `IS-XX`, `IS-UXX` และ `OS-XX` ให้คงที่ ให้ §3.3 เป็นเจ้าของ deferred/not-doing items และ change triggers เพียงแห่งเดียว รายการที่ยังรอยืนยันต้องมี OQ/DEC/ASM link และ treatment
5. นับ item-count ใน §3.4 ให้รวมเท่ากับ confirmed + needs-confirmation + out-of-scope ไม่ใช้จำนวนนี้เป็น MD, screen หรือ API count หาก count เปลี่ยน ให้ระบุ downstream impact
6. เก็บ assumption ที่หักล้างได้ พร้อม validation signal, disproof trigger, owner และ needed-by ใช้ ASM namespace เดิมจาก Step 00 แยก constraints กับ open questions แล้วจัด Step 02 handoff ให้ระบุ scope basis, integrations, hosting, security, NFR และช่องว่าง
7. ตรวจ `Internal Review` ตาม contract เขียน Step Summary และเรื่องที่ต้องตัดสินใจไม่เกิน 3 เรื่องไว้ก่อนภาคผนวก เก็บตารางทำงานทั้งหมดและ approval metadata

## ผลลัพธ์และจุดหยุด

สร้างหรือปรับ `output/step_01_intake_scope.md` พร้อม Full Template, Step Summary และ Handoff Note ไม่สร้าง architecture, WBS, MD, timeline หรือราคา

หยุดที่ `approve Step 01` หรือ `revise Step 01: ...` พร้อมตัวเลือก `stop` ไม่เริ่ม Step 02 เอง แม้ผู้ใช้เคยอนุญาต continuous mode ให้ router เป็นผู้เลือก action ถัดไปหลัง quality gates ผ่าน

## ตัวอย่างคำขอ

"ใช้ Step 00 ที่อนุมัติแล้วจัด intake scope แยกงานที่ยืนยัน งานรอตัดสินใจ และงานไม่รวม พร้อมตรวจยอด scope count"
