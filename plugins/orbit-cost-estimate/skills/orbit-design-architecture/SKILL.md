---
name: orbit-design-architecture
description: "ออกแบบ Step 02 architecture และ constraints จาก scope ที่อนุมัติแล้ว พร้อม Surface Map, integration coverage, NFR, options และ complexity score ไม่สมมติ stack หรือ SLA จากตัวอย่าง"
---

# ออกแบบ architecture และข้อจำกัด

ก่อนตัดสินผล action รวมถึงการถามหรือหยุด ให้โหลด dependencies ตาม [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) โดยใช้รายการใน `กฎที่ต้องอ่าน` ด้านล่าง.

## ใช้เมื่อ

ใช้เมื่อมี Step 00 baseline และ Step 01 ที่อนุมัติแล้ว ต้องกำหนด architecture เพื่อส่งต่อ feature inventory โดยไม่เพิ่ม scope หรือคำนวณ effort

## สิ่งที่ต้องเตรียม

อ่าน `output/step_00_confirmation_baseline.md` และ approved revision ของ `output/step_01_intake_scope.md` รวมข้อจำกัดกับคำถามค้าง ใช้ TOR เท่าที่ต้องตรวจ traceability หาก prerequisite ขาดหรือ Step 01 ไม่อนุมัติ ให้หยุดเพื่อทำขั้นตอนต้นทางก่อน

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

1. ตรวจ hosting, deployment, integration contracts, security, compliance และคำถามที่กระทบ architecture รับ clarity score เดิม ไม่ให้คะแนน TOR ซ้ำ
2. ประกาศทุก surface ครั้งเดียวใน §1.1 ด้วย `SUR-XX` ที่คงที่ ใช้ Internal Admin, Public Customer, Internal Dashboard และ Backend / Integration เป็น taxonomy ไม่ใช่ข้อบังคับให้สร้างทุก surface เพิ่ม surface เฉพาะเมื่อ scope รองรับ
3. สรุป Current → Target ทั้ง Business Process, Application, Data และ Infrastructure เสนอ architecture options ไม่เกิน 2-3 ทาง พร้อม recommendation, rationale และ effort impact แบบ L/M/H โดยไม่ประมาณ MD
4. อ่าน [optional architecture profile](references/architecture.md) เฉพาะเมื่อต้องประเมิน candidate นั้น ต้องได้รับการยอมรับของโครงการอย่างชัดเจนก่อนนำค่าไปใช้ ไม่ถือ continuous mode เป็นการอนุมัติ AWS, EKS, microservices หรือ SLA ตัวอย่าง [APO inventory](references/examples/architecture-apo.md) ใช้เพื่ออธิบายเท่านั้น ไม่ยก ID, screen count หรือ scope มาใช้
5. สร้าง Integration Map โดยใช้ INT ID จาก Step 00 ตรวจ coverage ของ SSO/Auth, notification, payment, BI/reporting, file storage, master data และระบบที่ TOR ระบุ ระบุ direction, protocol, volume, complexity, frequency และ status โดยแยก Confirmed, Assumption และ Open
6. ครอบคลุม NFR อย่างน้อย Performance, Availability, Security, Scalability, Retention และ privacy/data protection ระบุค่าจากหลักฐาน หรือเสนอ `Default:` พร้อม impact if false และรออนุญาตก่อนถือเป็น baseline บันทึก technical constraints และ Environment & Release
7. คำนวณ complexity จาก 6 drivers น้ำหนัก 5, 4, 4, 3, 3, 3 และ rating 0-3 ใช้ผลรวม weight × rating หาร 66 จัด Low <33%, Medium 33% ถึง <67%, High ≥67% ด้วยเปอร์เซ็นต์ที่ไม่ปัดเศษ อธิบาย rating ด้วยหลักฐาน
8. บันทึก `DEC-XX` พร้อม owner, treatment, needed-by และ authorized fallback อ้าง OQ ต้นทางแทนคัดลอก ไม่เลื่อนวัน overdue โดยซ่อนประวัติ ตรวจ `Internal Review` และเตรียม Step 03 handoff เป็น work-package candidates ไม่สร้าง WBS เอง

## ผลลัพธ์และจุดหยุด

สร้างหรือปรับ `output/step_02_architecture_constraints.md` พร้อม Full Template, Step Summary และ Handoff Note ใช้ภาษา reviewer ที่ไม่ใส่ชื่อ tool/stack เกิน architecture style กับ hosting ใน summary เก็บรายละเอียดไว้ในภาคผนวก

หยุดที่ `approve Step 02` หรือ `revise Step 02: ...` พร้อมตัวเลือก `stop` ไม่สร้าง feature inventory หรือ diagram เอง Router อาจอนุญาต action ถัดไปหลังผ่าน quality gates เท่านั้น

## ตัวอย่างคำขอ

"ออกแบบ architecture จาก Step 01 ที่อนุมัติแล้ว ตรวจ integration และ NFR ให้ครบ และเทียบทางเลือกโดยไม่สมมติใช้ AWS"
