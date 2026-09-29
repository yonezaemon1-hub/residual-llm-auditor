# v0.8 claim boundaries

## Supersedes one v0.7 interpretation

`HAND_BACK / RESPOND` is not a deterministic continuation in Stretto's read-only flow.
It is a fallback from compiled execution to the agent/model.

The corrected 5-session site is therefore:

- 8/9 trace-exact contexts deterministically coverable;
- exact minimum deterministic cover on those 8 contexts: 2 branches;
- 1/9 context requires fallback relative to the two compiled lookup branches.

## Genuine compiler-emitted deterministic multiway site

Stretto's public reach retail flow records four deterministic lookup transitions after
`get_order_details`:

- `get_order_details` — 1332
- `get_product_details` — 223
- `get_user_details` — 3
- `list_all_product_types` — 7

Restricting the certification set to these lookup-labeled transitions and using exact
lookup-label reproduction gives `beta_TRACE = 4`. No model fallback is counted as a branch.

## Task-success three-way certificate

At the compiled telecom `check_apn_settings` site, Stretto's public no-model procedure
contains successful-training branches whose fixes include:

- data refuel;
- SIM reseat;
- APN reset.

The official τ² telecom task generators and tool implementation provide three canonical
fault contexts whose task-success requirements separate the corresponding full fix suffixes:

1. data-usage exceeded -> `refuel_data(+2 GB)`; exact +2 GB assertion;
2. SIM unseated -> `reseat_sim_card`; otherwise network search remains NO_SERVICE;
3. APN broken -> `reset_apn_settings; reboot_device`; otherwise APN remains BROKEN and
   network search remains NO_SERVICE.

On this finite 3-context / 3-program certification set the task-success matrix is identity,
so `beta_TASK = 3`.

This is a finite relative lower bound over these branch programs. It is not a claim that no
other program in the full telecom action language could solve more than one context.
