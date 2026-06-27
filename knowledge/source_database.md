# Source Database — AI YouTube Studio OS

Registry of all verified sources used across all production projects. Written to by the Memory Engine after each project. Read by the Research prompt (to surface known sources) and the QA Engine (to cross-reference claims).

**Schema version:** 1.0
**Last updated:** [Updated automatically by Memory Engine]
**Record count:** 0 (seed file — no projects completed yet)

---

## Schema Definition

Each source record has the following fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `source_id` | string | yes | Unique identifier: `src_YYYYMMDD_NNN` |
| `source_name` | string | yes | Full name of the source |
| `outlet_platform` | string | yes | Publisher, website, or platform |
| `year` | integer | yes | Year of publication |
| `url` | string | no | Full URL (if confirmed to exist) |
| `url_confirmed` | boolean | yes | Whether URL has been verified active |
| `type` | enum | yes | See Type Enum below |
| `language` | string | yes | ISO 639-1 code of the source |
| `topics_covered` | string[] | yes | Topics this source has been used for |
| `reliability_rating` | enum | yes | `high`, `medium`, `low`, `unrated` |
| `times_used` | integer | yes | Count of projects that used this source |
| `first_used_project` | string | yes | Project slug of first use |
| `last_used_project` | string | yes | Project slug of most recent use |
| `deprecated` | boolean | no | If true: source is outdated or removed |
| `deprecation_note` | string | no | Why deprecated |
| `notes` | string | no | Any special handling instructions |

### Type Enum

| Value | Meaning |
|---|---|
| `news_major` | Major national/international news outlet |
| `news_local` | Regional or local news outlet |
| `documentary` | Named documentary with identified director/broadcaster |
| `academic` | Peer-reviewed paper or academic book |
| `government_record` | Official government publication or database |
| `reddit_post` | Reddit post (treat as personal account, not verified fact) |
| `social_media` | Twitter, Facebook, TikTok, or other social platform post |
| `wiki` | Wikipedia or similar collaborative encyclopedia |
| `paranormal` | Paranormal-focused outlet or publication |
| `book_nonfiction` | Published non-fiction book |
| `forum` | Internet forum post (non-Reddit) |
| `archive` | Internet Archive, Wayback Machine, or document archive |
| `other` | Anything that does not fit the above |

### Reliability Rating Criteria

| Rating | Criteria |
|---|---|
| `high` | Major news outlet, government record, peer-reviewed academic, named documentary |
| `medium` | Established local news, non-fiction book, reputable forum thread with corroboration |
| `low` | Single social media post, paranormal outlet, Wikipedia without primary source |
| `unrated` | Source added but not yet evaluated across multiple projects |

---

## Source Records

*This section is populated automatically by the Memory Engine after each project.*

*No records yet — this is a seed file.*

---

## Source Index

*Searchable index — maintained by Memory Engine.*

### By Topic

*Empty — populated after first project.*

### By Outlet

*Empty — populated after first project.*

### By Language

*Empty — populated after first project.*

### By Reliability Rating

*Empty — populated after first project.*

---

## Aggregate Statistics

*Updated by Memory Engine after each project.*

| Metric | Value |
|---|---|
| Total sources registered | 0 |
| High reliability | 0 |
| Medium reliability | 0 |
| Low reliability | 0 |
| Unrated | 0 |
| Sources with confirmed URLs | 0 |
| Sources with unconfirmed URLs | 0 |
| Most-used source | — |
| Highest-use topic | — |

---

## Memory Engine Write Protocol

When a project completes, the Memory Engine:

1. Reads `research_verified.md` from the project
2. For each source in the Sources section:
   a. Search existing records for matching `source_name` + `outlet_platform` + `year`
   b. If match found: increment `times_used`, add current topic to `topics_covered`, update `last_used_project`
   c. If no match: create new record with `source_id = src_YYYYMMDD_NNN` (NNN = sequential number for that date)
3. Update aggregate statistics section
4. Update `last_updated` in file header

Write is atomic — the full file is updated at once, not appended line by line.
