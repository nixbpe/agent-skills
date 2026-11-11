---
name: plan-resources
description: "วาง resource plan จาก approved Raw MD ของ Step 04 โดยคำนวณ Adjusted MD, calendar-derived PM, weekly FTE, capacity, timeline และ warranty schedule สำหรับ planning เท่านั้น ใช้เมื่อขอจัดทีม วางกำลังคน หรือทำ Step 05 โดยไม่เปลี่ยน sizing baseline และไม่คำนวณราคา"
---

# วางแผนทีมและกำลังการส่งมอบ

ใช้ [วิธีอ่านร่วม](../principle-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ใช้เมื่อมี approved sizing แล้วและต้องแปลง effort เป็นทีม ระยะเวลา และ weekly resource matrix ของ Step 05 งานนี้ไม่ทำ risk range ของ Step 06 และไม่คำนวณต้นทุนหรือราคา

## สิ่งที่ต้องเตรียม

- `output/step_04_sizing_estimate.md` และ `output/step_04_sizing_review.md` ที่อนุมัติเป็น paired revision เดียวกัน พร้อม arithmetic gates ที่ผ่าน
- Approved WBS, bucket breakdown, feature/subfeature basis และ dependencies ที่อ้างจาก sizing
- Project type, target go-live, calendar, staffing constraints, delivery model และ warranty/hypercare treatment

อ่าน approval metadata และ detail rows ที่ใช้คำนวณ ไม่ใช้ Summary/Handoff แทนหลักฐาน ถ้า sizing หรือ review ขาด ไม่อนุมัติ ไม่ตรงกัน หรือมี mandatory gate ที่ไม่ผ่าน ให้หยุดและระบุ prerequisite ที่ต้องแก้ผ่าน [size-effort](../size-effort/SKILL.md)

`output/` และ project artifacts อ้างจาก working project ส่วนลิงก์ bundled references อ้างจาก installed skill นี้

## กฎที่ต้องอ่าน

อ่าน [Resource planning contract](references/contract.md) ทั้งหมดก่อนเริ่ม รวมสูตร ตาราง defaults และ output template แม้เรียก action นี้โดยตรง แล้วอ่าน principles ต่อไปนี้ก่อนทำงาน ไม่ต้องเรียก router ก่อน

- [Evidence and traceability](../principle-evidence-and-traceability/SKILL.md)
- [Explicit approval](../principle-explicit-approval/SKILL.md)
- [Baseline and scenarios](../principle-baseline-and-scenarios/SKILL.md)
- [Effort accounting](../principle-effort-accounting/SKILL.md) พร้อม [role boundaries](../principle-effort-accounting/references/roles.md) และ [estimation calibration](../principle-effort-accounting/references/estimation-calibration.md)
- [Risk and reserve](../principle-risk-and-reserve/SKILL.md)
- [Verify before publish](../principle-verify-before-publish/SKILL.md)
- [Reviewer-first](../principle-reviewer-first/SKILL.md)
- [Planning not pricing](../principle-planning-not-pricing/SKILL.md)

## ขั้นตอนทำงาน

1. บันทึก approved inputs และ Raw MD ทุก role โดยไม่แก้ sizing ยืนยัน scope และแยก delivery ออกจาก warranty ตาม upstream baseline
2. รวมคำถามที่กระทบ baseline ไม่เกิน 5 ข้อเป็น gate เดียวเท่าที่ทำได้ ใช้ ask tool สำหรับตัวเลือกที่ชัดเจน ถ้าไม่มี tool ให้ถามใน chat ใช้ defaults ได้เฉพาะเมื่อได้รับอนุญาต ถ้าไม่มี blocker ให้ระบุ `No blocking confirmations; proceeding with approved baseline/defaults.`
3. เลือก productivity profile จาก contract ตั้ง calendar constants ครั้งเดียว Rework และ Buffer คิดจาก Raw MD แยกกัน ไม่ compound และไม่ใช้ focus ลด Adjusted MD
4. คำนวณ Adjusted MD ราย role โดยคง specialist roles จาก Step 04 สร้าง PM Base MD จาก governance allocation และ calendar บวกเฉพาะ PM buffer ที่อนุมัติ ตรวจ benchmark โดยไม่บังคับ PM ให้เป็นเปอร์เซ็นต์
5. จัด backlog ตาม dependency, critical path, sizing, business priority และ risk ตัดสิน mini-phasing ตาม BUILD duration ใช้ feature group, week range, gate, dependency และ staffed roles ครบทุก mini-phase
6. สร้าง weekly resource matrix เดียวพร้อม Phase Band และ Gantt ที่ใช้สัปดาห์เดียวกัน คำนวณ FTE-Weeks, Nominal MD และ Effective MD แยกกัน แสดง warranty support schedule ต่างหาก ไม่เฉลี่ย warranty standby ปน delivery horizon
7. ตรวจ Effective MD ต่อ Adjusted MD ราย role และรวมให้อยู่ใน 95–105% ทั้ง delivery และ delivery รวม warranty ถ้าไม่ถึงให้แก้ allocation/duration หรือระบุ infeasible ห้ามเปลี่ยน Raw MD เพื่อให้ผ่าน เก็บ staffing constraints ใน matrix notes และ Handoff ไม่สร้าง risk register
8. ทำ Internal Review และคำนวณ arithmetic อิสระตาม contract ถ้า baseline เปลี่ยนให้ทำ correction sweep ก่อน publish พร้อม evidence และข้อจำกัดการตรวจ

## ผลลัพธ์และจุดหยุด

สร้างหรือแก้เฉพาะ `output/step_05_resource_plan.md` ตาม template เต็มใน contract วาง Step Summary, canonical Handoff Note, สิ่งที่เปลี่ยน, Warning/Fail, ประเด็นตัดสินใจไม่เกิน 3 ข้อ และ Post-step Review Gate เหนือ `ภาคผนวก` เก็บ working tables ครบด้านล่าง

ขอ `approve Step 05` หรือ `revise Step 05: ...` แล้วหยุด การอนุมัติไม่ข้าม mandatory quality gate และความเงียบไม่ใช่การอนุมัติ ส่ง handoff ให้ [assess-risk](../assess-risk/SKILL.md) ได้ แต่ไม่รันต่อเอง Router เท่านั้นที่อาจอนุญาต action ถัดไปแยกต่างหาก

## ตัวอย่างคำขอ

- "จัดทีมและ weekly timeline จาก Step 04 ที่อนุมัติแล้ว โดยแยก warranty ออก"
- "ทำ Step 05 และตรวจว่ากำลังคนแต่ละ role รองรับ Adjusted MD หรือไม่"
