---
name: orbit-cost-estimate
description: "Plan software delivery from TOR/RFP through scope, architecture, effort, resources and risk. Use for ประเมินโครงการ, continue estimation, or selecting an Orbit planning action. Excludes costing and pricing."
---

# Orbit cost estimate

ชุดนี้ช่วยทีม pre-sales และ delivery วาง planning baseline จาก TOR/RFP. ประเมิน scope, effort, duration, resources และ risk. ไม่คำนวณราคาหรือต้นทุนทางการเงิน.

ใช้ skill นี้เมื่อยังไม่แน่ใจว่าจะเริ่ม action ไหน หรือต้องการเดินหลายขั้นต่อกัน. ถ้ารู้สิ่งที่ต้องทำและมี approved inputs แล้ว ให้เรียก action นั้นโดยตรงได้.

## เริ่มอ่านตรงไหน

1. เลือกงานจากตาราง actions ด้านล่าง.
2. เปิด `SKILL.md` ของ action นั้นเพื่อดู input, ขั้นตอนและ output.
3. โหลด principles ที่ action ระบุ และอ่าน contract เต็มก่อนสร้างผลงาน.
4. ใช้ reference เพิ่มเฉพาะเมื่อ action ต้องใช้ rubric, defaults หรือ tooling นั้น.

ทุก action อยู่ระดับเดียวกันในชุด skills. ลิงก์ในเอกสารอ้างจากตำแหน่ง skill ที่ติดตั้ง. Paths ใต้ `output/` หมายถึง working project ของผู้ใช้ ไม่ใช่ directory ของ skill.

## เลือก action

| ต้องการทำอะไร | Action | Input ที่ต้องมี | Output หลัก |
|---|---|---|---|
| ตรวจ TOR และข้อที่ต้องถาม | [orbit-analyze-tor](../orbit-analyze-tor/SKILL.md) | TOR/RFP, requirement notes หรือ customer brief | `output/step_00_confirmation_baseline.md` |
| กำหนด scope และข้อจำกัด | [orbit-define-scope](../orbit-define-scope/SKILL.md) | Approved Step 00 และ source evidence | `output/step_01_intake_scope.md` |
| เสนอ architecture และ integrations | [orbit-design-architecture](../orbit-design-architecture/SKILL.md) | Approved Step 01 พร้อม Step 00 | `output/step_02_architecture_constraints.md` |
| แตก functional features | [orbit-inventory-features](../orbit-inventory-features/SKILL.md) | Approved scope และ architecture | `output/step_03_01_feature_inventory.md` |
| สร้าง backlog และ inventory | [orbit-build-backlog](../orbit-build-backlog/SKILL.md) | Approved feature inventory | `output/step_03_02_backlog_inventory.md` |
| แตก work packages และ owners | [orbit-build-wbs](../orbit-build-wbs/SKILL.md) | Approved backlog พร้อม supporting evidence | `output/step_03_03_wbs_baseline.md` |
| ประเมิน Raw MD | [orbit-size-effort](../orbit-size-effort/SKILL.md) | Approved WBS และ feature/backlog detail | `output/step_04_sizing_estimate.md` และ `output/step_04_sizing_review.md` |
| วางทีมและ delivery schedule | [orbit-plan-resources](../orbit-plan-resources/SKILL.md) | Approved Step 04 ทั้งสองไฟล์และ WBS/dependencies | `output/step_05_resource_plan.md` |
| สรุป risk และ planning baseline | [orbit-assess-risk](../orbit-assess-risk/SKILL.md) | Approved Step 05 และ upstream evidence | `output/step_06_risk_contingency.md` |
| เตรียม workbook ให้คนตรวจ | [orbit-prepare-workbook](../orbit-prepare-workbook/SKILL.md) | Approved Step 01–06 หรือ explicit draft-export authorization | `output/estimation_workbook.md` |
| แปลง workbook เป็น Excel | [orbit-export-workbook](../orbit-export-workbook/SKILL.md) | Workbook Markdown และ authorization ให้ export | `output/estimation_workbook.xlsx` |
| วาดภาพ architecture | [orbit-draw-architecture](../orbit-draw-architecture/SKILL.md) | Approved architecture artifact | SVG และ PNG ตาม diagram contract |

## Workflow และจุดหยุด

Planning pipeline เดินตามลำดับ Step 00, 01, 02, 03.1, 03.2, 03.3, 04, 05 และ 06. แต่ละขั้นมี review gate ของตัวเอง. Step 06 เป็นขั้นสุดท้ายของ planning.

Workbook เป็น reporting workflow แยก. เตรียม Markdown ก่อน แล้วรอ review/authorization ก่อน XLSX เว้นแต่มี `generate both` แล้ว. Diagram ทำได้เมื่อ architecture พร้อม ไม่ต้องรอ sizing หรือ risk.

1. อ่านคำขอและตรวจ artifacts ที่มีอยู่. ตรวจ source revision, approval และ relevant details ตาม action contract.
2. หากผู้ใช้ระบุ action ให้เลือก action นั้น. ถ้า prerequisites ไม่ครบ ให้แจ้ง artifact หรือ decision ที่ขาด. ห้ามสร้าง approval หรือข้าม upstream checks.
3. หากผู้ใช้ขอ continue ให้เลือกขั้นถัดจาก approved artifacts ที่ตรวจแล้ว. อย่าใช้ filename หรือการมีไฟล์เป็นหลักฐานอนุมัติ.
4. ก่อนทำงาน โหลดกฎร่วมด้านล่างและกฎเพิ่มตาม action. หลักฐาน unchanged ที่อ่านแล้วใน session ใช้ซ้ำได้.
5. ให้ action ผลิตเฉพาะ output ของตัวเองและตรวจ mandatory gates. เมื่อ action ส่งกลับ router จะตัดสินใจว่าจะหยุดหรือไปขั้นถัดไปตาม authorization.
6. ถ้าไม่ได้รับ `run all steps continuously` ให้หยุดที่ review gate. หากได้รับ ให้เดินต่อได้เฉพาะเมื่อ quality gates ผ่านและบันทึก Approval Basis/assumptions/defaults แล้ว. ไม่ถือเป็น client หรือ contractual sign-off.
7. เมื่อจบ ให้บอก output paths, revision/approval state, remaining blockers และ action ถัดไปที่เป็นไปได้. ไม่เขียน headline numbers ซ้ำจาก artifact.

## Principles ที่ใช้ร่วมกัน

Principles เป็นกฎตัดสินใจ ไม่ใช่ขั้นตอนสร้าง artifact. Action ที่เรียกโดยตรงต้องโหลด principles ของตัวเอง ไม่ต้องอาศัย router โหลดให้.

| Principle | ใช้ตอนไหน |
|---|---|
| [Evidence and traceability](../principle-orbit-evidence-and-traceability/SKILL.md) | เปลี่ยน source facts, assumptions และ decisions เป็น artifact ที่ย้อนตรวจได้ |
| [Explicit approval](../principle-orbit-explicit-approval/SKILL.md) | ตรวจ inputs, ถาม stakeholder, ใช้ defaults และผ่าน review gates |
| [Baseline and scenarios](../principle-orbit-baseline-and-scenarios/SKILL.md) | เลือก scope, แยก scenario และจัดการ re-baseline |
| [Effort accounting](../principle-orbit-effort-accounting/SKILL.md) | แตก WBS, sizing, roles, capacity และ warranty |
| [Risk and reserve](../principle-orbit-risk-and-reserve/SKILL.md) | คำนวณ allowance และเลือก commitment basis |
| [Verify before publish](../principle-orbit-verify-before-publish/SKILL.md) | ตรวจคุณภาพตัวเลข, workbook หรือ diagram ก่อนเผยแพร่ |
| [Reviewer-first output](../principle-orbit-reviewer-first/SKILL.md) | จัด summary, metadata, decision gate และภาคผนวกให้คนอ่าน |
| [Planning, not pricing](../principle-orbit-planning-not-pricing/SKILL.md) | จำกัดขอบเขตทุก action ไม่ให้กลายเป็น costing/pricing |

ก่อน route งานให้อ่าน evidence, approval, baseline, verification, reviewer-first และ planning-not-pricing. โหลด effort-accounting หรือ risk-and-reserve เพิ่มเมื่อเลือกงานในขอบเขตนั้น.

## ข้อมูลที่แต่ละขั้นเป็นเจ้าของ

| ข้อมูล | เจ้าของ |
|---|---|
| Source clarity, confirmed facts และ initial integration IDs | Step 00 |
| Business scope และ constraints | Step 01 |
| Architecture, surfaces และ technical implications | Step 02 |
| Functional outcomes, atomic subfeatures และ Approved Baseline Scope | Step 03.1 |
| Backlog, physical screens, APIs และ inventory counts | Step 03.2 |
| Work packages, owners และ dependencies | Step 03.3 |
| Raw MD และ sizing review | Step 04 |
| Adjusted MD, PM, staffing, duration และ warranty schedule | Step 05 |
| Selected commitment, contingency, reserve และ final snapshot | Step 06 |

ปลายทางอ้างข้อมูลต้นทางด้วย ID และ revision. ห้ามให้ workbook หรือ Step 06 แก้ Raw MD เงียบ ๆ. เมื่อ upstream เปลี่ยน ต้องตรวจ affected downstream views และขอ approval ของ revision ใหม่.

## ตัวอย่างคำขอ

- "ใช้ orbit-cost-estimate วิเคราะห์ TOR ใน docs/requirements.pdf แล้วหยุดที่ Step 00 ให้ตรวจ."
- "ใช้ orbit-size-effort จาก approved artifacts ใน output/ สร้าง Estimate และ Review เป็นคู่."
- "ใช้ orbit-plan-resources จาก Step 04 revision ที่อนุมัติแล้ว อย่าเปลี่ยน Raw MD."
- "ใช้ orbit-prepare-workbook จาก approved baseline แล้วหยุดให้ตรวจ Markdown."
- "ใช้ orbit-export-workbook แปลง output/estimation_workbook.md และรายงานสถานะ recalculation."
- "ใช้ orbit-draw-architecture จาก output/step_02_architecture_constraints.md."

ใน Claude Code เรียก `/orbit-cost-estimate` หรือ action name โดยตรง. ใน pi เรียก `/skill:orbit-cost-estimate` หรือ `/skill:<action-name>`.

## ขอบเขตการติดตั้งและเครื่องมือ

ติดตั้ง suite ทั้ง 21 skills ไว้ระดับเดียวกัน. การเรียก action แยกกันไม่ได้หมายถึงการคัดลอก `SKILL.md` ไฟล์เดียวโดยไม่เอา dependencies ไปด้วย. อ่าน [Agent Skills format](https://agentskills.io/specification) สำหรับโครงสร้างมาตรฐาน.

Core planning ใช้การอ่านและเขียน artifacts. Non-text TOR อาจต้อง Docling ตาม input contract. XLSX ต้องใช้ Python และ dependencies ที่ export skill ระบุ. Diagram ต้องใช้ renderer และ PNG tooling ตาม contract. ถ้าเครื่องมือไม่พร้อม ให้รายงาน blocker หรือ fallback ที่ contract อนุญาต ห้ามอ้างว่างานครบ.

หาก asking tool ไม่มี ให้ถามเป็นข้อความพร้อมตัวเลือก. ไม่บังคับชื่อ tool, model หรือ subagent ของ vendor ใด. งานที่ต้องลำดับ approval ให้ทำตาม artifact dependency แม้ agent จะรองรับ parallel execution.

## สำหรับผู้ดูแลชุด skills

แก้กฎร่วมที่ principle เจ้าของ. แก้ schema, สูตรเฉพาะขั้น และ template ที่ action contract เจ้าของ. เก็บชื่อ artifacts, headings, IDs และ status words ที่ downstream อ้างอิงไว้.

หลักการออกแบบอ้างอิง [pstack](https://github.com/backnotprop/pstack) แต่ชุดนี้ไม่ต้องติดตั้ง pstack เพื่อทำงาน. กฎ engineering ของ pstack ไม่ใช่ prerequisites ของผู้ใช้ Orbit.
