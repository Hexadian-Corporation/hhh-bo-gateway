<critical>
For full project context, read:
- Local: `.github/instructions/*.instructions.md`
- Standalone: https://github.com/Hexadian-Corporation/hhh-bo-gateway/blob/main/.github/instructions/*.instructions.md
</critical>

<critical>
**After every implementation:** once code is committed and pushed to the feature branch, always open a pull request targeting `main` using the GitHub MCP tools (`mcp__github__create_pull_request`). The PR title MUST be identical to the originating issue title. The PR body MUST include `Fixes #N` to link and auto-close the issue on merge. Never consider an issue "done" until the PR exists.
</critical>

<critical>
**GitHub MCP requires GITHUB_PERSONAL_ACCESS_TOKEN:** The GitHub plugin (`github@claude-plugins-official`) in `.claude/settings.json` needs this environment variable set to authenticate. Without it, `mcp__github__create_pull_request` and all other GitHub MCP tools fail. Ensure this is set in the session environment or via Claude Code's GitHub OAuth integration before starting work that requires PR creation.
</critical>

<critical>
**PR Workflow — mandatory for every change**
Every change — with or without a linked issue — MUST go through a feature branch and Pull Request targeting `main`. Direct commits to `main` are forbidden.

**Mandatory review before closing the task** — after push + PR is open, run ALL of the following commands in order:

*Quality & correctness:*
- `/review`
- `/pr-review-toolkit:review-pr`
- `/code-review:code-review`
- `/code-reviewer`
- `/requesting-code-review`

*Security & depth:*
- `/security-review`
- `/pr-review-toolkit:type-design-analyzer`
- `/pr-review-toolkit:comment-analyzer`

These invoke specialized subagents and skills: `pr-review-toolkit:code-reviewer`, `pr-review-toolkit:code-simplifier`, `pr-review-toolkit:pr-test-analyzer`, `pr-review-toolkit:silent-failure-hunter`, `code-review:code-reviewer`, `superpowers:requesting-code-review`, `security-auditor`, `senior-security`, `pr-review-toolkit:type-design-analyzer`, and `pr-review-toolkit:comment-analyzer`.

**All findings must be fixed** — regardless of severity or whether they were pre-existing — with new commits pushed to the PR after the review. The task is not done until all reviews pass clean.
</critical>

<critical>
**Development Cycle — follow this sequence for every non-trivial task**
1. **Plan first:** `/writing-plans` (`superpowers:writing-plans`) before touching any code
2. **TDD:** `/test-driven-development` (`superpowers:test-driven-development`) — write tests before implementation
3. **Implement with specialized subagents + expert skills:**
   - Parallel independent tasks → `/dispatching-parallel-agents` (`superpowers:dispatching-parallel-agents`)
   - Sequential plan execution → `/subagent-driven-development` (`superpowers:subagent-driven-development`)
   - Agent: `feature-dev:code-architect`, `feature-dev:code-explorer`, `python-pro`, `senior-backend`, `senior-frontend`, `senior-fullstack`…
   - Skill: `clean-code`, `react-best-practices`, `python-patterns`, `senior-backend`, `senior-frontend`…
4. **Verify before pushing:** `/verification-before-completion` (`superpowers:verification-before-completion`)
5. **Push + open PR → run full review suite** (see PR Workflow block above)
</critical>

<critical>
**Quality Gate — mandatory before any push or PR**
All unit and integration tests MUST pass (zero failures) and test coverage MUST be ≥ 90% — target as close to 100% as possible. Do not push, open a PR, or consider the task done until this gate is met.
Test command: `uv run pytest --cov --cov-fail-under=90`
</critical>

## Issue Triage — Priority & Complexity

Every new issue across Hexadian repos must be added to the GitHub Project ["Hexadian Apps — Active Work"](https://github.com/orgs/Hexadian-Corporation/projects/1) and classified with **Priority** and **Complexity** custom fields before moving from *Backlog* to *Ready*.

### Priority (4 levels, PINK · ORANGE · PURPLE · BLUE)

| Level | Color | Use for |
|---|---|---|
| **Critical** | PINK | Blocks 5+ other project items, or severe prod regression / security incident. |
| **High** | ORANGE | Bug fixes (`fix:` / `hotfix:` / `security:`), or work blocking 3–4 items. |
| **Medium** | PURPLE | New features, perf, refactors (`feat:` / `perf:` / `refactor:`), or 1–2 dependents. |
| **Low** | BLUE | Tests, chores, docs, CI (`test:` / `chore:` / `docs:` / `ci:` / `style:` / `build:`). |

**Assignment heuristic:**

1. **Baseline by conventional-commit type** in the issue title:
   - `fix` / `hotfix` / `security` → **High**
   - `feat` / `perf` / `refactor` → **Medium**
   - `test` / `chore` / `docs` / `ci` / `style` / `build` → **Low**
   - other → **Medium**
2. **Block-count bump** — count project items this issue blocks (body text `Blocks #N` / `Requires #N`, sub-issue tracking, parent task lists):
   - blocks ≥ 5 → **Critical** (override baseline)
   - blocks 3–4 → +2 levels (cap Critical)
   - blocks 1–2 → +1 level
   - blocks 0 → baseline

### Complexity (4 levels, GRAY · GREEN · YELLOW · RED)

| Level | Color | Use for |
|---|---|---|
| **Trivial** | GRAY | One-line change, config tweak, typo. ≤ 30 min. |
| **Low** | GREEN | Small, localized change in a familiar area. ≤ 2 h. |
| **Medium** | YELLOW | Multi-file change within one service/layer, standard patterns. ½–2 days. |
| **High** | RED | Cross-cutting, new subsystem, architectural change, or research. > 2 days. |

**Rules of thumb:**
- Complexity is **effort**, not importance. A Trivial fix can be Critical priority.
- If scope grows past the initial Complexity estimate, split the issue instead of upgrading.
- Four levels (not three) force a deliberate choice rather than defaulting to a safe middle.
