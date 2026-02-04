# copy_base.py Migration Guidelines

Purpose
-------
- Provide an agent-friendly knowledge base describing rules, patterns and step-by-step instructions
  to create `copy_base.py` (OOP-style base test classes) from the legacy, fixture-based copy tests
  found in `Old/copy_old/` and using helper code in `Old/copy_tuf_old/`.

Intended audience
-----------------
- Automated agents (scripts) performing migration
- Engineers porting tests from fixture-based to class-based (OOP) tests

Inputs the agent will need
-------------------------
- Repository root (workspace): `dune/`
- Old fixtures and tests: `home/ryu535/Old/copy_old/`
- Legacy helpers/libs: `home/ryu535/Old/copy_tuf_old/` (e.g., `copy.py`)
- Central pytest infrastructure: `src/test/tests/conftest.py`
- Target folder for new base & tests: `src/test/tests/copy/`

Expected outputs
----------------
- `src/test/tests/copy/copy_base.py` implementing base classes and helpers
- Converted pilot test files (1–3) in `src/test/tests/copy/` inheriting the base
- A mapping artifact (CSV/MD) mapping old fixtures/tests → new base attributes/tests
- A short parity/validation report (pass/fail, flakiness, notes)

High-level migration strategy (recommended)
-----------------------------------------
1. Create a minimal `copy_base.py` first (core resources only).
2. Convert a small pilot set (1–3 tests) to validate approach.
3. Iterate: extract helpers into `copy_base.py` as duplicated needs appear.
4. Port remaining tests in batches (8–20 tests), grouped by subsystem.
5. Validate, open small PRs per batch, run CI, and repeat.

Design rules and patterns for `copy_base.py`
-----------------------------------------
- Scope and lifetime
  - Use `@classmethod def setup_class(cls)` to reproduce class-scoped fixture behavior.
  - Use `teardown_class` (or subclass teardowns) to restore persistent state (default tickets, configuration).

- Keep setup minimal
  - Start with the smallest set of shared resources required by pilot tests:
    `ip_address`, `cdm`, `udw`, `tcl`, `copy`, `job_queue`, `job_history`.
  - Instantiate `PrintEmulation`, `Spice`, or `EWS` only in subclasses or when required by tests.

- Responsibility separation
  - Base class: centralize copy-related resources and general helpers (job helpers, ticket validation, queue/history handling).
  - Subclasses: hold environment-specific setup (UI, EWS, full-headed). Example subclasses:
    - `TestWhenWorkingWithCopyUI` (starts `Spice` and `UI`)
    - `TestWhenWorkingWithCopyEWS` (creates `ews` client)
    - `TestGivenEmptyQueueAndEmptyHistory*` classes (clear queue/history in setup)

- Helper functions
  - Create focused helpers rather than one huge routine. Examples:
    - `validate_settings_used_in_copy(self, job_id, **expected)`
    - `save_default_ticket(self)` / `restore_default_ticket(self)`
    - `enable_duplex_supported(self)` / `disable_duplex_supported(self)`
    - `reset_trays_if_emulator(self)`

- Logging and waits
  - Add structured logging inside base methods to aid debugging.
  - Prefer polling for device-ready states instead of fixed `sleep()` times.

- No global mutable state
  - Keep test state on `cls` or `self`. Avoid module-level mutable variables.

- Autouse fixtures from legacy `conftest.py`
  - Keep `src/test/tests/conftest.py` — it provides global options and session-level fixtures.
  - During migration, keep `Old/copy_old/conftest.py` as a reference. Only move copy-only fixtures into `copy_base.py`.
  - Do not duplicate fixture names between pytest `conftest.py` and `copy_base.py` — use methods for copy-specific behavior.

Fixture → attribute mapping (common patterns)
-------------------------------------------
- `cdm` fixture → `cls.cdm = get_cdm_instance(cls.ip_address)`
- `udw` / Underware fixture → `cls.udw = get_underware_instance(cls.ip_address)`
- `tcl` fixture → `cls.tcl = TclSocketClient(cls.ip_address, 9104)`
- `copy` fixture → `cls.copy = Copy()` or `Copy(cls.cdm, cls.udw)`
- `job`, `job_queue`, `job_history` fixtures → `JobQueue()`, `JobHistory()` on `cls`
- `spice` fixture → create `Spice` in UI subclass using `get_qmltest_port()` and `get_screen_capture()`
- `print_emulation` fixture → instantiate `PrintEmulation` only if tests need it

Agent step-by-step actionable procedure
--------------------------------------
Phase A — Inventory (agent)
  1. Parse `Old/copy_old/conftest.py` and collect all fixture names, scope and usage.
  2. For each fixture mark: `session-wide` | `copy-only` | `used-by-other-suites`.
  3. Produce a CSV: Fixture, Scope, FilesUsing (list), MoveToBase? (yes/no).

Phase B — Build minimal base (agent)
  1. Create `src/test/tests/copy/copy_base.py` with:
     - imports for `get_cdm_instance`, `get_underware_instance`, `TclSocketClient`, `Copy`, `JobQueue`, `JobHistory`, `get_ip`, `get_emulation_ip`, `get_qmltest_port`, `get_screen_capture`, `PrintEmulation`, `Spice`, `get_ews_instance`.
     - `TestWhenWorkingWithCopy.setup_class` implementing core attributes.
     - Minimal `teardown_class` that can restore saved defaults if present.
  2. Add lightweight `validate_settings_used_in_copy(self, job_id, **expected)` stub.

Phase C — Pilot conversion (agent or human)
  1. Select 1–3 representative tests (simple, one UI, one headless, or as available).
  2. Convert function-style tests to class tests that `inherit` the appropriate base or subclass.
     - Replace fixture parameters with `self.<attribute>` usages.
  3. Run the original test and the refactored test and compare results.

Phase D — Extract helpers and iterate
  1. While porting more tests, extract repeated logic into separate helper methods in `copy_base.py`.
  2. Keep helper functions small and documented.

Phase E — Batch migration and CI
  1. Port tests in batches (8–20) grouped by subsystem.
  2. Create small PRs per batch including a mapping file and run CI.
  3. Address regressions quickly; keep PRs revertable.

Validation & parity checks (required)
----------------------------------
- Run old vs new tests with identical inputs; compare pass/fail and key log lines.
- Repeat each test 3 times to detect flakiness.
- Check that side-effects are identical: saved outputs, tray states, default ticket restored.
- Confirm no leaked state between tests by running batch twice in sequence.

CI / PR guidance
----------------
- Keep each PR small and focused (one batch). Include:
  - mapping CSV: old_test -> new_test
  - what was moved from `Old/copy_old/conftest.py` into `copy_base.py`
  - local verification logs and flakiness notes
- Run a targeted subset of CI tests for the batch; run full suite in a staging run before final merge.

Common pitfalls and how to handle
--------------------------------
- Big monolithic `copy_base.py`: avoid; prefer incremental helpers.
- Leaving autouse behavior unaccounted: audit autouse fixtures and implement equivalent logic in base setup/teardown.
- Starting UI or emulation unnecessarily: use subclasses to avoid launching heavy services for headless tests.
- Race / timing issues: use polling and status checks instead of blind sleeps.

Sample minimal skeleton (agent may use as template)
--------------------------------------------------
```python
from dunetuf.cdm import get_cdm_instance
from dunetuf.copy.copy import Copy
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.metadata import get_ip, get_emulation_ip, get_qmltest_port, get_screen_capture
from dunetuf.features.job.job_history.job_history import JobHistory
from dunetuf.features.job.job_queue.job_queue import JobQueue
from dunetuf.emulation.print import PrintEmulation
from dunetuf.ui.spice import Spice
import logging

class TestWhenWorkingWithCopy:
    @classmethod
    def setup_class(cls):
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        cls.tcl = TclSocketClient(cls.ip_address, 9104)
        cls.copy = Copy()
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()

        engine_ip = get_emulation_ip()
        if engine_ip and engine_ip != 'None':
            cls.print_emulation = PrintEmulation(cls.cdm, cls.udw, cls.tcl, engine_ip)
        else:
            cls.print_emulation = None

    @classmethod
    def teardown_class(cls):
        # restore defaults if saved
        if getattr(cls, 'saved_default_ticket', None):
            cls.copy.set_copy_configuration(cls.saved_default_conf)

    def validate_settings_used_in_copy(self, job_id, **expected):
        # fetch ticket and assert requested fields
        pass

class TestWhenWorkingWithCopyUI(TestWhenWorkingWithCopy):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        port = get_qmltest_port()
        screen_capture = get_screen_capture()
        cls.spice = Spice(cls.ip_address, port, screen_capture)
```

Recommended tools & automation
------------------------------
- Small generator script (optional): read function tests and emit skeleton class files replacing fixture args with `self` attributes.
- Use CSV/MD mapping files for traceability.

Final notes
-----------
- Keep the central `src/test/tests/conftest.py` — it contains CLI and session-level fixtures required by the entire test suite.
- Keep `Old/copy_old/conftest.py` until migration completes; use it as authoritative reference and audit source.
- Migrate incrementally and keep PRs small for safe rollbacks.

---
Generated by migration guidance agent.
