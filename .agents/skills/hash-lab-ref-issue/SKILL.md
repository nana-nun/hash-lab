---
name: hash-lab-ref-issue
description: Use with hash-lab-issue-runner when a GitHub Issue has the primary label t:ref or asks for reference collection, literature review, papers, links, BibTeX entries, DOI/ePrint/DBLP metadata, or reading notes for hash-lab.
---

# Hash Lab Reference Issue

Use this skill after `hash-lab-issue-runner` has confirmed the Issue, labels, branch, and safety scope.

## Check Before Work

- Confirm the requested topic is relevant to toy hash, reduced-round SHA-like hash, avalanche measurement, neural distinguishers, small SAT/SMT work, or local simulations.
- Prefer primary sources: papers, standards, proceedings pages, DOI pages, IACR ePrint, DBLP, author pages, or official project pages.
- Do not add references for misuse-enabling attacks on real wallets, keys, signatures, live networks, mining pools, or production systems.
- Capture uncertainty plainly when metadata is incomplete.

## Source Metadata

For papers, capture as many of these fields as available:

- Paper title
- Authors
- Year
- Venue or publication type
- DOI when available
- Stable URL, preferably DOI, IACR ePrint, DBLP, or official publisher page
- BibTeX status

## File Placement

- Add BibTeX-manageable papers to `references/papers.bib`.
- Add human-readable summaries to `references/reading-list.md`.
- Add web pages, tools, datasets, standards pages, or non-paper links to `references/links.md`.
- Add deeper reading notes to `references/notes/` only when the Issue asks for notes or the source needs more than a short summary.

## Verification

- Check for duplicate BibTeX keys before adding entries.
- Prefer stable BibTeX keys in the form `<firstauthor>_<shorttitle>_<year>`.
- Use ASCII-safe BibTeX escapes for non-ASCII names when practical.
- Verify every added reference has title, authors or organization, year, and DOI or URL.

## Done Criteria

- The requested number of sources is added or the shortfall is explained.
- Each source has a short Japanese note explaining its relevance to hash-lab.
- PR or final response names the updated reference files and any sources that still need deeper reading.
