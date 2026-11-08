---
name: orbit-analyze-tor
description: "วิเคราะห์ TOR/RFP หรือ customer brief เป็น Step 00 confirmation baseline พร้อม clarity score 9 มิติ, ambiguity triage และคำถามเพื่ออนุมัติ ใช้ก่อนกำหนด scope ไม่ประเมินราคา"
---

# วิเคราะห์ TOR และยืนยันข้อมูลตั้งต้น

ก่อนตัดสินผล action รวมถึงการถามหรือหยุด ให้โหลด dependencies ตาม [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) โดยใช้รายการใน `กฎที่ต้องอ่าน` ด้านล่าง.

## ใช้เมื่อ

ใช้เมื่อได้รับ TOR/RFP, requirement notes หรือ customer brief และต้องแยกข้อเท็จจริงออกจากข้อสงสัยก่อนกำหนด scope รวมถึงการแก้ Step 00 หลังได้รับคำตอบใหม่

## สิ่งที่ต้องเตรียม

เตรียมต้นฉบับพร้อมชื่อไฟล์ revision หรือวันที่ที่ตรวจสอบได้ และวัตถุประสงค์การวางแผน หากมี Step 00 เดิมให้อ่าน approval record และ ID เดิมก่อนปรับแก้

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

1. อ่าน [clarity rubric ฉบับเต็ม](references/tor-rfp-score-guidance.md) แล้วตรวจชนิดต้นฉบับ ข้อความ `.txt`, `.md` หรือ pasted text ใช้ได้โดยไม่ต้องใช้ Docling
2. ถ้าไม่ใช่ข้อความ ให้ใช้ Docling ที่มีอยู่แปลงก่อน บันทึกผลใต้ `output/` และตรวจเทียบกับต้นฉบับ เก็บ original source, converted path, tool และ revision ตาม contract ไม่สร้าง converter ใหม่ หากไม่มี Docling แปลงล้มเหลว หรือยืนยันผลไม่ได้ ให้หยุด ขอ text source หรืออนุญาตดำเนินการภายใต้ข้อจำกัดที่ระบุ ห้ามอ้างว่าอ่านส่วนที่เข้าถึงไม่ได้แล้ว
3. ให้คะแนนทั้ง 9 มิติด้วยหลักฐาน ใช้ 5W1H ตรวจความครบถ้วนภายในแต่ละมิติ ไม่เพิ่มมิติที่สิบ คำนวณค่าเฉลี่ยเลขคณิตและจัดระดับด้วยค่าที่ยังไม่ปัดเศษ แสดงหนึ่งตำแหน่งทศนิยม
4. แยก ambiguity เป็น High, Medium และ Low จัด High ที่ผู้มีอำนาจตอบได้เป็น decision packet พร้อม `DEC-XX`, options, impact, owner และ needed-by ใช้ Type `Integration` สำหรับมติ integration ไม่สร้าง namespace DEC ใหม่
5. บันทึกคำตอบครั้งเดียวใน `Decision_Outcomes` และนำรายการที่ปิดแล้วออกจาก `Open_HighImpact` เก็บ defaults ที่ได้รับอนุญาตพร้อม rationale, impact และ treatment ไม่ถือว่าความเงียบคือการยอมรับ
6. เขียน artifact ตาม schema ทั้งหมด รวม integration inventory เมื่อมี integration, assumptions, source-quality notes เมื่อจำเป็น และ `Step01_Handoff` ตรวจ `Readiness_Check` และเผยแพร่ reviewer view ก่อนภาคผนวก

## ผลลัพธ์และจุดหยุด

สร้างหรือปรับ `output/step_00_confirmation_baseline.md` พร้อม Full Template, Step Summary และ Handoff Note ค่าเฉลี่ยต่ำกว่า 2.0 อนุญาตเพียง ROM หรือ discovery-first ไม่ใช่ fixed commitment และ action นี้ยังไม่คำนวณ MD

หยุดที่ `approve Step 00` หรือ `revise Step 00: ...` พร้อมตัวเลือก `stop` การอนุมัติทำให้ไฟล์พร้อมเป็น input ของ action ถัดไป ไม่สั่งรัน Step 01 เอง Router อาจรับคำสั่ง continuous mode แต่ห้ามข้าม quality gate

## ตัวอย่างคำขอ

"ช่วยวิเคราะห์ TOR นี้เป็น Step 00 แสดงความชัดเจนทั้ง 9 มิติ และรวบรวมเรื่องที่ต้องยืนยันก่อนกำหนด scope"
