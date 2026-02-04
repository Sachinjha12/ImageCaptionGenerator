COPY_BASE_MIGRATION_EXTRA
=========================

Purpose
-------
This supplemental document provides section-wise, explicit instructions and small templates that an automation agent or engineer can follow when creating `copy_base.py` and migrating fixture-based tests to OOP-based tests. Use this together with `COPY_BASE_MIGRATION_GUIDELINES.md` and the `Base Class Reference Guide.pdf` attached in the workspace.

Section A — Inventory output schema (exact)
-----------------------------------------
Create `migration/inventory.json` with this JSON schema for each fixture and test:

{
  "fixtures": [
    {
      "name": "cdm",
      "scope": "session",
      "used_by": ["copy/test_file.py::test_...", "..."],
      "autouse": false,
      "move_to_base": false,
      "notes": "session CDM client; keep in central conftest"
    }
  ],
  "tests": [
    {
      "path": "home/ryu535/Old/copy_old/test_ui_copy_app.py",
      "candidates_for_pilot": true,
      "fixtures": ["cdm", "udw", "spice"]
    }
  ]
}

Section B — File templates (concrete, copy-ready)
------------------------------------------------
Below are exact templates the agent should write to disk. Replace `{Asset}`, `{AssetClass}` placeholders.

Minimal `copy_base.py` (write to `src/test/tests/copy/copy_base.py`):

```python
from dunetuf.metadata import get_ip, get_qmltest_port, get_screen_capture, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.copy.copy import Copy
from dunetuf.features.job.job_queue.job_queue import JobQueue
from dunetuf.features.job.job_history.job_history import JobHistory
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
            logging.info('Starting PrintEmulation at %s', engine_ip)
            cls.print_emulation = PrintEmulation(cls.cdm, cls.udw, cls.tcl, engine_ip)
        else:
            cls.print_emulation = None

    @classmethod
    def teardown_class(cls):
        # restore defaults if saved
        if getattr(cls, 'saved_default_ticket', None):
            cls.copy.set_copy_configuration(cls.saved_default_conf)

    def validate_settings_used_in_copy(self, job_id, **expected):
        # stub: implement progressively as you port tests
        pass

class TestWhenWorkingWithCopyUI(TestWhenWorkingWithCopy):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        port = get_qmltest_port()
        screen_capture = get_screen_capture()
        cls.spice = Spice(cls.ip_address, port, screen_capture)
```

Section C — Single-test conversion script (pseudocode)
----------------------------------------------------
Agent pseudocode to convert a function test to class skeleton:

1. Parse the test function file and identify pytest fixture argument names.
2. Choose the appropriate base class (UI/EWS/Headless) by seeing whether `spice` or `ews` fixture is used.
3. Emit a new file under `src/test/tests/copy/` with a `Test...` class inheriting the chosen base.
4. Inside the method, create local aliases: `cdm = self.cdm`, `udw = self.udw`, etc.

Section D — Mapping CSV exact header
-----------------------------------
Header line (CSV):

old_path,old_test_name,new_path,new_test_name,fixtures_mapped,move_notes

Section E — Automated validation policy (strict)
-----------------------------------------------
- For each migrated test:
  - Run original test and migrated test with identical environment args.
  - Require both to pass. If migrated test fails but old test passes, mark defect and stop batch.
  - If both fail with the same error, flag as environment-dependent and note in mapping.
- Retry policy: up to 3 runs; if inconsistent results, flag as flaky and isolate.

Section F — Failure triage flow
------------------------------
1. If migration test fails, collect logs: `migration/logs/<batch>/<test>_new.log` and `<test>_old.log`.
2. Compare failing stack traces and last 200 lines of logs.
3. If difference appears in setup steps (e.g., missing saved default ticket), modify `copy_base.py` to include that setup.
4. If difference appears in timing, add wait_for/polling helper and retry.

Section G — Example `wait_for` helper (exact code)
-------------------------------------------------
```python
import time

def wait_for(predicate, timeout=30, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if predicate():
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False
```

Section H — Reuse for other assets
----------------------------------
- Replace the `Copy` imports and ticket-validation logic with the asset equivalent (Print/Scan/Fax).
- Maintain the same file and class naming conventions: `print_base.py` → `TestWhenWorkingWithPrint`.

Section I — Recordkeeping
-------------------------
- Agent must write these artifacts into `migration/` folder for auditability:
  - `inventory.json`
  - `mapping_batch_<n>.csv`
  - `logs/` per test and batch
  - `patches/` (diffs that show generated files)

Section J — When to stop using legacy `Old/copy_old/conftest.py`
----------------------------------------------------------------
- Only when all tests that referenced those fixtures are migrated and mapping CSV shows no remaining references.
- Run a grep for references to old fixture names before deleting; keep backup branch.

---
End of supplemental migration instructions.
