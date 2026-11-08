# Architecture Baseline

Reference only. This file offers an AWS stack candidate and an illustrative APO example; it is not TOR evidence or an approved project baseline. Use it only when consistent with Step 01 and explicitly accepted in Step 02. Label adopted values `Default:` or `Assumption:` with owner, impact, treatment, and needed-by. All MUST/SHOULD rules below are conditional on that acceptance; client policy and approved requirements take precedence. Do not add EKS, microservices, notification events, screens, or contractual SLA merely because they appear here.

## A1. Fixed Baseline Stack

| Layer | Baseline | Rule |
|---|---|---|
| Cloud Provider | AWS | MUST deploy in customer landing zone unless TOR/RFP states otherwise |
| Availability Zone | Multi-AZ, single region | MUST use Multi-AZ for production stateful services |
| Compute | Amazon EKS | DEFAULT container orchestration for application workloads |
| Backend | TypeScript + Hono | DEFAULT API framework; OpenAPI-first |
| Frontend | TypeScript + Next.js | DEFAULT web frontend; App Router; SSR/ISR when useful |
| Relational DB | Amazon RDS for PostgreSQL | MUST enable Multi-AZ, automated backups, PITR |
| Cache / Queue | ElastiCache Redis or Valkey | SHOULD use for cache, session, lightweight queue, or job dispatch |
| Object Storage | Amazon S3 | MUST enable versioning, lifecycle policy, SSE-KMS |
| Observability | OpenTelemetry | MUST emit traces, structured logs, metrics from first deploy |
| IaC | Terraform | MUST use module-based Terraform with remote state and lock |
| Secrets | AWS Secrets Manager / SSM Parameter Store | MUST NOT store secrets in source code or plain env files |
| Network | Multi-AZ VPC | MUST place workloads in private subnets; public ingress only where required |

## A2. Non-Negotiables

- MUST use TLS 1.2+ for all public traffic and internal service traffic where feasible.
- MUST encrypt all persistent data at rest with KMS-managed keys.
- MUST keep application pods stateless; persistence belongs in RDS, ElastiCache, or S3.
- MUST use Terraform for production infrastructure; production ClickOps is prohibited.
- MUST wire OpenTelemetry into Hono, Next.js, and worker processes from day one.
- MUST use least-privilege IAM; EKS pod access to AWS services must use IRSA or equivalent.
- MUST document any stack deviation as an architecture decision.

## A3. Architecture Options

| Option | Name | Use When | Avoid When | Mandatory Traits |
|---|---|---|---|---|
| A | Monolith | Internal tool, back-office app, very small workload, 1-3 backend engineers, <50 concurrent users | Multiple bounded contexts, high async workload, strong isolation needs | Single deployable, one PostgreSQL schema, optional Redis, minimum 2 replicas |
| B | Modular Monolith + Worker + Client/Server | DEFAULT for most medium production systems, 3-8 backend engineers, mixed sync/async workload | More than 8 backend engineers, independent domain teams, strict service isolation | Separate Next.js, Hono API, and Worker deployments; one codebase; module boundaries; schema per module |
| C | Microservices | More than 8 backend engineers, separate teams per bounded context, >1 TB primary DB, strict isolation, special compliance triggers | Chosen only for future flexibility, immature DevOps, unclear domain boundaries | Service per bounded context, database per service, async-first via SQS/SNS/EventBridge, distributed tracing mandatory |

## A4. Decision Logic

Evaluate all gates as review prompts, not automatic escalation. Do not automatically select a higher option because of team size, database volume, PII, certification, or tenant count. Choose the least complex option that satisfies approved isolation, availability, ownership, and release requirements; record the trade-off in Step 02.

### Gate 1 - Team Size & Ownership

| Condition | Decision |
|---|---|
| 1-3 backend engineers, one team, shared release cadence | Option A or B |
| 3-8 backend engineers, one team or 1-2 product teams | Option B |
| More than 8 backend engineers or 3+ product teams | Option C |
| Independent squads with independent release cadence within 6-12 months | TRIGGER Option C review |

### Gate 2 - Data Volume & Domain Complexity

| Condition | Decision |
|---|---|
| 1-2 bounded contexts, <50 GB primary DB at 1-year horizon | Option A can fit |
| 3-8 bounded contexts, 50 GB-1 TB primary DB, logical schema isolation sufficient | Option B |
| 8+ bounded contexts, >1 TB primary DB, sharding by domain, or divergent data lifecycles | Option C |
| Cross-domain transactions require strict immediate consistency | Prefer Option A/B with single DB unless other gates force C |
| Eventual consistency acceptable and domain boundaries are clear | Option C can fit |

### Gate 3 - Compliance & Security

| Condition | Decision |
|---|---|
| No/minimal personal data, internal policy only | Option A or B |
| Standard PII, PDPA, ISO 27001 baseline | Option B |
| Special-category personal data, SOC 2 Type II, strict residency, tenant isolation, or blast-radius isolation requirement | Review required controls and isolation boundaries; Option C only if A/B cannot satisfy them |
| Multi-tenant system with strong tenant isolation guarantee | Option C preferred |

### Tie-Breakers

- DEFAULT is Option B.
- MUST justify any move away from Option B.
- MUST NOT select Option C only for future flexibility.
- MUST verify that the selected option meets the actual forcing requirement.
- MUST record the requirement and accepted trade-off; certification alone does not require microservices.

## A5. NFR Minimums

### Availability

| Metric | Option A | Option B | Option C |
|---|---:|---:|---:|
| Service Availability SLO | 99.5% monthly | 99.9% monthly | 99.95% monthly per service |
| Candidate customer-facing SLA | Best-effort | 99.5% | 99.9% |
| Error budget review | Quarterly | Monthly | Per service with automated alerts |

Customer-facing SLA values are discussion candidates, not contractual promises. Availability must be measured end to end with dependencies and exclusions defined. Multi-AZ alone does not prove the SLO or region-disaster recovery.

### Performance

| Metric | Minimum Target |
|---|---:|
| API request latency p95 | <300 ms |
| API request latency p99 | <600 ms |
| Next.js SSR TTFB p95 | <500 ms |
| Page LCP p75 | <2.5 s |
| Queue pickup latency p95 | <5 s |
| OLTP database query p95 | <50 ms |
| Redis/cache hit latency | <5 ms |

### Recovery

| Metric | Option A | Option B | Option C |
|---|---:|---:|---:|
| RTO | <=4 hours | <=1 hour | <=30 minutes per service |
| RPO | <=1 hour | <=15 minutes | <=5 minutes per service |
| RDS backup retention | 7 days | 14 days | 30 days |
| PITR | Required | Required | Required |
| DR drill cadence | Annual | Semi-annual | Quarterly |

### Scalability

- MUST make all EKS workloads horizontally scalable.
- MUST configure HPA with CPU plus at least one workload metric, such as request rate or queue depth.
- SHOULD use read replicas before write splitting.
- SHOULD vertically scale RDS before sharding unless Option C domain split is already justified.
- MUST keep 30% steady-state headroom at projected peak.
- SHOULD plan 100% burst headroom for known peak events.

### Observability

- MUST trace all critical request paths; high-volume paths may sample but retain at least 1%.
- MUST ingest logs within 30 seconds of emission.
- MUST alert critical breaches within 60 seconds.
- MUST provide RED dashboards per service.
- MUST provide USE dashboards per host or workload group.

## A6. Cross-Cutting Controls

### Observability

- MUST use OpenTelemetry SDK in frontend, API, and worker processes.
- MUST propagate trace context across HTTP and queue boundaries.
- MUST emit structured JSON logs with trace and span IDs.
- MUST deploy an OTel collector per cluster or approved equivalent.

### Email Notification / INT-03

The `INT-03` label and workflow events below belong to the illustrative APO example. In a new project, use its actual INT ID and approved event inventory. Notification, escalation, retries, and admin configuration remain scenario candidates unless sourced or approved.

- MUST treat in-scope email notification as an integration boundary, not only an application utility.
- MUST externalize provider, sender domain, recipient matrix, template variables, retry policy, and delivery-status handling.
- MUST store notification request, provider response, delivery status, retry count, failure reason, and related workflow/request ID for audit evidence.
- MUST support configurable reminder threshold and escalation recipient for approval SLA breach.
- MUST keep template and recipient configuration approval-controlled when self-service admin configuration is enabled.

Workflow event examples belong to the [Illustrative APO inventory](./examples/architecture-apo.md), not the reusable baseline.

### Security

- MUST use IRSA or equivalent pod identity for AWS access.
- MUST enforce deny-by-default network policy where platform supports it.
- MUST scan container images in CI and block critical CVEs for production.
- MUST run SAST and dependency scanning before merge to main.
- MUST store secrets in Secrets Manager or SSM only.
- MUST place WAF in front of public ALB/ingress.
- MUST enforce TLS with modern cipher suites for public endpoints.

### Infrastructure as Code

- MUST define AWS infrastructure in Terraform.
- MUST use reusable modules and versioned module consumption.
- MUST store Terraform state remotely in encrypted S3 with DynamoDB lock or equivalent.
- MUST parameterize environments; no copy-paste environment definitions.
- SHOULD run drift detection at least daily for production.

### Deployment

- SHOULD use GitOps with ArgoCD/Flux or pipeline-driven Helm.
- MUST use rolling updates by default.
- SHOULD use canary or blue/green deployment for tier-1 services.
- MUST emit deployment markers to observability backend.
- MUST test rollback path before go-live.

### Customer Landing Zone

- MUST comply with customer SCPs and account structure.
- MUST forward CloudTrail, VPC Flow Logs, Config, and audit logs to customer central logging where required.
- MUST follow customer hub-and-spoke network pattern if present.
- MUST conform to mandatory tag policy from first deployment.
- MUST document KMS key ownership and cross-account grants.

## A7. Sitemap / Menu Baseline

[Illustrative APO inventory](./examples/architecture-apo.md) is optional and project-specific. Read it only when an APO/menu example is requested; derive actual project screens from approved Step 03.1 scope.

## A8. Validation Checklist

| Tag | Check |
|---|---|
| stack | Cloud provider and landing zone match approved baseline |
| stack | Backend is TypeScript + Hono or deviation is documented |
| stack | Frontend is TypeScript + Next.js or deviation is documented |
| stack | Compute is EKS-based or deviation is documented |
| stack | RDS PostgreSQL is Multi-AZ with backup and PITR |
| stack | ElastiCache Redis/Valkey is Multi-AZ when used in production |
| stack | S3 has versioning, lifecycle, and SSE-KMS |
| stack | Terraform remote state and locking are configured |
| gate | Team size and 12-month team projection evaluated |
| gate | Bounded contexts and ownership model documented |
| gate | 1-year primary DB size projection documented |
| gate | Compliance triggers assessed: PDPA, ISO 27001, SOC 2, sector-specific rules |
| gate | Selected option satisfies approved requirements without automatic escalation |
| gate | Option C is not justified only by future flexibility |
| nfr | Availability SLO meets option minimum |
| nfr | RTO/RPO meet option minimum |
| nfr | Performance targets defined for critical paths |
| nfr | Backup restore drill is planned or completed |
| nfr | Capacity headroom is documented |
| observability | OTel instrumentation exists in frontend, API, and worker |
| observability | RED and USE dashboards exist before go-live |
| security | IRSA or equivalent pod identity is used |
| security | Secrets are not stored in source code or plain env files |
| security | WAF protects public ingress |
| security | SAST, dependency scan, and container scan gate production release |
| deployment | GitOps or pipeline-driven deployment path exists |
| deployment | Rollback path is tested |
| landing-zone | Tagging, logging, SCP, network, and KMS rules match customer landing zone |
| compliance | PII inventory and data classification exist where personal data is involved |
| compliance | Retention and deletion policies are defined |
| compliance | SSO + MFA enforced for human production access |
| compliance | Audit logs are immutable and retained per applicable policy |
| integration | In-scope notification INT ID, provider, sender domain, template variables, recipient matrix, retry, delivery status, and audit evidence are defined |
| integration | Approval workflow email coverage includes submitted, pending next approval, approved by level, final approved, rejected, route back, resubmitted, cancelled/withdrawn, delegated/reassigned/expired, and reminder/SLA breach |
