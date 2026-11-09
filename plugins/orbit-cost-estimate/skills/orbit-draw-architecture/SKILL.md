---
name: orbit-draw-architecture
description: "วาด solution architecture diagram จาก approved architecture artifact ด้วย project-local renderer และ source-backed nodes/edges. ใช้เมื่อขอ SVG และ PNG ของ architecture ที่อนุมัติแล้ว พร้อม provider grouping, corridor routing และ actual visual verification. ไม่เปลี่ยน scope หรือ baseline."
---

# วาด architecture จากหลักฐานที่อนุมัติแล้ว

ใช้ [วิธีอ่านร่วม](../principle-orbit-explicit-approval/SKILL.md#การอ่าน-dependencies) กับรายการ `กฎที่ต้องอ่าน`.

## ใช้เมื่อ

ต้องการภาพประกอบ architecture ที่มี approved artifact อยู่แล้ว เช่น Step 02 งานนี้ไม่เลือก architecture ใหม่ ไม่เพิ่ม components และไม่เปลี่ยน scope, effort หรือ baseline

## สิ่งที่ต้องเตรียม

- `INPUT_FILE` เป็น approved architecture artifact พร้อม revision และ approval basis ถ้าไม่ได้ระบุ ให้ค้น working-project `output/` ก่อนถาม
- `ARCHITECTURE` และ `CLOUD_PROVIDER` จาก artifact หรือ explicit arguments ที่ไม่ขัดกับ source
- Runtime สำหรับ project-local renderer เช่น Python 3 ที่ใช้ standard library สร้าง SVG ได้
- SVG viewer หรือ browser สำหรับ offline visual inspection และ `rsvg-convert` สำหรับ PNG ถ้ามี

Neutral vector glyphs เป็นทางเลือกที่ไม่ต้องพึ่ง network ส่วน provider icons ต้องมี provenance และฝังไว้ใน SVG

## กฎที่ต้องอ่าน

อ่าน [diagram contract](references/contract.md) และ principles ต่อไปนี้ก่อนเริ่ม แม้เรียก action นี้โดยตรง

- [Evidence and traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [Explicit approval](../principle-orbit-explicit-approval/SKILL.md)
- [Baseline and scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [Reviewer-first](../principle-orbit-reviewer-first/SKILL.md)
- [Planning, not pricing](../principle-orbit-planning-not-pricing/SKILL.md)
- [Verify before publish](../principle-orbit-verify-before-publish/SKILL.md)

## ขั้นตอนทำงาน

1. Resolve input, pattern และ hosting จาก arguments, user message และ approved source ตามลำดับ ถ้าขาด artifact หรือไม่มี architecture content ให้หยุด ถ้ามี unresolved decision จริง ใช้ ask tool พร้อมตัวเลือก หรือ numbered chat options เมื่อไม่มี tool
2. ทำ inventory ของ actors, boundaries, application/data tiers, cross-cutting services และ external integrations ที่มีหลักฐาน เก็บ node/edge/group mapping พร้อม source section, IDs, direction, protocol และ baseline/scenario treatment ใน `output/solution_architecture_diagram_review.md` บันทึก exclusions โดยไม่เติม components ตามความคุ้นเคย
3. วาง layout จาก inventory ใช้ vertical flow, left cross-cutting strip และ right external column ตาม source วาง route corridors ก่อนสร้าง geometry ห้ามยก project nodes จากตัวอย่างอื่นมาใช้
4. สร้าง `output/render_architecture_diagram.py` หรือ renderer ภาษาอื่นใน working project ให้ใช้ explicit icon/output paths และ source-backed inventory ไม่ต้องสร้าง universal Markdown parser ใช้ neutral glyphs หรือ provider SVG ที่ตรวจ provenance แล้วและ embed ให้เปิด offline ได้
5. สร้าง `output/solution_architecture_diagram.svg` พร้อม legend และ footer ใช้ solid สำหรับ baseline และ dashed สำหรับ optional/future scenario ไม่ใส่ project/client names, ราคา หรือ phases ที่ source ไม่ระบุ
6. Parse SVG เป็น XML แล้วเปิดดูจริงแบบ offline ตรวจทุก checklist item ตาม contract ถ้ามี `rsvg-convert` ให้ export `output/solution_architecture_diagram.png` ที่กว้างอย่างน้อย 2x ตรวจ dimensions จริง ดูทั้งภาพและ cropped quadrants แก้ renderer แล้ว render ใหม่จนผ่าน
7. ถ้าไม่มี `rsvg-convert` ให้ส่ง `SVG-only` และระบุ PNG checks เป็น `Not verified` ถ้าดู SVG จริงไม่ได้ก็ระบุ visual inspection ว่ายังไม่ verified แยกจาก XML check ห้ามอ้าง full completion หรือใช้ PNG เก่าแทนผลรอบนี้

## ผลลัพธ์และจุดหยุด

ส่ง SVG, PNG เมื่อสร้างและตรวจได้จริง, project-local renderer และ review record ที่มี source revision, commands, checklist evidence และข้อจำกัด จากนั้นหยุดให้ผู้ใช้ review ไม่เรียก planning action อื่นและไม่อนุมัติ architecture แทนผู้ใช้

ทุก `output/` เป็น path ใน working project ส่วน [contract](references/contract.md) เป็น bundled reference ของ installed skill

## ตัวอย่างคำขอ

- "วาด SVG และ PNG จาก Step 02 ที่อนุมัติแล้ว ใช้ hosting model ตาม artifact"
- "ทำ architecture diagram สำหรับ on-premises แยก future scenario ด้วยเส้นประ และรายงาน checks ที่ทำจริง"
