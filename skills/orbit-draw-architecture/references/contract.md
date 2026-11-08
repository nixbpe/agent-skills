# Generate System Diagram

## Inputs (no defaults; resolve every run)

Resolve in order: explicit argument, user's message, approved source artifact, then the available ask tool with selectable options. Use numbered chat choices if that tool is unavailable. Validate requested argument values against the approved source. Reuse explicit source values without another confirmation. Ask once only for a genuine unresolved architecture or hosting decision. Do not ask the user to identify facts already in the artifact.

| Key | Argument | If missing |
| --- | --- | --- |
| `INPUT_FILE` | `input=<path>` | Scan the working project's `output/` for `step_02_*.md` or `*architecture*.md`. Offer candidates and a custom path if the controlling artifact is ambiguous. |
| `ARCHITECTURE` | `architecture=<pattern>` | Read the approved pattern from `INPUT_FILE`. Ask only if multiple patterns remain unresolved. |
| `CLOUD_PROVIDER` | `cloud=aws\|azure\|gcp\|on-premises\|hybrid` | Read the approved hosting model. Use neutral infrastructure glyphs for on-premises and provider-specific groups for hybrid. |

Read the shared principles listed in [the action guide](../SKILL.md) before working. Every `output/` path below belongs to the working project.

## Contract

| Field | Rule |
| --- | --- |
| Purpose | Supplementary diagram of the approved architecture. It never changes scope, MD, baseline or step outputs. |
| Outputs | `output/solution_architecture_diagram.svg`, self-contained with embedded icons and well-formed XML, plus `output/solution_architecture_diagram.png` at least 2x the SVG logical width when PNG tooling is available. |
| Reproduction | A project-local renderer with explicit input inventory, icon/cache and output paths. Record the command and runtime requirements in `output/solution_architecture_diagram_review.md`. |
| Source of truth | Every node, edge and architecture group traces to the approved `INPUT_FILE` revision. Architecture defaults apply only when adopted in that artifact. Examples, vendor catalogs and decorative layout conventions are not project evidence. |
| Content rules | No project/client names in the delivered diagram. No pricing. Approved baseline is solid; optional/future scenario is dashed. A legend and footer are mandatory. Do not invent Phase 1/2 if the source has no phases. |
| Failure | No network means use a verified project-local icon cache or neutral glyphs. Missing provider icon means neutral doc/db/gear/user glyph. No `rsvg-convert` means label the delivery `SVG-only`, report the PNG checklist as `Not verified`, and do not claim full completion. Missing architecture input, missing approval, or no architecture content means STOP. |

## Workflow

1. **Inventory.** Read the approved artifact, its revision and approval basis. Extract actors with volume/auth facts; edge/security; application containers for `ARCHITECTURE`; data tier including DB, replica, cache and queue only when sourced; storage/retention; cross-cutting services such as secrets, keys, observability, email and CI/CD with scans; external `INT-XX` systems with direction, protocol and phase; region/NFR facts. These categories are prompts to look for evidence, not mandatory invented components. Map every included item to a node, edge or group and record exclusions.
2. **Trace.** Write the source-to-diagram inventory in `output/solution_architecture_diagram_review.md`. Record source path/revision, approval basis, selected architecture/hosting, node and group IDs, labels, source section/ID, baseline/scenario treatment and exclusions. For each edge record source node, target node, direction, protocol/meaning, phase when sourced, and source reference. Separate unresolved relationships from approved edges. Do not use generic knowledge to fill an unexplained connection.
3. **Plan.** Lay out only the approved inventory using the layout and connector rules below. Record the chosen bands, provider boundaries, external alignment and route corridors before writing geometry. Use presentation IDs to connect the renderer to the evidence inventory without leaking project/client names into the diagram. If requested overrides contradict the approved artifact, stop for the source decision rather than silently redrawing a different architecture.
4. **Icons.** Prefer verified cached provider SVGs. When network access is available, find an actual provider icon slug through theSVG catalog or its lookup integration, then fetch that verified asset from its CDN to the working project's `output/diagram_assets/icons/`. Do not guess a slug or require a vendor-specific tool. Record asset provenance and applicable license. If unavailable, draw a neutral vector glyph directly in the renderer. Embed the final SVG content or data URI; remove external links, script/event content and remote font/image dependencies so the diagram renders offline.
5. **Generate.** Create `output/render_architecture_diagram.py` or an equivalent project-local renderer using the chosen runtime. Encode the explicit source-backed inventory and project geometry, or load that inventory from a project-local data file. No universal Markdown parser is required. The renderer accepts or clearly defines explicit project-local icon and output paths. Produce SVG with width/height, viewBox, embedded assets, provider groups, labels, orthogonal routed connectors, legend and footer. Escape XML text and attribute values. The standard-library Python path can emit SVG directly with neutral vector glyphs and requires no third-party rendering package.
6. **Validate and export.** Run the project-local renderer, parse the emitted SVG as XML, and inspect it visually. Export PNG at least 2x the SVG width, inspect the full PNG and cropped quadrants against every checklist item, and fix/re-render until those checks pass. Record actual results rather than a blanket pass. Preserve the SVG-only fallback below if PNG tooling is absent.
7. **Present and stop.** Deliver the paths, source revision, rendering command, verification evidence, warnings and `SVG+PNG` or `SVG-only` status. Ask for review and stop. This action does not approve a revised architecture or start another planning action.

## Layout

The diagram uses top-to-bottom system flow, with a cross-cutting strip on the left and external systems on the right. These are placement guides, not a requirement to invent a missing tier or vendor service.

```text
┌ cross-cutting ┐  ┌──── approved provider boundary ────┐  ┌ external ┐
│ LEFT strip   │  │ Users at top, outside boundary     │  │ RIGHT    │
│ sourced      │  │ ↓ sourced edge/public services    │  │ sourced  │
│ shared       │  │ ↓ private application containers  │  │ systems  │
│ services     │  │ ↓ data tier                       │  │ aligned  │
│              │  │ ↓ storage and retention           │  │ to peers │
└──────────────┘  └────────────────────────────────────┘  └──────────┘
```

- Vertical flow is users, edge/public, private application, data, then storage. Omit absent tiers rather than creating them.
- Cross-cutting services occupy the LEFT strip inside their approved cloud/provider boundary. External systems occupy the RIGHT column outside that boundary, row-aligned to their internal counterpart. On-premises and hybrid boundaries follow the approved hosting model.
- Use provider-canonical groups with corner badge and accent color. AWS Cloud is `#242F3E`, VPC `#8C4FFF`, public subnet `#7AA116`, private subnet `#00A4A6`, and EKS `#ED7100`. Azure VNet/subnet uses the `#0078D4` family. GCP VPC/subnet uses the `#4285F4` family. These styles apply only to groups supported by the source.
- Each node has an icon around 46 px, a bold label and a grey sub-label beneath. All label text has a white halo with `paint-order="stroke"`.
- The legend explains solid baseline, dashed scenario and any distinct deployment/control style. The footer identifies the architecture revision and verification status without project/client names or pricing.

## Connectors

- Use orthogonal horizontal/vertical segments only, rounded corners, arrowheads and one neutral connector color. Dashed means optional/future scenario. Deployment/control edges need a separate labelled style so they cannot be confused with scope phasing.
- Reserve dedicated lanes between bands and vertical channels beside the left strip, VPC right margin and cloud-to-external corridor. Stagger edges 6-12 px so unrelated edges do not share coordinates.
- Route a sourced identity redirect from user to IdP over the top, outside the cloud. Do not add an IdP merely because this routing rule exists.
- Multi-target integrations use one trunk per sourced phase, with junction dots where branches peel off. If the source has no phases, use one approved integration trunk without invented phase labels. Shared trunk branches are intentional topology, not accidental parallel overlap.
- Exit and enter nodes on the side facing the corridor. Never pass through icons or labels.
- The crossing budget is at most 6, perpendicular only. If routing requires more, reorder nodes within a band or move a lane.
- Label every edge on its longest segment, with a white background. Stagger labels to prevent overlap.

## Actual verification and SVG-only fallback

Use the working project's SVG path for XML parsing. For a Python renderer, `xml.etree.ElementTree.parse` from the standard library can validate well-formedness. XML success does not prove layout quality, traceability or offline rendering. Open the SVG in an available image viewer or browser with network disabled and inspect embedded assets, labels, routes and all diagram regions.

When `rsvg-convert` is available, resolve `PNG_WIDTH` to an integer at least twice the SVG logical width, then run:

```bash
rsvg-convert -w "$PNG_WIDTH" \
  -o output/solution_architecture_diagram.png \
  output/solution_architecture_diagram.svg
```

Read the resulting PNG's actual dimensions, inspect the whole image and crop all four quadrants with an available image tool. Read those crops at a useful scale. Correct clipped labels, misrouted edges, overlaps, palette errors and unexpected nodes in the renderer, then regenerate and repeat the affected checks. Record the renderer command, raster command, dimensions, inspection evidence and per-item outcomes in the review file.

If `rsvg-convert` is absent, deliver the valid SVG with `SVG-only` status and mark PNG existence, dimensions and raster inspection `Not verified`. Do not fabricate a PNG path, use a stale PNG as current evidence, or claim the full checklist passed. If SVG visual inspection is also unavailable, disclose that separately as `Not verified`; XML parsing alone is not a visual pass. Tool failures after rendering begins are reported with their actual diagnostics. Do not treat a failed render as successful fallback without explaining what remains unverified.

## Checklist (all must pass for full completion; SVG-only fallback must disclose missing PNG verification)

- [ ] SVG is well-formed; icons are embedded; it renders offline; a current PNG at least 2x width exists.
- [ ] Layer order and left/right placement follow the source-compatible layout.
- [ ] No line crosses an icon/label; no unintended parallel overlaps; crossings are at most 6 and perpendicular only.
- [ ] Every node, edge and architecture group traces to `INPUT_FILE`; phases match the source.
- [ ] No project/client names or pricing terms appear in the diagram.
- [ ] Provider palettes/badges are correct; legend and footer are present.

Record each outcome as Pass, Fail or Not verified with evidence. Fix Fail items before claiming completion. A screenshot or SVG XML parse alone does not prove source fidelity.
