# Evidence guide

- `local-trace.json`: final Qwen 2.5 3B run, including input fixture, measured latency and comparison with authored expectations. It got 5/6 labels correct, missing Python evidence, and took 35.016 seconds. This is limited synthetic evidence, not a broad accuracy claim.
- `demo-trace.json`: deterministic non-AI keyword baseline on the same fixture.
- `test-results.txt`: 12 passing regression tests.
- `browser-check.txt`: demo browser-check details; original desktop/mobile screenshots are `interface-desktop.png` and `interface-mobile.png`.
- `browser-local-check.txt`: final live-model browser verification; screenshots use the `interface-local-` prefix.
- `iteration-02-uncertain.json`: small-model run with unverifiable evidence downgraded.
- `iteration-03-omitted-gaps.json`: small-model run that omitted preferred requirements.
- `iteration-04-guarded-gaps.json`: six requirements, with two unsupported matches downgraded.
- `iteration-05-small-model.json`: small-model run that incorrectly labeled all requirements missing.

The initial 1.5B development run completed in 29.630 seconds with four matches and two gaps, but its free-form advice overstated proficiency. Its full JSON was not preserved. This finding led to replacing free-form suggestions with verified-evidence templates. Subsequent unsuccessful runs are preserved above. The final 3B model improves classification relative to those runs but still misses one clear match.

The app and documentation were tested with Python 3.12.14 and pypdf 6.21.4. No human recommendation ratings have been collected.
