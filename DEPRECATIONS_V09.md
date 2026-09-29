# v0.9 deprecations

- The v0.7 interpretation that counted Stretto `HAND_BACK / RESPOND` as a deterministic
  continuation is invalid and superseded by v0.8+.
- The shorthand `beta_TASK = 3` for the telecom three-fault example is too broad.
  The correct claim is candidate-relative:

  `beta_{TAU2_TASK_SUCCESS,C0}(q;H) = 3`

  where `C0 = {REFUEL, RESEAT_SIM, RESET_APN_REBOOT}` and `H` is the three explicit
  fault contexts.

The older JSON files are retained only for provenance/regression history; use the v0.9
candidate-relative result in any paper or README claim.
