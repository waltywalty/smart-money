# programmes/insider - SCOPED, NOT OPEN

**This programme is not open. No build follows from anything in this directory.**

`ROADMAP.md` family 2 carries a gate: *relocation complete, and family 1 has produced a
verdict.* **Neither has happened.** Family 1 has not detected a single event.

Packet 7 answered four questions from literature and public documentation in order to find
out whether the family is worth building **before** a week is spent on infrastructure. It
built nothing: no collector, no parser, no EDGAR pipeline, and **no filing data was fetched
at any point**. Reading SEC documentation to learn what a field means was in scope; pulling
a Form 4 to see what is in the field was not.

| document | what it is |
|---|---|
| `KILL-CONDITION.md` | **Sealed before the literature was read.** sha256 `925b9bff478cea4211d7c4cdccf626e70f2ca58c99745a6730a90cef3dcfcde1`, commit `eac6eda`. Not to be edited - dated amendments only. |
| `PRIORS.md` | What the literature claims, with sample periods, and what is missing. No synthesis. |
| `CLASSIFIER-SPEC.md` | Rules as specifications, from papers and SEC documentation. Not code. |
| `HURDLE.md` | The cost of trading this at Walton's size, from public documentation. |
| `SCOPING-VERDICT.md` | The verdict against the sealed kill condition. |

**A "survives scoping" verdict would not open the programme.** It would mean the gate is the
only thing between here and a build, and lifting the gate is Walton's call after the move.

Every figure in these documents was read from a source fetched as raw bytes. Where a source
could not be reached, the item is recorded as **could not establish** - never as *no
evidence found*. A summary of a paper is not the paper.
