# X Space Governance & Knowledge Graph Questions (Answer Log)

**Context:** There will be an X Space coming soon.  
**Intro video:** https://www.youtube.com/watch?v=50RFTBm7reU

Use this file to append answers as you find them (during the X Space, in follow-up docs, or from team members).  
Recommendation: keep answers short, and add links under **Sources / Evidence**.

---

## How to use this log
- **Status:** `unanswered` → `partial` → `answered` → `needs follow-up`
- Add dates in **Answer (latest)** and keep older notes under **History / Notes**.
- Put links, screenshots, docs, and references under **Sources / Evidence**.

---

## 1) What metrics define “useful” (usage in apps, query success, citations, downstream reuse)?

**Status:** unanswered  
**Answer (latest):**  
_TBD — no concrete metrics stated in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no explicit metrics found

---

## 2) What metrics define “better organized” (link density, ontology completeness, dedup rate, resolution time for disputes)?

**Status:** unanswered  
**Answer (latest):**  
_TBD — no concrete metrics stated in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no explicit metrics found

---

## 3) How do you separate “what is true” objects (claims/evidence) from “what is good” objects (preferences/goals) in the graph structure?

**Status:** unanswered  
**Answer (latest):**  
_TBD — AMA discusses facts vs claims, but not “true vs good” object separation._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no explicit “true vs good” modeling described

---

## 4) When two groups disagree, what’s the intended outcome: one canonical answer, multiple competing views, or segmented by space?

**Status:** answered  
**Answer (latest) (2026-01-30):**  
**Pluralism by design.** GEO aims to support **multiple viewpoints** rather than a single centralized canonical answer. Disagreement can be represented (a) **within a space** using **claims** (with support/oppose arguments + signals), and/or (b) by **forking/creating another space** if a community wants different rules or outcomes.

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: pluralism / coexistence of viewpoints (00:17:00–00:17:23)  
- AMA transcript: claims to accommodate differing views (00:18:39–00:19:35)  
- AMA transcript: fork/create spaces if governance goes sideways (00:30:08–00:30:24)

---

## 5) What does “shared truth” mean operationally? Majority vote, expert weighting, evidence scoring, or something else?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
Not defined as a single mechanism. Current operational signals described:  
- Two roles: **editors** and **members**.  
- Some decisions require a **vote of editors**.  
- Members can **publish knowledge** and **upvote/downvote** to produce signal.  
- More granular **reputation weighting tools** are planned (not yet the default system).

**History / Notes:**  
- Needs follow-up: whether “shared truth” is expected to emerge via votes, evidence scoring, reputation, or per-space rules.

**Sources / Evidence:**  
- AMA transcript: roles + editor votes + member signaling (00:15:47–00:16:17)  
- AMA transcript: reputation weighting tools planned (00:16:27–00:16:40)

---

## 6) How do you represent uncertainty (ranges, confidence, dispute state) and change over time (versions, retractions)?

**Status:** unanswered  
**Answer (latest):**  
_TBD — no concrete uncertainty/versioning scheme described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no explicit confidence/ranges/versioning/retractions found

---

## 7) What’s the minimum evidence standard for a “fact” node vs a “claim” node?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
They strongly recommend using **claims** to model contentious assertions so disagreement can coexist without “bifurcating” a space. However, they **do not specify a minimum evidence threshold** that cleanly distinguishes “fact” vs “claim.”

**History / Notes:**  
- Needs follow-up: explicit standard for when something is allowed to be asserted as “fact” vs must remain “claim.”

**Sources / Evidence:**  
- AMA transcript: “fact” framing can bifurcate; “claim” framing allows coexistence + signaling + supporting/opposing arguments (00:18:51–00:19:35)

---

## 8) What signals do you think should define reputation: peer review, external credentials, accuracy track record, citations, or stake/points?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
No finalized reputation metric set was stated. What was described:  
- Current default governance has **editors** (more power) and **members** (publish + signal).  
- They are building **more granular reputation tools** to weight governance actions over time.

**History / Notes:**  
- Needs follow-up: whether citations/track record/credentials/stake/peer review become first-class inputs.

**Sources / Evidence:**  
- AMA transcript: editors vs members + editor votes + member signals (00:15:47–00:16:17)  
- AMA transcript: granular reputation tools planned (00:16:27–00:16:40)

---

## 9) Can “domain expert” status really be verified, and if so how? How do you avoid credentialism and avoid “anyone can assert anything” chaos?

**Status:** unanswered  
**Answer (latest):**  
_TBD — no verification/credentialing mechanism described in the AMA transcript._

**History / Notes:**  
- They note domain experts should be able to “spot things that are wrong” in review, but not how expert status is verified.

**Sources / Evidence:**  
- AMA transcript: domain experts can spot wrong info during review (00:40:34–00:40:38)

---

## 10) What’s the escalation path for disputes: reviewer → moderators → space governance → root governance?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
A formal escalation ladder wasn’t described. What was described operationally:  
- **Editors** have tools to **remove** bad actors from a space.  
- If editors abuse power, people can **move / fork / create their own space**.

**History / Notes:**  
- Needs follow-up: explicit escalation path + appeals within a space; any “root” governance process.

**Sources / Evidence:**  
- AMA transcript: auditable actions + editors remove troublemakers (00:29:11–00:29:40)  
- AMA transcript: fork/create spaces if editor powers go too far (00:30:02–00:30:24)

---

## 11) What parts of governance are space-local vs global and why?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
They state governance is **not one-size-fits-all** and should vary by space (e.g., **science** slower/more rigorous vs **news** faster). GEO aims to provide **sensible defaults** plus tools for **space-level customization**.

**History / Notes:**  
- Needs follow-up: what is globally enforced (if anything) vs always per-space.

**Sources / Evidence:**  
- AMA transcript: governance not one-size-fits-all; science vs news; defaults + customization (00:41:20–00:42:21)

---

## 12) Who awards points (automation, reviewers, voting, staff)? What’s the auditability?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
They emphasize **auditability**: actions are transparent/auditable/onchain (publishing, votes/signals). They also say they’ll “do our best” to track contribution value with **points**, but **do not specify** the exact awarding mechanism (automation vs reviewers vs staff vs voting).

**History / Notes:**  
- Needs follow-up: explicit points pipeline and who/what triggers point issuance.

**Sources / Evidence:**  
- AMA transcript: actions transparent & auditable; upvote/downvote etc. (00:29:11–00:29:23)  
- AMA transcript: “track with points” the value of contributions (00:31:06–00:31:12)

---

## 13) How do you prevent “content volume farming” while still rewarding consistent contributions?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
No explicit “volume farming” policy described, but they emphasize:  
- **Onchain/auditable actions** make behavior visible.  
- **Editors** can remove bad actors from a space.

**History / Notes:**  
- Needs follow-up: concrete anti-farming heuristics and “quality > quantity” scoring.

**Sources / Evidence:**  
- AMA transcript: auditable actions + editors can remove troublemakers (00:29:11–00:29:40)

---

## 14) If points eventually map to power, what protections exist against early insiders dominating?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
Not addressed directly as “early insiders.” They emphasize:  
- **Openness**: anyone can join; good work should allow rising to the top.  
- **Exit/fork**: if editor power is abused, people can fork/create a space.

**History / Notes:**  
- Needs follow-up: concrete safeguards against early capture (caps, decay, quorum rules, checks & balances).

**Sources / Evidence:**  
- AMA transcript: openness + rising to the top (00:28:37–00:28:52)  
- AMA transcript: fork/create spaces if editors go too far (00:30:02–00:30:24)

---

## 15) What does a “good bounty” include: acceptance criteria, schema/ontology targets, citation requirements, sample outputs?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
No bounty template requirements were listed. The only concrete statement: they’re experimenting with **bounty-based** work as one possible mechanism.

**History / Notes:**  
- Needs follow-up: bounty template + “definition of done.”

**Sources / Evidence:**  
- AMA transcript: bounty-based experimentation mentioned (00:38:16–00:38:19)

---

## 16) How are bounties prioritized? By votes, staff, impact metrics, or “space leads”?

**Status:** unanswered  
**Answer (latest):**  
_TBD — no prioritization mechanism described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no bounty prioritization detail found

---

## 17) Is there a standard bounty template you want everyone to use?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no standard bounty template described

---

## 18) What prevents 10 duplicate ontologies for “Bitcoin” across crypto/AI/politics?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no dedup / cross-space ontology prevention described

---

## 19) What’s the exact week-to-week curator workflow: discover → model → add sources → publish → review → dispute?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
Short rollout sequence described (near-term):  
- Next week: curators go through **onboarding flow** + give feedback.  
- Following week: spaces go live; people **join spaces and start publishing knowledge**.  
- Tools: **GeoGenesis** to browse/contribute; a **curator app** to discover bounties/work.

**History / Notes:**  
- Needs follow-up: the “steady-state” weekly loop including dispute/resolution.

**Sources / Evidence:**  
- AMA transcript: onboarding next week; spaces live following week; start publishing; tools described (00:21:28–00:22:48)

---

## 20) What’s the review flow in detail (who reviews, turnaround expectations, what gets blocked)?

**Status:** answered  
**Answer (latest) (2026-01-30):**  
Review is **editor-driven**: editors of a space are responsible for quality. When someone publishes a proposal, it goes to **review** that looks like a **GitHub pull request** (diffs visible). Editors can do checking; they plan to add AI/statistical sampling and potentially peer-review-like processes. Review processes may differ by space (science vs news).

**History / Notes:**  
- Turnaround expectations / SLAs were not stated.

**Sources / Evidence:**  
- AMA transcript: editors responsible; review tools; PR-like diffs (00:39:57–00:40:33)  
- AMA transcript: add AI/sampling; governance differs by space (00:40:39–00:42:21)

---

## 21) What’s the fastest “hello world” contribution that teaches the system correctly?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no “hello world” contribution described

---

## 22) If something sensitive gets published by mistake, what remediation exists (tombstoning, redaction markers, blocklists)?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no remediation/takedown process described

---

## 23) What is your copyright/IP policy? What’s allowed to be uploaded vs only referenced?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no copyright/IP policy described

---

## 24) Do you require “AI-assisted” labeling? Do you track prompts/derivations for accountability?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no labeling/prompt tracking described

---

## 25) How do you plan to handle AI-generated misinformation that gets through review? Reputation hits?

**Status:** partial  
**Answer (latest) (2026-01-30):**  
No explicit “reputation penalty” policy described. They emphasize editor responsibility + review, and plan to add tools (AI verification + statistical sampling) to improve review quality over time.

**History / Notes:**  
- Needs follow-up: whether publishing wrong info creates penalties, reversions, or reputation impacts.

**Sources / Evidence:**  
- AMA transcript: editors responsible; PR-like review; add AI/sampling (00:39:57–00:40:59)

---

## 26) What is the appeals process for false positives in your fraud/sybil/etc detection?

**Status:** unanswered  
**Answer (latest):**  
_TBD — not described in the AMA transcript._

**History / Notes:**  
- 

**Sources / Evidence:**  
- AMA transcript: no sybil appeals process described
