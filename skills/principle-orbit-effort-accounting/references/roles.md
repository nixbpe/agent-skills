## Role Reference

Use these boundaries in Step 03 WBS, Step 04 sizing, and Step 05 capacity. `UX/UI` is the display alias for `UX`; `DevOps` is the display alias for `DO`. Do not treat either alias as an extra role. Carry any approved DE, DBA, Change, or specialist role through every detail/summary/resource table. PM effort belongs to Step 05 only.

| Abbr | Role | ขอบเขตงานสำหรับ Estimation / WBS Ownership |
|---|---|---|
| SA | System Analyst | แปลง requirement เป็น functional specification, system flow, interface specification, data model ระดับ logical/application, API contract และ integration design ระดับ solution. รับผิดชอบความครบถ้วนของ spec เชิงระบบ แต่ไม่รวม implementation, DB tuning หรือ infra setup |
| BA | Business Analyst | วิเคราะห์ business process, current/to-be workflow, business rules, requirement summary, acceptance criteria และ business test scenario สำหรับ UAT. เน้นความถูกต้องของ business need ไม่ลงรายละเอียด technical design |
| UX | UX/UI Designer | ออกแบบ user journey, wireframe, mockup, clickable prototype, UI guideline และ design system/component guideline. ไม่รวม frontend implementation |
| FE | Frontend Dev | พัฒนา UI screens, frontend components, routing, form validation, state management และ integration กับ API จากฝั่ง client. ไม่รวม API business logic หรือ backend data processing |
| BE | Backend Dev | พัฒนา API, business logic, service layer, authentication/authorization logic ระดับ application, data access และ integration adapter ฝั่ง backend. ไม่รวม DBA tuning, CI/CD pipeline หรือ infra provisioning |
| QA | Tester | วาง test plan, test case, test data, execute functional test, SIT support, regression test, defect tracking และ UAT support. Performance test และ security scan ให้นับเป็น QA coordination/basic execution เท่านั้น เว้นแต่มี specialist scope แยก |
| DO | DevOps | จัดการ environment, CI/CD pipeline, build/release process, deployment automation, configuration, monitoring platform และ operational readiness. ไม่รวม backend feature code หรือ business logic |
| PM | Project Manager | วางแผนงาน, schedule, resource coordination, progress tracking, risk/issue management, stakeholder communication, reporting และ governance. ไม่รวมการตัดสินใจเชิง solution หรือ business requirement detail |
| Change | Change Management Lead | วางแผน stakeholder readiness, communication, adoption และผลกระทบจากการเปลี่ยนกระบวนการ ใช้เป็น role แยกเฉพาะเมื่อ WBS และ Step 04 ระบุ effort แยกไว้ ไม่คัดลอก effort เดิมที่อยู่ใน BA/SA |
| DE | Data Engineer | ออกแบบและพัฒนา ETL/data pipeline, data migration scripts, data cleansing/transformation และ migration validation dataset ถ้ามี scope data migration. ไม่รวม DB administration หรือ performance tuning ระดับ database engine |
| DBA | DBA | ดูแล database schema governance, indexing, query tuning, backup/restore, database environment support, migration execution support และ performance troubleshooting ระดับ database. ไม่รวม ETL pipeline หรือ application business logic |

## Role Boundary Guidance

| Boundary | Rule |
|---|---|
| SA vs BA | BA owns business intent, process, rules, and acceptance criteria. SA owns system specification, API/interface design, logical data model, and technical translation. ถ้าเป็น workshop เดียวกัน ให้แยก effort เป็น BA-led business discovery และ SA-led solution/spec elaboration |
| QA vs Security/Performance | QA owns test planning, functional/SIT/UAT/regression, and defect control. Performance/security นับใน QA เฉพาะ coordination หรือ basic execution; formal penetration test, vulnerability assessment, หรือ load-test engineering ต้องแยกเป็น activity ชัดเจนภายใต้ owner ที่เหมาะสม |
| DE vs DBA | DE owns data movement and transformation logic. DBA owns database structure, tuning, operational support, and controlled execution. Migration script = DE; schema/index/performance/backup plan = DBA |
| DO vs BE | BE builds application services and deployable backend code. DO builds the path to deploy, run, and monitor it. Observability instrumentation in code can be BE; monitoring platform, pipeline, environment variables, release automation, and deployment runbook are DO |
