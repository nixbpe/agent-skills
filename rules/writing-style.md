# Writing Style

Applies to prose you write: docs, agent and skill files, handoffs, reviews,
commit messages, code comments, and replies. Does not apply to code, quoted
material, or user-written text you were not asked to edit.

State the fact, number or decision first, so the reader can act on it.

## Preserve verbatim
Never reword, translate or reformat:
- Headings that other files link to or cite
- Identifiers defined by the project (rule IDs, ticket IDs, trace IDs)
- Numbers, units, dates, versions
- Inline code, code blocks, file paths, commands, config keys
- Field labels and status words defined by the project
- Technical terms in their original language (API, endpoint, rollback), even in Thai prose

## Avoid → Write instead
- "Not X, but Y" contrasts → state the actual fact or impact
- Filler openers (นอกจากนี้, อย่างไรก็ตาม, Additionally, Moreover) → start with the subject
- Inflated words (ยกระดับ, ครอบคลุมอย่างครบถ้วน, robust, comprehensive, seamless, leverage)
  → name what is covered, with the number or ID
- Stacked qualifiers (อาจจะมีแนวโน้มที่อาจ) → one qualifier, only where uncertainty is real
- Vague subjects or passive voice that hides the actor → name who or what does it
- Em or en dashes as punctuation → comma, colon or parentheses
  (hyphens in compound terms and numeric ranges are fine)
- Decorative bold or emoji → bold only field labels and totals
- Closing sentence that restates the paragraph → end on the last concrete fact
- Chat residue (หวังว่าจะเป็นประโยชน์, Let me know, Great question) → remove
- Restating the request or narrating steps already visible in tool output → remove

## Structure
- Lead with the conclusion, then evidence.
- Lists for parallel items (3+), tables for comparisons across 2+ attributes,
  prose for reasoning. Keep list items parallel and non-overlapping.
- Match length to the task; a one-line answer stays one line.

## Accuracy
- Separate what was verified (ran, read, observed) from what is assumed.
  Say which is which.
- When tightening, do not add or remove facts, sources, owners or dates,
  and do not change modality (must / should / may).
- If a sentence needs a missing detail, ask or mark it as open.

## Language
- Reply in the language the user writes in. Docs follow the existing language of the file.
- Thai prose: keep sentences short, avoid formal padding (ในส่วนของ, ได้มีการ, ทำการ).

## Commit messages and comments
- Commit subject: imperative, ≤ 72 chars, no trailing period. Body explains why, not what.
- Code comments explain intent or constraints the code cannot show. No comments that restate the code.
