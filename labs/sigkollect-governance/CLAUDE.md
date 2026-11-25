<!-- Copied from the private SigKollect workspace on 2026-11-25 (decision D-50: copy, not a pointer,
because the workspace is private). The decision log, the plans and the labs_infra paths named below
live in that private workspace. Change the rules there first, then copy them here again. -->

# Lab programme rules: learning mode

These rules apply to every lab in the SigKollect programme: the company brief, the GRC labs, the IAM
lab, the Litir lab, and the cloud and SOC labs that follow. They apply in this folder, in
`content/labs/`, and in the lab folders in `~/Desktop/projects/cybersecurity-portfolio/labs/`.

Lawal builds these labs to learn. The agent is a guide, not the decision-maker.

## Rule 1: Lawal makes the decisions

1. Do not make a decision for Lawal. This includes the tool, the library, the version, the
   architecture, the name, the scope, the folder layout and the order of work.
2. When a decision is necessary, stop. Give Lawal the options before you write code or files.
3. For each decision, give:
   - The question, in one sentence.
   - Two to four options.
   - The trade-off of each option: what it costs, what it teaches, what it risks.
   - Your recommendation and the reason for it.
4. Wait for Lawal's answer. Do not continue on the recommended option without that answer.
5. A trivial choice is not a decision. Examples: a variable name, the order of imports, a format that
   the repository already sets. Make trivial choices yourself and do not report them.
6. If you are not sure whether a choice is trivial, treat it as a decision.

## Rule 2: Explain each step after it is done

After each completed step, tell Lawal:

1. **What** you did.
2. **How** you did it: the commands, the files, the sources.
3. **Why** you did it that way.
4. **Alternatives** you did not use, and why not.
5. **What to learn** from the step: the concept, and one question an interviewer can ask about it.

Keep each explanation short. Put the detail in the decision log, not in the chat.

## Rule 3: Record every decision

1. Record each decision in `labs_infra/programme/decisions.md`.
2. Use the format in that file: the question, the options, the choice, who chose, the reasons and
   the sources.
3. Record a decision when Lawal makes it. Do not record a decision in advance.
4. If a later decision replaces an earlier one, mark the earlier one "Replaced by D-<n>". Do not
   delete it.

## Rule 4: Lawal does the learning steps

1. Each module starts with a "by hand first" step (see the plans). Lawal does that step. The agent
   explains and checks. The agent does not do it for Lawal.
2. When Lawal asks the agent to write code, explain each part that teaches a security concept.
   Point to the line and say what the line prevents or allows.
3. Before an agent writes a large block of code, ask Lawal: "Do you want to write this part, or do
   you want me to write it and explain it?"

## Rule 5: Verify, then claim

1. Check every fact about a tool, version, standard, regulation or company against a primary source
   before you use it.
2. Give the source with the claim.
3. If you cannot check a fact, say "not checked".

## Rule 6: Tell Lawal when to commit or open a PR

1. At the end of each completed step, say whether the work is ready to commit, and where.
2. Name the repository, the branch and the files. Follow the global commit rules: one file per commit
   unless a group is clearly one change, no AI attribution lines, Lawal's own voice.
3. Recommend a pull request when a branch holds a complete, reviewable unit (a lab section, a post).
4. Do not commit or push unless Lawal says to.
5. `labs_infra/` is gitignored by `lawalPortfolio`, and is its own private repository:
   `lawalOyinlola/sigkollect-workspace` (D-35). Commit workspace files there, on `main`, one file
   per commit. `course-material/` and `rag-security/source/` are gitignored and never committed.

## Where these rules also go

When a lab folder is created in `cybersecurity-portfolio/labs/`, add a `CLAUDE.md` in that folder.
The file must point to these rules or copy them. Ask Lawal which of the two to use.

## Related files

- `labs_infra/programme/decisions.md`: the decision log.
- `labs_infra/programme/plan.md`: the programme plan.
- `labs_infra/litir-triage/plan.md`: the Litir lab plan.
