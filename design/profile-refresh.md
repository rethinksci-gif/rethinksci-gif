# GitHub profile refresh — 2026-09-28

Scope: the profile README in `rethinksci-gif/rethinksci-gif`. GitHub's surrounding UI and pinned repository configuration are unchanged.

## Maintained references

- https://github.com/stats-organization/github-stats-extended — latest commit checked 2026-09-28; README demonstrates `picture` with light/dark media sources. Used this pattern with original, repository-hosted SVGs.
- https://github.com/DenverCoder1/readme-typing-svg — latest commit checked 2026-09-17; reviewed README banner, sizing and alt-text examples. Used a static, self-contained banner for this profile.

Excluded lowlighter/metrics (latest default-branch commit returned 2023-12-18) and anuraghazra/github-readme-stats (deprecation notice directs users to Stats Extended).

## Design

A forest/cream research identity, responsive theme-aware banner, three stacked project sections, direct reading/source/RSS links and an optional Chinese introduction. Layout uses GitHub-supported Markdown and HTML, without custom CSS, JavaScript, third-party image services or invented statistics. Text remains readable independently of the SVG.

No external source code or artwork copied; no additional runtime dependencies or scheduled jobs.

# Live profile — 2026-10-09

## Maintained references

- https://github.com/simonw/simonw (pushed 2026-10-09) and https://github.com/tw93/tw93 (pushed 2026-10-09): scheduled Action rewrites marker-delimited README blocks from the owner's own feeds. Adopted for the "Latest issues" table.
- https://github.com/antfu/antfu (pushed 2026-10-09): compact centered `<samp>` link bar. Adopted for top navigation.
- https://github.com/gautamkrishnar/blog-post-workflow (pushed 2026-10-07): reviewed as an off-the-shelf RSS-to-README action. Not used, because the Electrification site has no feed and the briefing feeds need custom titles.

## Design

`build_readme.py` (standard library only) reads the AIM4R and Plastic Signal Atom feeds, the CCU RSS feed and the Electrification sitemap, and rewrites the block between `<!-- latest starts -->` and `<!-- latest ends -->`. A source that fails keeps its previous row. `.github/workflows/build.yml` runs it daily at 06:37 UTC and commits only when the README changes.

The garden's Quartz `index.xml` is excluded: every item carries the build date, which would make unchanged notes look new.

## Reading paths — 2026-10-10

The introduction now states the reader benefit and includes a visible Chinese summary. Three starting paths lead to the research garden, engineering cases and current briefings. Publication names open the live sites, with separate repository and subscription links. The Chinese guide is visible and linked from the introduction; a contact section invites sources, corrections and research questions.

The daily latest-issue markers and row format are preserved so the existing updater remains compatible. The dark banner arrow now uses dark ink against its light circle for legibility. All visual assets remain repository-hosted, with no added dependencies.
