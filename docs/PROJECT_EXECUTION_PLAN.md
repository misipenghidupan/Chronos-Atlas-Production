# Chronos Atlas: Comprehensive Execution Plan & Project Rules

This document is the central, living checklist and rulebook for building Chronos Atlas to MVP and beyond. Update as you progress.

---

## 1. Guiding Principles

- **Single Source of Truth:** Each config (e.g., DB settings, indexes) defined in only one place.
- **Environment Parity:** Dev mirrors prod (Docker, PostgreSQL, unified settings).
- **Clarity & Maintainability:** Code, docs, and structure must be clean, consistent, and easy for any developer.
- **Modern Docker Usage:** Always use `docker compose` (never `docker-compose`).
- **Docker-First Workflow:** All development, debugging, tests, pre-commit hooks, and management commands must be run inside Docker containers. Never run or debug code, tests, or automation outside Docker unless explicitly documented as an exception.
- **README Policy:** Keep all READMEs in sync and up to date, with clear audience and purpose.

---


## 2. Unified Roadmap & Workflow Execution Plan

### ✅ Foundation & Refactor (Complete)
- [x] Fix management command and restore GiST indexes.
- [x] Unify environment config (PostgreSQL, dj_database_url, settings).
- [x] Remove hardcoded settings, consolidate documentation.

- [x] Add `.pre-commit-config.yaml` for auto-formatting (Black, isort) and lint checks.
- [x] Install and enforce pre-commit hooks (`pip install pre-commit` + `pre-commit install`).
		- After pulling the latest changes, contributors should run:
			```bash
			pip install pre-commit
			pre-commit install
			```
		- This will ensure all code is auto-formatted and linted before every commit.
- [x] Add GitHub Actions workflow (`.github/workflows/ci.yml`) to run tests on every push/PR.
- [x] Add a `Makefile` or shell scripts for common Docker Compose commands (build, up, down, test, logs).
- [x] Use `mkdocs` to auto-generate and serve docs from markdown files.
	- To install: `pip install mkdocs`
	- To serve locally: `mkdocs serve`
	- To build static site: `mkdocs build`
- [x] Set up branch protection rules on GitHub for `dev-stage` and `main`.
	- Go to your repository on GitHub > Settings > Branches.
	- Add rules for both `main` and `dev-stage`:
		- Require pull request reviews before merging
		- Require status checks to pass before merging (e.g., CI)
		- Require branches to be up to date before merging
		- (Optional) Restrict who can push to matching branches
- [x] Add `.github/pull_request_template.md` for standardized PRs.
- [x] Create a script to automate copying and committing shared files between repos if needed.
	- Usage: `./scripts/sync_shared_files.sh` (from project root)
- [x] Add a setup script to automate pyenv/virtualenv creation and requirements installation for new contributors.
	- Usage: `./scripts/setup_python_env.sh` (from project root)

### ⬜️ Pre-MVP: Core Functionality & Quality
 - [x] Add GitHub Actions workflow (`.github/workflows/ci.yml`) to run tests on every push/PR.
- [x] Update all READMEs and detailed docs for MVP state.
- [x] Add API usage examples and troubleshooting tips.
- [x] Test production Docker Compose setup (`docker-compose.prod.yml`).
- [x] Document deployment, environment variables, and secrets handling.
- [x] Load larger sample data and verify GiST index usage in query plans.

### ⬜️ Post-MVP: Polish & Scale
- [ ] Implement and document ETL pipeline (Wikidata, etc.).
- [ ] Integrate Redis and Celery for caching and ETL jobs.
- [ ] Add logging, error tracking, and basic monitoring.
- [ ] Audit for secrets, permissions, and best practices.
- [ ] Prepare for cloud deployment (Docker registry, cloud DB, etc.).

### ⬜️ Onboarding & Contributor Experience (Continuous)
- [ ] Add onboarding steps for new contributors (clone, setup, run, test, contribute).
- [ ] Document all automation and workflow scripts.

---


---

## 4. Final MVP Review & PR Template

### Final Summary

Chronos Atlas MVP is complete:
- All core APIs, models, and automation are implemented and tested.
- Documentation is up to date for onboarding, deployment, and troubleshooting.
- Sample data and GiST indexes are loaded and verified.
- CI, pre-commit, and PR automation are enforced.
- All MVP checklist items are complete in `PROJECT_EXECUTION_PLAN.md`.

### PR Preparation Checklist

- [x] All code passes tests and linting (pre-commit, CI).
- [x] All documentation is up to date and clear.
- [x] All environment and deployment instructions are accurate.
- [x] No secrets or sensitive data are committed.
- [x] All MVP checklist items are complete in `PROJECT_EXECUTION_PLAN.md`.
- [x] Branch is up to date with `dev-stage` and ready for PR.

### PR Body Template

```
## Chronos Atlas MVP Delivery

### What’s included
- All core APIs (GraphQL, REST), models, and management commands
- Docker Compose (dev/prod), environment parity, and automation
- Pre-commit, CI, and PR workflow
- Complete documentation (README, detailed docs, onboarding, troubleshooting)
- Sample data and GiST index verification

### How to test
1. Clone repo and run `pip install pre-commit && pre-commit install`
2. Start dev: `docker compose -f docker-compose.dev.yml up --build -d`
3. Run tests: `make test`
4. Try API endpoints: `/graphql/`, `/api/figures/`, `/api/timeline/`
5. Review docs in `README.md` and `docs/README_DETAILED.md`

### Checklist
- [ ] All tests pass
- [ ] All docs up to date
- [ ] No secrets committed
- [ ] Ready for review/merge
```

---

## 3. Session Log

*Update this section as you complete major tasks or milestones.*
