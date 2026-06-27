# Reddit Template — AI YouTube Studio OS

Niche template for Reddit Mystery content — r/UnresolvedMysteries, r/NoSleep, r/AskReddit strange stories, and other platform-origin mystery content.

**Template version:** 1.0
**Compatible with prompt versions:** All v1.x prompts
**Niche IDs covered:** `reddit_mystery`
**Primary languages:** `en`, `vi`
**Last updated:** 2026-06-27

---

## Template Overview

Reddit mystery content is uniquely structured: the source material is typically a specific post (or series of posts) on Reddit or another platform. The story exists within a community context — there are comments, theories, updates, and often the mystery of what happened to the original poster. The content must honor the original post faithfully while adding investigative depth and narrative shape.

This template differs from others in that the source material is often unverified personal account — the "mystery" includes whether the story is true. This must be handled honestly.

## Niche Parameters

| Parameter | Value |
|---|---|
| `niche_id` | `reddit_mystery` |
| `primary_platforms` | Reddit, 4chan (archived), Twitter/X threads, forum posts |
| `source_verification_standard` | LOWER (personal accounts) — but must acknowledge uncertainty |
| `ending_type` | `open_question` or `op_disappeared` or `update_found` |
| `fictional_content_allowed` | Yes (NoSleep is fiction) — must be labeled |
| `screenshot_required` | Yes — original post must be shown |

---

## Stage Addendum: stage_01 (Research)

### Required Research Elements for Reddit Content

**Primary source documentation:**
- Locate the original post URL (or archived version via web.archive.org)
- Note the subreddit, post date, and username (if still public)
- Record upvotes, comment count, and awards at the time of research (use archive for historical data)
- Note whether the post has been deleted, the account deleted, or the subreddit quarantined/banned

**Community research:**
- Find the top 5-10 comments and their content
- Note whether any comments provided an explanation or update
- Search for follow-up posts by the same user (OP) across Reddit
- Search external platforms (Twitter, news) for coverage of the post

**Background verification (for non-fiction posts):**
- Attempt to verify whether the described events could have occurred
- Search for news coverage of similar events in the described location/time period
- Note any internal inconsistencies in the story that could indicate fabrication
- Do not attempt to identify the OP's real-world identity

**For NoSleep and explicitly fictional content:**
- NoSleep content is labeled fiction by the subreddit rules — acknowledge this upfront
- Research the author's other works (if relevant to the story's context)
- Do not attempt to verify fictional events as real

### Platform-Specific Research Notes

| Platform | Research Approach |
|---|---|
| Reddit (active) | Direct URL — note current status |
| Reddit (deleted) | web.archive.org snapshot — note archive date |
| Reddit (quarantined subreddit) | Pushshift archive (if accessible) or screenshot documentation |
| 4chan (archived) | archived.moe or desuarchive — note thread number and board |
| Twitter/X threads | threadreaderapp.com or archive for long threads |
| Old forums (SomethingAwful, etc.) | Internet Archive — note forum section |

---

## Stage Addendum: stage_02 (Source Verifier)

### Reddit-Specific Source Verification

- **Reddit posts are personal accounts, not verified facts.** The "source" is the post itself. Verify: post existence, date, subreddit, and community reception — not the factual truth of the story (that is separate).
- **For verification of claimed events:** Apply standard verification — news search, local records, geographic plausibility. If events cannot be verified, label the story as `[Unverified personal account]` in the research file.
- **Community corroboration:** If multiple commenters independently confirm aspects of the story, note this — it increases credibility without proving the story.
- **"OP confirmed" updates:** If OP provided a follow-up confirming or explaining events, document the follow-up as a separate source entry.
- **NoSleep disclaimer:** For confirmed NoSleep fiction, do not apply the standard fact-checking process. Instead, verify: subreddit (r/NoSleep), author, post date, and whether the author has acknowledged fictional nature.

---

## Stage Addendum: stage_03 (Story Outline)

### Required Narrative Structure for Reddit Mystery

Use the **Reddit Narration Structure** from STYLE_GUIDE.md:

**Required beats (must all appear):**

1. **Platform Context Beat** — Establish where this story comes from and why the community pays attention to it. (20-30 seconds)
2. **The Post Itself** — Read or paraphrase the original post faithfully. This is the core content. (30-50% of video)
3. **Community Reaction Beat** — What did commenters think? What theories emerged? Were there any expert or insider comments?
4. **The Update Beat (if exists)** — Did OP update? Did the story develop? What was the outcome?
5. **The Current Status Beat** — Where does the story stand now? Is the account still active? Has anyone ever explained this?
6. **The Open Question** — What remains unknown? Why does this story stay with people?

**Parameter Override:**
| Parameter | Base Value | This Template | Reason |
|---|---|---|---|
| `hook_type` | `shocking_fact` | `in_media_res` | Start mid-story, then provide context |
| `person_for_post` | `third` | `first` | Voice the post in first person |
| `community_beat` | optional | required | Community is half the content |

**For NoSleep content:** The outline must clearly mark which sections are narrating fiction vs. providing authorial/meta context about the story.

---

## Stage Addendum: stage_04 (Script Writer)

### The Post Narration Beat — Critical Requirements

When narrating the original Reddit post:
- Voice it in **first person** as the original poster
- Use **faithful paraphrase** — capture the original voice, do not rewrite in the narrator's style
- If the post has distinctive phrasing, slang, or voice — preserve it
- If quoting directly (recommended for key passages): use `"direct quote"` punctuation
- Do not add information to the post's story that the OP did not include
- Do not editorialize about the post while narrating it — save that for the community reaction beat

**Transition markers in the script:**
```
[CONTEXT: narrator voice]
"This story was originally posted to r/[subreddit] in [year] by a user known only as [username]."

[POST NARRATION: first person, original poster voice]
"I don't know how to explain what I saw that night..."

[RETURN TO NARRATOR]
"The post received [X] comments within the first hour. What followed would only deepen the mystery."

[COMMUNITY BEAT: narrator voice]
```

### Truth Status Labeling in Script

The script must make the truth status clear to the audience at least once:

| Post Type | Required Statement |
|---|---|
| Verified real event | "The events in this post have been corroborated by [source]." |
| Unverified personal account | "We cannot verify whether these events occurred as described." |
| NoSleep fiction | "This is a work of fiction originally posted to r/NoSleep, a creative writing subreddit." |
| Disputed/hoax suspected | "Several researchers have raised questions about whether this account is genuine." |

This statement appears in the Platform Context Beat — not repeatedly throughout the script.

### Forbidden Script Constructions for This Template

- Presenting an unverified Reddit account as a verified true story
- Speculating about the OP's real identity
- Changing details of the original post for narrative convenience
- Presenting NoSleep fiction as a real event

---

## Stage Addendum: stage_05 (Story Bible)

### Additional Entity Types for Reddit Mystery

| Entity Type | Required Format | Example |
|---|---|---|
| Reddit username | Exactly as posted (preserve capitalization) | `u/ThrowawayStrangeNight` |
| Post URL | Full URL or archive URL | `reddit.com/r/UnresolvedMysteries/comments/abc123` |
| Subreddit | Exact name with r/ prefix | `r/UnresolvedMysteries` |
| Post date | YYYY-MM-DD | `2021-03-14` |
| Upvote count (at research time) | Integer | `14,200` (as of 2026-06-27) |
| Notable comment usernames | As posted | `u/DetectiveMike2019` |

---

## Stage Addendum: stage_06 (Scene Splitter)

### Visual Vocabulary for Reddit Mystery

**Required visual beats:**
- **First scene:** Show the Reddit post (screenshot — dark mode, highlighted OP text)
- **Post narration scenes:** Keep Reddit post visible in corner (picture-in-picture style suggestion) or cut between AI atmosphere and post text
- **Community reaction beat:** Show top comments (screenshot with usernames visible unless private content)
- **Update beat (if exists):** Show the update post/comment

**Visual hierarchy for this niche:**
1. Screenshot of original post (priority)
2. Screenshots of key comments
3. Screenshot of any related external coverage
4. Atmospheric AI images for mood between readings
5. Maps or location imagery if the story involves a real place

**Screenshot preparation notes (for storyboard):**
- Note whether screenshots need usernames blurred (for sensitive or potentially private content)
- Note if the subreddit interface should show specific flair, awards, or vote count
- Reddit dark mode preferred — more atmospheric than light mode

---

## Stage Addendum: stage_07 (Image Finder)

### Image Sourcing for Reddit Mystery

**Screenshots are the primary visual asset for this niche:**
- Direct URL to the original post (take fresh screenshot + archive link)
- Archive version for deleted posts (web.archive.org)
- Comment thread screenshots (identify specific comments to capture)

**Supplementary real imagery:**
- If the post describes a real location: find real photos of that location
- If the post references a real event: find news coverage of that event
- If the post is set in a recognizable real place: Google Maps Street View

**AI image criteria for this niche:**
- Atmospheric and slightly surreal — not photorealistic (the story may be fiction)
- Should feel like a memory or a dream, not a documentary
- Color: warmer and darker than documentary style — dark browns, deep blues

---

## Stage Addendum: stage_08 (Image Prompt Generator)

### Aesthetic Style for Reddit Mystery AI Images

**Visual style:** Impressionistic unease. Not photorealistic — the slightly unreal quality mirrors the uncertainty of the source material.

**Prompt keywords:**
```
"dreamlike horror, dark warm tones"
"impressionistic, slightly blurred, atmospheric dread"
"dim interior, single light source, night"
"forest at night, flashlight beam, dense trees"
"abandoned room, personal belongings, no people"
"digital illustration style, dark, mysterious"
```

**For NoSleep fiction:** AI images can be more stylized — closer to dark illustration or horror art. The fictional framing allows more expressionistic interpretation.

**Color direction:**
- Warm dark: deep browns, amber, faded orange-black
- Cold variation: steel blue-gray for unsettling outdoor scenes
- Avoid: red unless specifically referenced in the story

---

## Stage Addendum: stage_09 (Voice Director)

### Voice Character for Reddit Mystery

**Delivery philosophy:** Intimate storytelling. The narrator is sharing a story they find genuinely disturbing or compelling — not performing horror, but conveying real unease.

**The Post Narration Beat:**
- Shift to first-person voice naturally — the listener should feel they are the OP
- Pace: slightly faster than the context beats — this is someone telling their own story
- Emotional quality: contained, but slightly unsteady — as if recounting something still unresolved

**Community Reaction Beat:**
- Read comment text in a slightly different register — clinical or curious, not frightened
- Upvote count and community reception: delivered factually

**Update Beat (if exists):**
- If the update resolves the mystery: slightly deflated — "and then the mystery was solved" is always less satisfying than the mystery
- If the update deepens the mystery: slow down, let it land

**For Vietnamese narration (`vi`):**
- Match the conversational quality of the English delivery — Vietnamese narration can be warmer and more expressive than the documentary style
- Reddit content works well with a slightly younger, conversational Vietnamese voice

---

## Stage Addendum: stage_10 (YouTube SEO)

### SEO Strategy for Reddit Mystery

**Title patterns:**
- "I Found This on Reddit and I Can't Sleep" (engagement-first)
- "This Reddit Post Terrified the Internet in [Year]"
- "The Reddit Mystery That Nobody Could Explain"
- "r/[Subreddit]: [Brief Description of the Post]"

**Description structure:**
- Open with the platform context: "In [year], a Reddit post appeared in [subreddit] that would go on to receive [X upvotes]..."
- Include the subreddit name as a keyword
- Link to archived version of the original post in description (if available)

**Thumbnail text patterns:**
- `REDDIT MYSTERY`
- `OP DISAPPEARED`
- `STILL UNEXPLAINED`
- `WHAT DID THEY SEE?`

**Tags to always include for this niche:**
`reddit mystery`, `reddit story`, `r/unresolvedmysteries`, `r/nosleep`, `reddit true story`, `reddit horror`, `scary reddit posts`, `reddit narration`, `creepy reddit`, `unexplained reddit`

**For Vietnamese content:**
- Title: `Câu chuyện bí ẩn trên Reddit...`
- Include English tags alongside Vietnamese for diaspora audience reach
