---
name: principle-orbit-baseline-and-scenarios
description: "Use when Orbit planning selects scope, changes a baseline, compares options or reports budget and deadline scenarios."
---

# Baseline and scenarios

## ใช้เมื่อ

ใช้เมื่อ scope ยังไม่ชัด, เลือก SG grouping, เปรียบเทียบทางเลือก หรือมีตัวเลข baseline เปลี่ยน. Baseline แต่ละค่าอยู่กับ artifact เจ้าของ ไม่อยู่กับ workbook หรือ summary ที่คัดลอกค่า.

## แยกประเภทก่อนคำนวณ

| Treatment | ความหมาย |
|---|---|
| Baseline | Requirement ที่ยืนยันแล้วหรือ assumption ที่อนุมัติให้รวมใน planning commitment |
| Scenario Delta | ทางเลือกหรือ requirement ที่ยังไม่อนุมัติ. แสดง +MD, +duration และ +risk แยก |
| Exclusion | อยู่นอก scope หรือ future phase. ไม่รวม baseline และบันทึก change-control trigger |
| Discovery Needed | หลักฐานไม่พอสำหรับ sizing ที่มีเหตุผล. ใช้ ROM หรือ discovery-first |

MVP, cap, budget-fit, phased, 4-month และ scope-cut views เป็น scenarios จนกว่าผู้ใช้สั่ง `re-baseline`. Budget หรือ deadline ไม่ทำให้ effort ลดเอง. Clarity score ต่ำกว่า 2.0 ให้ ROM/discovery-first เท่านั้น ห้าม fixed commitment.

## Scope grouping

- Step 00–02 ยังไม่กำหนด SG grouping. แสดง scope alternatives โดยไม่เรียก SG1/SG2.
- Step 03.1 เป็นเจ้าของ `Approved Baseline Scope`. ขั้นถัดไปคงค่าจนกว่าจะมี explicit re-baseline.
- SG2 ไม่ได้แปลว่า excluded เสมอไป. `SG1+SG2` รวม SG2 ที่อนุมัติแล้ว. `SG1-only` ไม่รวม incremental SG2/AFN ใน Raw Grand Total, ROM หรือ resource handoff.
- AFN ที่ยังไม่อนุมัติอยู่ใน assumption/scenario. WBS approval ไม่ได้ promote unresolved scope โดยอัตโนมัติ.
- Shared work ที่ baseline ต้องใช้ให้นับครั้งเดียว. เฉพาะ optional increment เป็น scenario. การตัดงานที่ excluded อยู่แล้วประหยัด baseline MD เท่ากับศูนย์.

## เจ้าของตัวเลข

| ค่า | เจ้าของ |
|---|---|
| Raw MD | Step 04 Estimate และ companion Review |
| Adjusted MD, resource plan และ duration | Step 05 |
| Recommended Contingency, selected P50/P75, Delivery Baseline, Management Reserve และ Planning Total | Step 06 |
| Workbook และ diagram | รายงาน approved sources. ไม่มีอำนาจเปลี่ยน scope หรือตัวเลขต้นทาง |

เมื่อพบตัวเลข upstream ผิด ให้ยก finding หรือขอแก้ action เจ้าของ. ห้ามให้ Step 06 หรือ exporter เปลี่ยน Raw/Adjusted MD เงียบ ๆ.

## เมื่อ baseline เปลี่ยน

แก้ artifact เจ้าของก่อน. ตรวจ Summary, Handoff, Final Planning Baseline Snapshot, scenario tables, workbook sheets และ cross-step references ที่ได้รับผลทั้งหมด. Revision ใหม่ต้องมี approval evidence ของตัวเอง. ถ้ายังแก้ downstream ไม่ครบ ให้ระบุว่า stale และห้ามรายงานว่า baseline พร้อมใช้งาน.
