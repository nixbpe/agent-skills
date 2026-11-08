---
name: orbit-export-workbook
description: "แปลง estimation_workbook.md ที่ตรวจทานแล้วเป็น Excel ด้วย bundled Python converter พร้อม explicit project config, formula safety, verification และ Not recalculated fallback. ใช้เมื่อขอ continue to xlsx หรือ export workbook หลัง Markdown review gate. ไม่สร้าง estimate ใหม่และไม่คำนวณราคา."
---

# แปลง Markdown ที่ตรวจทานแล้วเป็น Excel

## ใช้เมื่อ

ผู้ใช้อนุญาตให้สร้าง `.xlsx` จาก workbook Markdown revision ที่ระบุแล้ว เช่น `continue to xlsx` หรือ `generate both` ไม่ใช้ action นี้เพื่อสร้าง source planning artifacts หรือแก้ตัวเลข baseline

## สิ่งที่ต้องเตรียม

- `output/estimation_workbook.md` ที่ผ่าน preparation checks และมี review authorization ของ revision ปัจจุบัน
- Approved Step 01-06 artifacts ที่ Markdown อ้างอิง หรือ explicit draft authorization พร้อม watermark และรายชื่อ source ที่ยังไม่อนุมัติ
- Python 3.10 ขึ้นไปและ dependencies ใน [requirements.txt](scripts/requirements.txt)
- Project config ที่ได้จาก [bundled config](scripts/workbook_config.yaml) พร้อม source-derived phase bands จาก Step 05
- Excel หรือ LibreOffice ถ้ามี เพื่อ recalculation และตรวจค่าจริง ถ้าไม่มีต้องใช้ fallback ที่ระบุใน contract

ทุก `output/` อยู่ใน working project ส่วน `scripts/` ใน links เป็น bundled assets ของ installed skill อย่าเปลี่ยน working directory ไปที่ skill เพื่อให้ relative CLI default ทำงาน

## กฎที่ต้องอ่าน

อ่าน [export runtime contract](references/contract.md), [canonical workbook schema](../orbit-prepare-workbook/references/contract.md) และ principles ต่อไปนี้ แม้เรียก action โดยตรง

- [Evidence and traceability](../principle-orbit-evidence-and-traceability/SKILL.md)
- [Explicit approval](../principle-orbit-explicit-approval/SKILL.md)
- [Baseline and scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md)
- [Effort accounting](../principle-orbit-effort-accounting/SKILL.md)
- [Risk and reserve](../principle-orbit-risk-and-reserve/SKILL.md)
- [Reviewer-first](../principle-orbit-reviewer-first/SKILL.md)
- [Planning, not pricing](../principle-orbit-planning-not-pricing/SKILL.md)
- [Verify before publish](../principle-orbit-verify-before-publish/SKILL.md)

## ขั้นตอนทำงาน

1. ตรวจ source approval และ authorization ของ Markdown revision นี้ ถ้าขาด Markdown หรือยังมี mandatory gate ที่ไม่ผ่าน ให้หยุดและระบุ prerequisite ไม่สร้าง estimate ทดแทน ถ้ามี decision ที่ต้องเลือก ใช้ ask tool หรือ numbered chat options เมื่อ tool ไม่พร้อม
2. ตรวจ 10 sheets, table headers, row widths, source rows, A1 formulas และ VAL-01 ถึง VAL-14 ตาม canonical contract อย่าอาศัย `--strict` แทน schema review เพราะมันตรวจเพียง H2 ที่ไม่มี tables
3. สร้าง `output/workbook_config.yaml` จาก bundled config ใส่ phase bands ที่ตรง approved Step 05 และ Markdown metadata ตรวจช่วงสัปดาห์และสีจริง ห้ามใช้ built-in 48-week example หรือแก้ shared config
4. Resolve path ของ installed converter แล้วเรียกจาก working project ด้วย `--input`, `--output`, `--config` และ `--strict` ตาม [runtime CLI](references/contract.md#bundled-runtime-and-paths) ต้องส่ง `--config` เสมอเพื่อไม่อ่าน config จาก directory ผิด
5. ถ้า conversion ล้มเหลว ให้แสดง exit code และ error จริง เก็บ Markdown ไว้ ระบุว่า `.xlsx` เดิมเป็น stale หากมี ห้ามอ้างว่า export สำเร็จจากไฟล์เก่า
6. เปิด workbook จริง ตรวจ sheet order, formula coordinates, cell types, phase bands, timeline fills และ readability สูตรไม่ถูกคำนวณโดย converter ให้ใช้ Excel หรือ LibreOffice ถ้ามี แล้วตรวจผลกับ independent reconciliation
7. หาก recalculation ไม่พร้อม ให้บันทึก `Not recalculated` ใน Markdown และ README พร้อม warnings ห้ามประกาศ formula checks ว่าผ่านเพราะสร้างไฟล์ได้ ทุก content/status ที่ส่งออกต้องมีใน Markdown และต้อง rerun conversion เมื่อ Markdown เปลี่ยน

## ผลลัพธ์และจุดหยุด

ส่ง `output/estimation_workbook.xlsx`, path ของ explicit project config และ conversion provenance พร้อม calculation status, checks ที่ทำจริง และ warnings จากนั้นหยุดให้ผู้ใช้ review ไม่เรียก action ถัดไปเอง

การ export ไม่แก้ baseline, ไม่เพิ่ม commercial fields และไม่ปลด mandatory quality gates ถ้า source ต้องแก้ ให้ระบุ finding เพื่อกลับไป [prepare workbook](../orbit-prepare-workbook/SKILL.md) ไม่แก้เงียบระหว่าง conversion

## ตัวอย่างคำขอ

- "ตรวจ Markdown revision ที่อนุมัติแล้วและ continue to xlsx ใช้ phase bands จาก Step 05"
- "Export workbook นี้ ถ้าไม่มี LibreOffice ให้ระบุ Not recalculated และตรวจ totals แยก"
