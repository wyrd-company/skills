**REVIEW ROUND {N}: {ACCEPTED | REJECTED | CHANGE APPROVED, REBASE EXPECTED | SURFACE REJECTED}**

{The result and what the executor does next, in two or three sentences.}

- Level: {low | normal | high}, {the signals that set it, and why it was raised, if it was}
- Reviewer: {full thread id}  <!-- task log only: leave it out on a GitHub surface -->
- Surface: {pull request or review id}
- Reviewed head: {sha}
- Base head: {sha, which any approval was made against}
- Findings: {P0 n, P1 n, P2 n, P3 n, Q n}, {the top concern}
- Previous round
  - {Finding}: {fixed | still open | rejection accepted | deferral accepted | answered}, {what you checked}
- Deferred findings: {for each, in an epic: into the epic or an issue, and why}
- Soft claims
  - {Claim}: {met or not, and what you judged it on}
- Lenses: {lens: what it found, or not run}  <!-- high only -->
- Council: {member: verdict, score}  <!-- council only -->
- Task audit: {flags, or no flags}  <!-- normal and high -->
- Safety fact: {the fact, and how far you proved it}  <!-- normal and high -->
- Merge gates  <!-- only when you have merge authority -->
  - Accepted: {yes | no}
  - Base unmoved since the surface check: {yes | no}
  - Surface head is the reviewed head and the task branch head: {yes | no}
  - Nothing merges ahead: {yes | waiting on task}
  - Nothing newly public holds a secret or identifying value: {yes | not applicable | no}
- Merged: {sha into branch | no, and why}
- Published: {epic pull request comment | unpublished, and why | not an epic}
