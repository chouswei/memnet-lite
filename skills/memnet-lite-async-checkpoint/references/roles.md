# Roles

Roles are duties. Model families live only in User Rules **Model by role**. Resolve the newest listed slug for that family and tier; if the preferred tier is missing, use the newest family slug on the session allowlist and name the gap.

MUST NOT pin a nickname or a product patch version as a role. MUST NOT use FAST / `*-fast` variants. MUST NOT use Cursor `subagent_type` values (`explore`, `bugbot`) as house roles. This skill does not copy a version table — resolve from User Rules.

| Role | Does | MUST NOT | Who runs it |
|------|------|----------|-------------|
| Architect | Thin root plan: purpose, constraints, approach, path/locator pointers. Complex root plan or complex diagnosis only. | Emit atoms, waves, patches, file bodies, skill stacks. | Worker. Parent sends pointers only. |
| Bind | Catch Architect (or write a normal plan). Fill detail. Emit atom cards with `wave`, `order`, `role`, disjoint scopes, proof. | Implement, deploy, or spawn Task itself. | Parent when it can emit cards; else one Bind worker that returns cards and stops. |
| Diagnose | Name cause and a checkable proof. | Implement or emit execute atoms. | Worker unless the parent can diagnose a small case. Then Bind. |
| Implement | Change one bound atom. Run that atom's proof command. | Plan, diagnose, deploy, edit outside `scope.paths` / `scope.locators`. | One worker per atom. |
| Deploy | Ship a committed change to the live host, verify, state rollback. | Author the change. Treat local tests as deploy proof. | Own wave/atom after Implement proof. |
| Web | Live web or library docs for one question. | Edit the repo. | Worker when Bind tagged Web. |
| Visual | Visual review of named artefacts. | Implement. | Worker when needed. |
| Prose | Author named prose. | Redesign architecture. | Worker when needed. |
| Unclear | Bound question or route when two scans fail. | Invent a specialist. | Parent or a planning-capable worker. |

Architect input: problem, constraints, path/locator pointers. Architect output: purpose, constraints, approach, path/locator pointers. Locators are MemNet Lite cues, not SysMLEdge qnames.

Review roles (Visual, Web, Prose, Unclear) only when Bind tags them or the operator asks.

## Parent vs worker

- Parent coordinates even when Bind is on parent.
- MUST NOT bundle Bind + Implement in one worker or one Task prompt.
- MUST NOT give Implement a root plan, a diagnosis, a bundled sequential job, live deploy, visual review, or web search.
- Fallback when a role's family is off the allowlist: name the gap, pick the next live listed slug, continue. MUST NOT stall.
- Soft: a planning-capable parent may Bind on parent. Do not require a named vendor parent.
