---
name: orbit-inventory-features
description: "จัดทำ functional feature inventory จาก scope และ architecture ที่อนุมัติแล้ว แยก atomic subfeature, SG1/SG2 และ integration refs ก่อนสร้าง backlog โดยยังไม่ประเมิน MD"
---

# จัดทำรายการ feature และ atomic subfeature

ใช้ [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อ scope และ architecture อนุมัติแล้ว และต้องการกำหนดขอบเขต functional feature ก่อนแตก backlog หรือทบทวนการจัดกลุ่ม feature เดิม

## สิ่งที่ต้องเตรียม

อ่าน `output/step_01_intake_scope.md` และ `output/step_02_architecture_constraints.md` พร้อม approved revision ของทั้งคู่ ใช้ TOR/RFP เฉพาะตรวจหลักฐานที่เอกสารเหล่านี้อ้างถึง หากขาดเอกสารหรือการอนุมัติ ให้หยุดและขอให้ทำ upstream action ให้ครบ

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

1. ยืนยัน Approved Baseline Scope เป็น `SG1-only`, `SG1+SG2` หรือ `TBD` และเกณฑ์การจัด SG อย่ารวม optional scope เข้าฐานโดยไม่มีการอนุมัติ
2. ทำ scope-to-feature map และเลือก business-flow หรือ capability grouping ตามหลักฐาน แยก deferred items ด้วย `OS-XX` ต่อจาก Step 01
3. ตรวจ Enterprise Functional Completeness ทั้ง 13 ด้านตาม contract แยก authentication, authorization และ integration boundary รายการที่ไม่มีหลักฐานเป็น assumption หรือ candidate ไม่ใช่ confirmed scope
4. สร้าง `FN-XX` และ `AFN-XX` พร้อม `SUR-XX` แล้วแตกเป็น atomic `FN-XX.NN` หรือ `AFN-XX.NN` หนึ่ง outcome ต่อแถว เก็บ actor, behavior, outcome, acceptance, integration relationship, INT ref และ sizing readiness ใน §1.2 ซึ่งเป็นเจ้าของข้อมูลนี้
5. ย้าย NFR, architecture, support และ delivery work ออกจาก feature inventory บันทึก dataset/record assumptions เป็น estimation-only พร้อม owner และผลกระทบ
6. ถามเฉพาะประเด็นผลกระทบสูงไม่เกิน 5 ข้อผ่าน ask tool หรือข้อความเมื่อไม่มีเครื่องมือ เมื่อ promote AFN ให้จัด FN ID ใหม่พร้อม mapping ห้าม renumber ID เดิม
7. ทำ correction sweep ของ FN/AFN/subfeature/SG/INT/count ทุกจุด ตรวจ Internal Review และจัด reviewer view ไว้เหนือภาคผนวกตาม template

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้เฉพาะ `output/step_03_01_feature_inventory.md` พร้อม Full Template, Step Summary, Handoff Note และ Post-step Review Gate ใช้ `approve Step 03.1` หรือ `revise Step 03.1: ...` แล้วหยุด ไม่สร้าง UI/API inventory, WBS หรือ MD การส่งต่อไป [orbit-build-backlog](../orbit-build-backlog/SKILL.md) ไม่ใช่สิทธิ์ให้รันต่อเอง

Approval ต้องผูกกับ revision ที่ตรวจจริง ความเงียบไม่ใช่ approval และ `use defaults` ใช้ได้เฉพาะ gate ปัจจุบัน แม้มี continuous authorization ก็ห้ามข้าม quality gate ทำเฉพาะ action นี้แล้วหยุด มีเพียง router ที่อนุญาต action ถัดไปได้ ไม่ขอหรือคำนวณ rate card, cost หรือราคา

## ตัวอย่างคำขอ

> ช่วยจัด feature inventory จาก Step 01 และ Step 02 ที่อนุมัติแล้ว แยก subfeature ให้ sizing ได้ และหยุดให้ตรวจ Step 03.1
