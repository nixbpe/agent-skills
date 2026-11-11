---
name: principle-effort-accounting
description: "Use when an estimation action decomposes work, sizes effort, assigns roles or reconciles delivery and warranty capacity."
---

# Effort accounting

## ใช้เมื่อ

ใช้กับ WBS, sizing, resource planning และการตรวจ effort ใน risk/workbook. อ่าน [Role boundaries](references/roles.md) เมื่อกำหนด owner. อ่าน [Estimation calibration](references/estimation-calibration.md) สำหรับ Step 04–06.

## ไม่คิดงานซ้ำ

1. ระบุว่าเป็น feature, integration หรือ non-dev work. Shared implementation มี owning WBS package เดียว. Optional increment แยกจากส่วนที่ baseline ต้องใช้.
2. รักษา approved specialist roles ทุกตาราง. `UX/UI` เป็นชื่อแสดงของ UX และ `DevOps` เป็นชื่อแสดงของ DO ไม่ใช่ role เพิ่ม.
3. QA มาจาก test cases และ MD/case. QA เทียบ FE+BE เป็น sanity check เท่านั้น ห้ามใช้แทนวิธี sizing.
4. PM packages อยู่ใน WBS ได้ แต่ PM effort อยู่ใน Step 05 เท่านั้น. Step 04 Estimate และ Review ต้องไม่มี PM effort.
5. แยก hypercare, warranty support/fix และ warranty standby. นับ effort ครั้งเดียว. Standby availability ไม่ใช่ consumed MD เว้นแต่มี approved reserved-capacity assumption.

## แยก effort กับ capacity

| ค่า | ความหมาย |
|---|---|
| Raw MD | Step 04 effort ก่อน delivery adjustment สำหรับ scope ที่อนุมัติ |
| Adjusted MD | Raw MD + rework + buffer + Step 05-derived PM Base MD. PM buffer ที่อนุมัติรวมใน buffer ครั้งเดียว |
| Nominal MD | FTE-Weeks × working days/week |
| Effective MD | Nominal MD × focus |
| Delivery Baseline | Adjusted MD + selected Delivery Contingency |
| Planning Total | Delivery Baseline + Management Reserve |

Focus ลด available capacity ไม่ลด effort. Rework และ buffer ใช้ Raw MD เป็นฐาน ไม่ compound กัน. PM Base MD มาจาก calendar/governance allocation ก่อน PM buffer และไม่เพิ่มย้อนกลับจาก allocation ที่รวม buffer แล้ว.

Role totals และ sizing bucket totals ต้องเท่ากันตรงตาม Step 04. Step 05 capacity ใช้ tolerance 95–105% ต่อ role และ total. ใช้ demand และ capacity ใน horizon เดียวกัน. Warranty มี schedule แยกหลัง hypercare.

Average FTE เป็น demand เฉลี่ย ใช้ `Adjusted MD ÷ (Weeks × working days/week × focus)` โดย numerator และ denominator อยู่ใน horizon เดียวกัน. แยก delivery กับ warranty. `Allocated average FTE = FTE-Weeks ÷ Weeks` เป็นค่าเฉลี่ย allocation ไม่ใช้แทน Average FTE แม้ coverage อยู่ใน 95–105%. ระบุ horizon และแสดงทั้งสองชื่อให้ชัดเมื่อรายงานคู่กัน.

## การใช้ benchmark

เปรียบเทียบ scope, roles และ buckets เดียวกัน. ห้ามเทียบ FE+BE benchmark กับ Raw Grand Total ที่รวม QA/support/non-dev แล้วอ้างว่า reconcile. Benchmark เท่ากับศูนย์ให้ N/A พร้อมเหตุผล.

Calibration thresholds เป็นสัญญาณให้ตรวจ ไม่ใช่สูตรบังคับปรับ effort. ค่าที่เกิน threshold ต้องมี rationale, assumption/risk/scenario mapping หรือ finding. ห้ามเปลี่ยนตัวเลขที่ถูกต้องเพื่อให้เข้าเกณฑ์.

Exact defaults, QA rates, productivity profiles และสูตรเฉพาะขั้นอยู่ใน action contract. Authorized overrides ต้องอยู่ใน calculation-input section พร้อม source และ impact.
