# Packet 9 progress log - **COMPLETE**

So a restarted session resumes from files rather than from memory.

| task | artefact | commit | sha256 (first 16) | status |
|---|---|---|---|---|
| T1 | `KILL-CONDITION.md` **SEALED - do not edit** | `8f3c0a9` | `c62c13ab11236f1b` | **done** |
| T2 | `PRIORS.md` | `91ecdae` | `55ef539f83aab686` | **done** |
| T3 | `MECHANICS.md` | `a9f1584` | `1a2923fdaf3225c4` | **done** |
| T4 | `BREAKS.md` | `44f83b8` | `bc950e6dde50f097` | **done** |
| T5 | `SCOPING-VERDICT.md` | `353a67d` | `92cf04fbca9d0fe0` | **done** |
| T5 | `registry/F3-FLOW-SCOPING.md` | `8cc8a6a` | `8cbf6645bf1d2174` | **done** |
| close | `CLOSEOUT-PACKET9.md` | see log | `45ed63f952a02a5b` | **done** |
| close | `README.md` | see log | `c15f26a93eeda528` | **done** |

**Verdict: family 3 does not survive scoping.** Both strands could not establish; neither killed on
arithmetic, because in neither case was the arithmetic evaluable.

**T1 is sealed.** Re-verify with
`python3 lib/verify_blob.py programmes/flow/KILL-CONDITION.md=flow/KILL-CONDITION.md` against sha256
`c62c13ab11236f1bef8733f24c9709b6ec8ff893463fb126eb0ad4163f05056a`. **Two defects were found in it
and recorded rather than patched** - see `CLOSEOUT-PACKET9.md` section 8.
