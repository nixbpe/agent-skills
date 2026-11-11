---
name: principle-evidence-and-traceability
description: "Use when estimation planning turns TOR facts, assumptions or decisions into traceable project artifacts."
---

# Evidence and traceability

## ใช้เมื่อ

ใช้เมื่ออ่าน TOR, บันทึก assumption, ตัดสินใจเรื่อง scope หรือส่งข้อมูลให้ action ถัดไป. หลักฐานหนึ่งรายการมีเจ้าของเดียวและใช้ ID เดิมตลอดโครงการ.

## กฎที่ต้องรักษา

1. แยกข้อเท็จจริงที่มี source ออกจาก `Assumption` และ `Default`. ข้อกำหนดจริงต้องอ้าง TOR/RFP หรือ artifact ที่อนุมัติแล้ว.
2. บันทึก source path พร้อม approved revision. ถ้าเอกสารเดิมไม่มี version ให้ใช้ commit หรือ content hash ที่ตรวจจริง. ห้ามสร้าง approval, วันที่ หรือ revision ขึ้นเอง.
3. Assumption และ decision ที่กระทบ baseline ต้องมี owner, impact if wrong, baseline treatment และ due date. Fallback ใช้ได้เมื่อได้รับอนุญาตตาม [Explicit approval](../principle-explicit-approval/SKILL.md).
4. ให้ข้อเท็จจริงอยู่ในตารางเจ้าของเดียว. ขั้นถัดไปอ้าง ID/section และเพิ่มเฉพาะ delta. การทำ summary, calculation หรือ workbook ซ้ำค่าได้เมื่อมี source และ reconciliation.
5. อย่าถาม decision ที่แก้แล้วซ้ำ. เมื่อได้คำตอบ ย้ายออกจาก open list และบันทึกผลพร้อม evidence ใน decision log.
6. Required section ที่ใช้ไม่ได้ต้องใส่ `N/A — [reason]`. ห้ามปล่อยว่างหรือใช้ placeholder แทนข้อเท็จจริงในผลงานจริง.
7. รักษา actor, สิทธิ์ที่อนุญาต และข้อห้ามของแต่ละ requirement ผ่าน feature, backlog, WBS และรายงาน. อ้าง source ID และข้อจำกัดเดิม แม้หลายรายการใช้ surface เดียวกัน. ห้ามแทน actor เฉพาะรายการด้วย `admin/viewer` หรืออนุมานสิทธิ์จากชื่อ role.
8. เมื่อ source ขัดกัน ให้บันทึก conflict และ decision ที่ต้องแก้ ไม่ขยายสิทธิ์หรือข้ามข้อห้ามเอง. การอนุญาตให้ประเมินไม่ใช่หลักฐานยืนยัน requirement ตาม [Explicit approval](../principle-explicit-approval/SKILL.md).

## ขอบเขตของ IDs

| กลุ่ม | วิธีใช้ |
|---|---|
| `ASM-XX`, `DEC-XX`, `INT-XX`, `NFR-XX`, `DATA-XX` | ใช้ namespace เดียวต่อโครงการผ่าน Step 06. ใช้ ID เดิมสำหรับรายการเดิมและต่อเลขสำหรับรายการใหม่ |
| `REQ-`, `RSK-`, `SCN-` | รักษา requirement, risk และ scenario references ตลอด downstream artifacts |
| `OS-XX` | ต่อเลขร่วมกันจาก Step 01 ถึง Step 03.1. ขั้นถัดไปอ้างรายการเดิม |
| `OQ-XX` | เลขแยกแต่ละ step. อ้างข้ามขั้นต้องระบุ เช่น `OQ-06(Step02)` |
| `FN-`, `AFN-` และ atomic subfeatures | ถ้า AFN ได้รับอนุมัติให้เป็น FN ให้สร้าง FN ใหม่และเก็บ old-to-new mapping ทั้ง feature และ subfeature. ห้าม renumber ของเดิม |
| `SUR-XX` | ใช้ surface IDs จาก approved architecture. ห้ามสมมติว่า backend ต้องเป็น `SUR-04` |

Minimum traceability fields คือ ID, Source, Description, Status และ Scope / Architecture / WBS / Sizing / Risk mappings. Status ใช้ `Confirmed`, `Assumption`, `Open`, `Excluded` หรือ `Scenario`. เติม mapping เมื่อ artifact นั้นพร้อม หรือระบุ N/A พร้อมเหตุผล.

ถ้า schema แยกสถานะกับ baseline treatment ได้ ให้คง `Status = Assumption` และระบุ `Included for estimation` พร้อม ASM/authorization ref ใน treatment. ถ้ามีเพียงช่องเดียว ให้ใช้ `Assumption` พร้อมคำอธิบายการรวมฐาน ไม่ใส่ใน confirmed scope โดยไม่มีหลักฐานยืนยัน.

## สิ่งที่ต้องเห็นในผลงาน

ผู้อ่านย้อนจากตัวเลขหรือข้อสรุปไปหา approved source, assumption หรือ decision ได้. หากยังทำไม่ได้ ให้บันทึก gap และผลกระทบก่อนส่งต่อ.
