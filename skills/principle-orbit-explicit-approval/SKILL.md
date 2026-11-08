---
name: principle-orbit-explicit-approval
description: "Use when an Orbit action checks prerequisites, asks stakeholder decisions, applies defaults or advances an approval gate."
---

# Explicit approval

## ใช้เมื่อ

ใช้ก่อนเริ่ม action และก่อนส่งต่อ artifact. การเรียก action โดยตรงไม่ยกเลิก prerequisite หรือ quality gate.

## การอ่าน dependencies

ใช้กฎนี้ทั้งผ่าน router และเรียก action โดยตรง ก่อนสร้างผลงาน ถามคำถาม หรือปฏิเสธเพราะ prerequisite ขาด.

1. ระบุรายการไฟล์ที่ต้องอ่านจาก action ที่เลือก ได้แก่ contract, principles ทุกข้อ และ references ที่เงื่อนไขตรงกับงาน. อ่านแต่ละไฟล์ให้ครบ รวม templates และ appendices. ไม่โหลด action อื่นหรือทั้ง suite.
2. อ่านครั้งละหนึ่งไฟล์ด้วยช่วงบรรทัดจำกัด. ถ้าผลถูกตัด ให้ตามอ่านช่วงที่ขาดจริงจนจบ ไม่ถือว่าคำสั่งอ่านสำเร็จแปลว่าเห็นครบ และไม่เดาช่วงที่ถูกละไว้.
3. ใช้ dependency ที่อ่านครบแล้วใน session ซ้ำได้เมื่อ revision/content ไม่เปลี่ยน. ถ้าเปลี่ยน ให้อ่านไฟล์นั้นใหม่. การเห็นชื่อไฟล์หรือ summary ไม่ใช่การอ่านครบ.
4. เก็บ read evidence สั้น ๆ เป็น path, revision/content identity และช่วงที่อ่านครบหรือ reused. แยกไฟล์ที่ขาด/อ่านไม่ได้ แล้วรายงาน blocker ตามหลักฐานนั้น. ไม่คัดลอกเนื้อหา dependencies ลงคำตอบ.
5. เมื่ออ่านกฎครบแล้วจึงตรวจ project inputs ตาม contract และตัดสินว่าจะทำต่อ ถาม หรือหยุด. ถ้า dependency อ่านไม่ได้ ให้รายงานเฉพาะ loading blocker ไม่อ้างว่าได้ตรวจ prerequisite ตามกฎที่ยังไม่เห็น.

## ก่อนเริ่มงาน

1. อ่าน approved inputs ตาม contract ของ action รวม relevant detail rows, approval metadata, blockers และ reconciliation evidence. Summary/Handoff อย่างเดียวแทนหลักฐานเหล่านี้ไม่ได้.
2. ตรวจว่า approval ใช้กับ revision ปัจจุบัน. หากไม่มี input, อ่านไม่ได้ หรือยังไม่ได้อนุมัติ ให้แจ้ง blocker และหยุด action ที่ได้รับผลกระทบ.
3. ถามเฉพาะข้อมูลที่หาไม่ได้จาก source และมีผลต่อ scope, MD, timeline, resource, risk, scenario หรือ commitment. ห้ามให้ผู้ใช้ยืนยันข้อเท็จจริงที่อ่านจาก artifact ได้.

## การถามและการใช้ defaults

| ระดับ ambiguity | การจัดการ |
|---|---|
| High | ถามก่อนอนุมัติขั้นที่ได้รับผล หรือแยก scenario delta. ถ้ามี mandatory blocker ต้องหยุด |
| Medium | บันทึก assumption/default ที่มี rationale, impact และ owner. การใช้ fallback ยังต้องได้รับอนุญาต |
| Low | บันทึก implementation assumption โดยไม่บล็อก workflow หากไม่กระทบ baseline อย่างมีนัยสำคัญ |

ถามไม่เกิน 5 high-impact questions ต่อ step และรวมเป็น gate เดียวเมื่อทำได้. ใช้ asking/question tool สำหรับตัวเลือกจำกัด. ถ้าไม่มี tool หรือคำตอบต้องยาว ให้ถามเป็นข้อความ. Decision packet มี DEC ID, source/context, 2–4 options, baseline impact, owner และ needed-by. ระบุ fallback เฉพาะเมื่อได้รับอนุญาต.

- `use defaults` อนุญาตเฉพาะ gate ปัจจุบัน.
- `run all steps continuously` อนุญาตให้เดิน workflow ที่เหลือต่อเมื่อ quality gates ผ่าน. ต้องบันทึก assumptions/defaults และ Approval Basis ตามคำสั่งนั้น.
- Continuous mode ไม่ใช่ client หรือ contractual sign-off. ห้ามอ้างว่าลูกค้าอนุมัติจากคำสั่งนี้.
- Authorization ให้ประเมินหรือใช้ assumption ไม่ยืนยันว่าข้อกำหนดนั้นเป็นข้อเท็จจริง. คง `Assumption`/`Default` และ ASM ref ไว้ แม้รวมใน planning baseline แล้ว. ใช้ baseline treatment แยกจาก evidence status. เปลี่ยนเป็น `Confirmed` ได้เมื่อมีหลักฐานยืนยันเนื้อหานั้นโดยตรง.
- ความเงียบไม่ใช่ approval. คำถามที่ไม่มีคำตอบไม่อนุญาต fallback.

## เมื่อจบ action

เผยแพร่ Post-step Review Gate หลังตรวจคุณภาพ. แสดงผลลัพธ์สำคัญโดยไม่เขียนตัวเลขซ้ำ, unresolved decisions และ baseline impacts. ใช้ action ตาม contract เช่น `approve Step 04` หรือ `revise Step 04: ...` พร้อม `stop`. เสนอ continuous mode เมื่อยังมีขั้นถัดไปใน workflow. Step 06 เป็น terminal step.

Gate approval ไม่ยกเลิก failed mandatory checks, scenario isolation, arithmetic หรือ verification limitations. เมื่อผู้ใช้สั่ง action เดียว ให้ส่งผลและหยุด. Skill หลักเลือกขั้นถัดไปได้ตาม authorization ที่มี แต่ action ไม่เรียกขั้นถัดไปเอง.

Workbook มี gate แยกหลัง Markdown. เริ่ม XLSX ต่อได้เมื่อมี `generate both`, `continue to xlsx` หรือคำขอ export ที่ชัดเจน. Diagram จบที่ user review.
