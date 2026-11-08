---
name: principle-orbit-risk-and-reserve
description: "Use when Orbit assigns contingency, selects a commitment range or separates resource constraints from external uncertainty."
---

# Risk and reserve

## ใช้เมื่อ

ใช้ใน Step 06 และการรายงานความเสี่ยง. อ่าน exact formulas, ranges และ 23 final checks ใน [Risk contract](../orbit-assess-risk/references/contract.md) เมื่อต้องคำนวณหรืออนุมัติ baseline.

## ความไม่แน่นอนต้องมีชื่อ

Contingency ทุกส่วนต้องผูกกับ named uncertainty, affected workstream, rationale และ treatment. ไม่มี unexplained padding. Trace กลับไป RSK, ASM, DEC, requirement หรือ integration ที่เกี่ยวข้อง.

Risk register ของ workflow นี้มีสอง themes เท่านั้น.

1. `Integration / External Dependency`.
2. `Requirement Unconfirmed`.

Staffing, ramp-up, scarce skills, productivity shortfall และ PM allocation เป็น resource constraints ภายใน. ไม่นำมาเพิ่ม external-risk contingency เว้นแต่มี external driver ที่ระบุหลักฐานได้.

## แยก allowances

| รายการ | วิธีใช้ |
|---|---|
| Expected risk MD | Probability × effort impact ของ named external risk |
| Recommended Contingency | Expected risk MD และ named residual adjustments ที่ไม่ซ้ำกัน |
| Selected Commitment Uplift | ส่วนเพิ่มจาก P50 ไปยัง selected P50/P75 view |
| Delivery Contingency | Recommended Contingency + Selected Commitment Uplift |
| Management Reserve | Sponsor-controlled reserve สำหรับ unknown-unknowns. แยกจาก delivery จนกว่าจะ release |
| Scenario Delta | Scope หรือทางเลือกที่ยังไม่อนุมัติ. ไม่ซ่อนใน contingency |

ห้ามคิด uncertainty เดียวทั้งใน Raw work, rework/buffer, expected risk และ residual adjustment ซ้ำ. Warranty อยู่ใน support/resource baseline ไม่ใช่ commercial reserve.

## Commitment ต้องส่งมอบได้

P25/P50/P75/P90 เป็น planning heuristics จนกว่าจะมี documented probabilistic model. อย่าอ้าง statistical coverage จากชื่อ percentile อย่างเดียว.

Step 06 ไม่เปลี่ยน Step 05 duration เอง. Duration delta ต้องมี named critical-path driver และแสดงเป็น scenario. ถ้า contingency/uplift ยังไม่มี staffed capacity ให้ขอ upstream resource revision หรือรายงาน feasibility finding. ห้ามเรียก commitment-ready จากการบวก MD สำเร็จอย่างเดียว.

บันทึก selected basis, reserve policy, approval และ change triggers พร้อม owner/action. Sponsor policy ที่อ้างอิงได้มีสิทธิเหนือ reference defaults.
