# AI use policy

## 1. Purpose

SigKollect uses AI to work faster and to build better products. Its risk appetite for technology
change, including AI, is **Open** (risk appetite row 6). That appetite never overrides the
**Averse** appetite for customer data (row 1) or for legal compliance (row 2).

This policy says which AI tools staff may use, what data may go into them, who approves a new AI
tool or feature, and how AI output is checked.

## 2. Scope

This policy covers:

- every employee, contractor and third-party worker who uses an AI tool for SigKollect work;
- every AI tool, whether it is a separate product (a chat assistant), a feature inside a tool
  SigKollect already uses, or a coding assistant;
- every AI feature that SigKollect builds into its own products or internal systems, including AI
  agents that can call tools or take actions.

## 3. Definitions

| Term | Meaning |
|---|---|
| AI tool | Software that produces text, code, images or decisions from a model trained on data, such as a large language model |
| Approved AI tool | An AI tool on the AI register (section 9), used through a SigKollect account |
| AI agent | An AI system that can take actions, such as reading files, calling an API or sending a message, and not only answer |
| Prompt | Everything sent to an AI tool: typed text, pasted text, uploaded files and connected data |

### Data classes

SigKollect has no data classification yet. Until the information security policy (objective c)
sets one, this policy uses these four classes:

| Class | Examples |
|---|---|
| **Restricted** | Card data, BVN, NIN, bank account details, passwords, API keys and other secrets, security logs, incident details |
| **Confidential** | Merchant and customer records other than the above, staff records, contracts, source code, internal financial data, risk register |
| **Internal** | Internal documents, process notes, meeting notes with no customer or staff data |
| **Public** | Published website content, public API documentation, marketing material |

## 4. Principles

1. **A person is responsible for every AI output.** The person who uses the output owns it, as if
   they wrote it themselves.
2. **Data goes only where it is allowed to go.** A prompt is a disclosure to the tool's supplier.
3. **AI does not decide alone about a person.** A decision that affects a customer, a merchant or a
   member of staff has a human review before it takes effect.
4. **An AI agent gets the least access it needs.** It gets only the tools, data and permissions
   its task needs, and a person approves any action that leaves SigKollect.
5. **Text from outside is data, not instructions.** Content from emails, websites, files and
   customers can carry hidden instructions (prompt injection). An AI system must not follow them.

## 5. Approved AI tools

SigKollect starts with AI features from suppliers it already uses and has assessed: Google
Workspace, GitHub and Microsoft Azure. Each feature is still assessed under section 8 before it goes
on the AI register, because an AI feature can have different data terms from the product it sits
in. Staff can request other tools through section 8.

Rules:

1. Use an AI tool for SigKollect work only through a **SigKollect account**, with single sign-on
   and MFA where the tool supports them. Personal and free accounts must not receive any data
   above Public.
2. A tool that is not on the AI register (section 9) is not approved.
3. Do not install browser extensions or desktop apps with AI features unless they are on the
   register.

## 6. Data in prompts

Each data class may go only into these AI tools:

| Data class | Allowed in |
|---|---|
| Restricted | Only a SigKollect-controlled deployment approved for Restricted data, such as a model in SigKollect's own Azure tenant. Never in any other AI tool |
| Confidential | Approved AI tools whose register entry allows Confidential data |
| Internal | Approved AI tools |
| Public | Any AI tool |

Rules:

1. **Passwords, API keys and other secrets never go into any AI tool.** If a secret is pasted by
   mistake, rotate it and report it to the security lead within 1 hour.
2. Remove names and identifiers from examples when the task does not need them.
3. Sending personal data to an AI supplier is a disclosure under the NDPA and, for EU customers,
   the GDPR (rules R-1 and R-4). The Head of Compliance confirms the legal basis before any tool is
   approved for personal data.

## 7. Checking AI output

1. Check every AI output before you use it, send it or publish it. AI tools state wrong facts with
   confidence.
2. Do not send AI-written text to a customer, a regulator or a merchant without a person reading
   it first.
3. AI must not make a final decision about a person (a refund dispute, a merchant onboarding, a
   hiring choice, a fraud block that cannot be reversed) without human review. The NDPA (section 37) gives a person the right not to be subject to a
   decision based solely on automated processing that has legal or similarly significant effects.
   Not checked: GDPR Article 22. The Head of Compliance, as data protection officer, confirms how
   both apply.

### AI-generated code

AI-written code goes through the normal pull request review. Code that touches payments,
authentication, access control, cryptography or customer data needs a second reviewer, whoever
wrote it. The CTO keeps the list of these sensitive code paths.

Rules:

1. The author must understand every line they submit, whoever or whatever wrote it.
2. AI-generated code passes the same pipeline security checks as any other change (risk appetite
   row 6).
3. Check new dependencies that an AI tool suggests. A package name that does not exist, or that is
   close to a real name, can be a trap.

## 8. Approving a new AI tool or AI feature

The security lead assesses each new AI tool or feature. The CTO approves it (risk appetite row 6).
If the tool will receive Restricted data, the CEO approves it (risk appetite row 1). Until April
2027, the consultant does the assessment.

The assessment checks:

1. **Data terms:** whether the supplier trains its models on SigKollect's prompts, how long it
   keeps them, and where it stores them.
2. **Access:** single sign-on, MFA, and whether an admin can see and remove users.
3. **Supplier:** the supplier assessment in risk appetite row 5, with security and breach terms in
   the contract.
4. **Legal:** the Head of Compliance confirms the legal basis for any personal data.
5. **Data classes:** which classes from section 3 the tool may receive.

For an AI feature that SigKollect builds, the assessment also checks:

6. **Prompt injection:** a threat model for untrusted content reaching the model (OWASP Top 10 for
   LLM Applications 2025, LLM01: genai.owasp.org).
7. **Tools and actions:** each tool the AI can call, and the permission it needs. No AI system
   combines access to private data, exposure to untrusted content and a way to send data out,
   unless a person approves each outgoing action. (This is Simon Willison's "lethal trifecta":
   simonwillison.net, June 2025.)
8. **Logging:** prompts, tool calls and actions are logged, without Restricted data in the logs.
9. **Testing:** the feature is tested against prompt injection before release, and after each
   model change.

## 9. AI register

The security lead keeps a register of approved AI tools and features. Each entry records:

| Field | Example |
|---|---|
| Tool or feature | |
| Supplier | |
| Business owner | |
| Data classes allowed | |
| Approved by, and date | |
| Review date | One year after approval, or earlier if the supplier changes its terms |

A tool leaves the register when it fails its review, when the supplier changes its data terms in
a way that fails section 8, or when nobody uses it.

## 10. Exceptions

An exception to this policy must be written, have an end date, and be approved by the person who
would approve the tool under section 8. An exception never allows secrets in a prompt, and never
allows Restricted data in a tool that is not under SigKollect's control.

## 11. Reporting and breaches of this policy

1. Report a mistake at once, without fear of blame (charter principle 5). Examples: customer data
   pasted into an unapproved tool, or an AI output sent to a customer without a check.
2. Restricted data sent to an unapproved tool is a suspected personal data breach. It follows
   the governance cadence, part 3: the security lead hears within 1 hour.
3. Hiding a breach of this policy, or repeating it after a warning, is a disciplinary matter for
   the Head of People.

## 12. Review

The security lead reviews this policy each year, and earlier when:

- SigKollect builds a new AI feature into a product;
- a regulation on AI or data changes for Nigeria or the EU (rules R-1 and R-4);
- an incident involves an AI tool.

The security steering committee approves each new version (RACI row 7).
