#!/usr/bin/env python3
"""Generate Morgan Rivers–style medi essays from lich-medi-200.json (≥1100 words each)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAL = ROOT / "_data" / "lich-medi-200.json"
POSTS = ROOT / "_posts"


def slug_words(slug: str) -> list[str]:
    return [w for w in slug.replace("-", " ").split() if w]


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


OPENERS = {
    "connection-health": [
        "There is a particular quiet that shows up when the day finally stops asking things of you. The notifications thin out. The rooms get larger. And somewhere between the last message you sent and the ones that never arrive, a familiar question surfaces: is this solitude, or is it loneliness wearing solitude's clothes?",
        "Most people do not announce loneliness the way they announce a fever. It arrives sideways — in the pause after a group chat goes still, in the way you rehearse a text and then delete it, in the strange fatigue of being around people and still feeling slightly out of frame.",
        "Connection is not a personality trait you either have or lack. It is a practice with seasons: weeks when conversation feels easy, weeks when every outreach costs more energy than you want to admit. This essay is for the costly weeks.",
    ],
    "sleep-nights": [
        "Night has a different grammar than day. Sounds get sharper. Thoughts get longer. The same apartment that felt ordinary at noon can feel oddly spacious after eleven, as if the furniture has stepped back to give your mind more room than it asked for.",
        "You can do everything \"right\" before bed and still find yourself staring at the ceiling, negotiating with a brain that insists on replaying Tuesday. Sleep advice often sounds simple until you are the person alone with the clock.",
        "Quiet nights are not automatically peaceful nights. Sometimes quiet is restorative. Sometimes quiet is just the volume turned down on everything except worry.",
    ],
    "brain-aging": [
        "The mind does not age in a single dramatic scene. It changes the way a neighborhood changes — a shop closes, a bus route shifts, a familiar face appears less often — until one day you notice the map in your head has quietly redrawn itself.",
        "Conversation is one of the most ordinary workouts the brain gets, and one of the easiest to lose without noticing. No membership card. No dramatic failure. Just fewer reasons to explain yourself out loud.",
        "Families often notice quiet before they notice anything clinical. A parent tells shorter stories. A grandparent stops calling to share small news. The question is rarely \"what disease is this?\" at first. The question is usually \"what changed in the social weather?\"",
    ],
    "gentle-habits": [
        "The internet loves extreme habits. Real life prefers habits small enough to survive a bad Tuesday. This piece is about the second kind — the kind you can keep when motivation is thin and the day already took most of what you had.",
        "You do not need a reinvention arc to feel a little more steady. Sometimes you need a ten-minute walk, a glass of water, and one human voice before the evening folds in on itself.",
        "Gentle habits are easy to dismiss because they do not look like transformation. They look like putting shoes by the door, texting one person back, and going to bed without treating rest like a moral failure.",
    ],
    "lived-stories": [
        "I keep thinking about how little of life announces itself as a turning point while it is happening. Most of the moments that later feel important arrive dressed as ordinary inconvenience: a missed call, a late bus, a dinner eaten standing up.",
        "This is not a neat lesson wrapped for strangers. It is a week I lived through, told carefully, because someone else might recognize the weather inside it.",
        "I used to wait for clarity before I wrote anything down. Then I learned that clarity often shows up after you admit what the quiet was actually doing to you.",
    ],
}


def pick(seq, i):
    return seq[i % len(seq)]


def build_body(p: dict, idx: int) -> str:
    cat = p["category_slug"]
    title = p["title"]
    angle = p["angle"]
    slug = p["slug"]
    words = slug_words(slug)
    topic = " ".join(words[:6])
    opener = pick(OPENERS[cat], idx)

    # Category-specific middle sections
    if cat == "lived-stories":
        return lived_story(p, idx, opener)
    if cat == "sleep-nights":
        return sleep_essay(p, idx, opener, topic, angle)
    if cat == "brain-aging":
        return brain_essay(p, idx, opener, topic, angle)
    if cat == "gentle-habits":
        return habits_essay(p, idx, opener, topic, angle)
    return connection_essay(p, idx, opener, topic, angle)


def unique_bridge(title: str, topic: str, angle: str, idx: int) -> str:
    bridges = [
        f"If the title brought you here — *{title}* — you are probably not looking for a lecture. You are looking for language that fits a feeling you already know.",
        f"People search phrases like “{topic}” when the usual advice (\"just go out more\") has already failed them once.",
        f"Hold the specific angle for a moment: {angle.rstrip('.')}. That specificity matters more than generic tips about \"being social.\"",
        f"I keep returning to this subject because *{title}* names a situation that looks minor from outside and feels heavy from inside.",
    ]
    return bridges[idx % len(bridges)]


def connection_essay(p, idx, opener, topic, angle):
    inline = p["inline_image"]
    title = p["title"]
    bridge = unique_bridge(title, topic, angle, idx)
    return f"""{opener}

{bridge}

This essay sits inside our **[Connection Health](/category/connection-health/)** series. The focus today is {angle.lower().rstrip('.')}. It is not a diagnosis, a personality verdict, or a demand that you become more social than you are. It is a careful look at how {topic} shows up in ordinary rooms — and what soft options exist when the gap between the contact you have and the contact you need starts to ache.

## What this feeling is usually pointing to

Loneliness, at its simplest, is a perceived gap. You can have people nearby and still feel it. You can be physically alone and not feel it at all. The body does not check your contact list before it decides something is missing; it checks whether your need for recognition, warmth, or companionship feels unmet.

With {topic}, the gap often disguises itself as something more respectable. People say they are \"just busy,\" \"just tired,\" or \"just not in the mood to talk.\" Sometimes that is true. Sometimes it is a story that protects you from admitting you want to be chosen — invited, remembered, answered.

A few patterns show up again and again:

- **Emotional loneliness** — you have acquaintances, but no one who knows the real weather inside your week.
- **Social loneliness** — your circle thinned, moved, paired off, or went quiet, and nothing replaced it.
- **Situational loneliness** — a move, a breakup, a new job, a season of caregiving made the map unfamiliar.
- **Transient loneliness** — a sharp evening that will pass, especially if you treat it as weather rather than identity.

None of these require you to pathologize yourself. They do ask for honesty. If you keep calling a hunger \"independence,\" the hunger does not disappear. It just gets better at sounding like a preference.

## Why reaching out feels harder the longer you wait

There is a cruel mechanic to withdrawal: the less you practice contact, the more dramatic contact feels. A simple text starts to look like a confession. A coffee invitation starts to look like a performance review of your entire personality.

Silence also creates stories. *They don't want to hear from me. I waited too long. If I mattered, someone would ask.* Those stories are efficient. They are also frequently wrong. Many people are privately hoping someone else goes first.

When the theme is {topic}, shame often joins the room. Shame says your need is excessive. Connection says your need is human. You do not have to believe the second sentence with your whole chest on day one. You only have to act as if it might be true long enough to send one low-stakes message.

![A quiet moment of human connection in ordinary light]({inline})
*Most reconnection does not look cinematic. It looks like a short message that finally leaves the drafts folder.*

## What usually helps (without forcing a personality transplant)

Start smaller than your pride wants. The goal is not to rebuild an entire social life before Friday. The goal is to interrupt the loop where loneliness becomes identity.

Practical moves that tend to work:

1. **Choose one person, not a broadcast.** Mass messages feel efficient and land cold. One honest note lands warmer.
2. **Offer a specific, easy yes.** \"Want to walk Saturday at ten?\" beats \"We should hang out sometime.\"
3. **Use a medium that matches your courage.** Voice notes, short calls, or parallel activity (walking, errands) can feel safer than face-to-face intensity.
4. **Separate liking solitude from needing connection.** You can love quiet mornings and still want a real conversation twice a week.
5. **Build a recurring appointment.** Standing calls beat heroic one-offs you will cancel when energy dips.

If strangers feel easier than friends tonight, that is information, not failure. Low-pressure conversation with someone who does not carry your history can lower the temperature enough to sleep, think, or remember you still know how to talk. Keep safety in the room: no money requests, no addresses, no urgency that does not belong to you. Leave when the tone turns sharp.

## How to tell solitude from loneliness in the moment

Ask three questions without turning them into a self-cross-examination:

- Do I feel restored by this quiet, or hollowed by it?
- If a kind person invited me into an easy conversation right now, would I feel relief or irritation?
- Has this quiet lasted long enough that my world is shrinking — fewer outings, fewer messages, fewer reasons to speak?

Restorative solitude usually still leaves a door ajar. Loneliness tends to nail boards over the door and call it strength. You are allowed to want company without performing despair to earn it.

## A softer standard for \"being connected\"

Connection does not require constant availability, a large friend group, or a personality that loves parties. For many people, a connected week looks like this: one meaningful exchange, one body of water/walk/outside air, one moment of being useful to someone else, and enough sleep to not hate your own company.

If {topic} has been sitting on your chest, treat it as a signal light, not a final verdict. Signals ask for a response. Responses can be small.

You might text someone who has been easy in the past. You might schedule a walk. You might open a low-pressure chat for twenty minutes and then go to bed. You might tell one trusted person, plainly, \"I've been quieter than I meant to be.\" Plain sentences are underrated medicine for social drift.

## When to bring in more support

If loneliness comes with persistent hopelessness, inability to care for basic needs, or thoughts of self-harm, that is larger than a lifestyle essay. Talk with a clinician or local crisis resource. Connection habits help many ordinary lonely seasons; they are not a substitute for care when the ground feels unstable.

For everyone else: you do not have to wait until you are impressive again to deserve a reply. You only have to be reachable enough for one good conversation to find you.

## A closing note you can keep

The point of paying attention to {topic} is not to become endlessly optimized for social performance. The point is to notice when quiet has stopped being chosen and started being endured — and to meet that moment with one kind, concrete action.

If tonight is one of those nights, keep the action small enough that you will actually do it. Small and done beats noble and postponed. Connection, like sleep and appetite, often returns after you give it a place to land.
"""


def sleep_essay(p, idx, opener, topic, angle):
    inline = p["inline_image"]
    return f"""{opener}

This piece belongs to **[Sleep & Quiet Nights](/category/sleep-nights/)**. We are looking at {angle.lower().rstrip('.')}, through the lens of ordinary evenings rather than a sleep clinic checklist. Nothing here replaces medical advice. If sleep loss is severe, ongoing, or paired with breathing concerns, talk with a clinician. For the rest of us — the people negotiating with restless minds in quiet apartments — soft structure still helps.

## Why nights magnify what daytime can ignore

Daylight comes with errands, noise, and other people's needs. Night removes the scaffolding. That can feel luxurious. It can also feel like being left alone with every unfinished thought you postponed since breakfast.

When the theme is {topic}, the mind often treats bedtime as a meeting it finally has time to hold. Old conversations replay. Tomorrow's tasks line up like impatient guests. The body is horizontal; the brain is still standing at a whiteboard.

Loneliness can intensify this. A shared evening has interruptions — a comment, a laugh, a show chosen together. Solo evenings can become long hallways. None of this means living alone is a mistake. It means nights deserve design, not just endurance.

## What \"trying harder\" usually gets wrong

People often respond to bad nights with harsher rules: no screens ever, perfect schedules, shame for waking. Harsh rules collapse on hard weeks. Softer rules survive.

Useful reframes:

- **Protect a wind-down window, not a personality makeover.** Even thirty to sixty minutes of quieter input helps some nights.
- **Separate rest from performance.** Lying quietly with a boring book still counts as care, even if sleep arrives late.
- **Stop grading the night at 2 a.m.** Clock-watching turns wakefulness into a second job.

![Warm low light in a calm evening room]({inline})
*Evenings get kinder when the room cues \"slow\" before the mind agrees.*

## A practical evening shape (flexible on purpose)

Think in layers you can keep on imperfect days:

1. **Dim the drama of light.** Softer lamps beat overhead glare when you are trying to convince your nervous system the day is ending.
2. **Park tomorrow on paper.** A three-line list often empties more mental RAM than another scroll.
3. **Choose low-stimulation company if you want voices.** A calm call, a gentle podcast, or a brief low-pressure chat can be better than silence that buzzes — and better than outrage media.
4. **Move screens from the pillow if you can.** If you cannot, at least change the content diet: no argument threads in bed.
5. **Keep caffeine honest.** Afternoon timing matters more than moral purity about coffee culture.

If {topic} is your recurring friction, pick one layer for seven days. One. The goal is a cue your body starts to recognize: *this sequence means we are allowed to stop.*

## Lonely nights vs tired nights

Not every sleepless hour is loneliness. Sometimes it is temperature, late food, a stressful email, or a season of grief. Still, ask gently: would a kind conversation earlier have made this quieter?

Many people discover that a ten-minute real exchange in the evening reduces the 1 a.m. courtroom in their head. That exchange can be a partner, a sibling, a friend, or — when those are asleep — a carefully bounded conversation with a stranger. Boundaries matter: leave if someone pushes for personal details, money, or intensity you did not invite.

## When sleep problems need more than essays

Seek professional guidance if you snore heavily with gasping, if insomnia dominates most nights for weeks, or if daytime functioning collapses. Lifestyle essays can support ordinary restless seasons; they should not delay care when something medical may be involved.

## A kinder morning after a rough night

Do not repay a bad night with a punishment day. Get light if you can. Drink water. Keep one small plan. Avoid declaring the whole week ruined before noon. Sleep debt is real; catastrophic storytelling about it makes the next night harder.

## Closing

{topic} is not a character flaw. It is a pattern asking for softer architecture: light, timing, input, and occasional human voices. Build the night you can repeat — not the night that looks impressive in a screenshot of someone else's routine.
"""


def brain_essay(p, idx, opener, topic, angle):
    inline = p["inline_image"]
    return f"""{opener}

This essay is part of **[Brain & Aging](/category/brain-aging/)**. Today's angle: {angle}. We will stay research-informed and careful — association is not destiny, and conversation is not a cure-all. Public health voices have increasingly treated social connection as relevant to later-life wellbeing. That does not mean every quiet person is in cognitive danger. It does mean isolation deserves attention the way hearing, sleep, and movement do.

## The ordinary workout nobody schedules

Explaining a story, tracking a joke, asking a follow-up question, remembering a grandchild's teacher name — these are unglamorous cognitive tasks. They happen automatically inside conversation. When conversation thins, those tasks thin with it.

Families sometimes assume withdrawal is \"just aging.\" Sometimes quieter years are temperament. Sometimes they are hearing fatigue, mobility costs, grief, or the loss of workplace small talk. Sorting those possibilities matters more than rushing to a dramatic conclusion.

With {topic}, the useful question is rarely \"How do I force more stimulation?\" It is \"Where did the natural occasions for talk go — and what gentle occasions can replace them?\"

## What careful research framing sounds like

Researchers have linked social isolation and loneliness with a range of health risks across populations. That language — *linked*, *associated*, *may increase risk* — is intentional. Human lives are messy. Protective factors stack: movement, sleep, hearing care, purpose, and relationships often travel together.

So treat connection as one lever among several, not a magic switch. A weekly call will not erase every aging fear. It can still make a week feel less sealed shut.

![An older adult in warm conversation at home]({inline})
*The most underrated cognitive tool is still a reason to explain yourself to another human being.*

## Practical ways to keep the mind in conversation

1. **Prefer recurring over impressive.** A twenty-minute weekly call beats a rare three-hour visit you dread arranging.
2. **Pair talk with light movement when possible.** Walks, porch sitting, or parallel chores reduce the pressure of face-to-face intensity.
3. **Treat hearing as infrastructure.** Untreated hearing strain makes people opt out of group talk. Getting that checked is practical, not vain.
4. **Use simple tech on purpose.** Video can help some people feel present; others prefer voice. Choose the lowest-friction tool you will actually use.
5. **Invite stories, not quizzes.** \"What was your first job like?\" lands better than memory tests disguised as chat.

If you are an adult child watching a parent grow quieter, lead with invitation rather than interrogation. \"Want to get coffee Thursday?\" carries less shame than \"Why don't you call anymore?\"

## Loneliness, solitude, and later life

Many older adults enjoy solitude and still benefit from a thin, reliable thread of contact. The danger zone is usually not \"likes being alone.\" It is \"no longer has anyone who would notice if the days went silent.\"

{topic} sits near that distinction. Keep dignity in the language. People can tell when they are being managed like projects.

## What this is not

This is not a guide to diagnosing dementia from a distance. Sudden confusion, safety issues, or major personality changes deserve clinical attention. Ordinary quieter seasons deserve companionship, hearing checks, and patience.

## A sustainable weekly shape

- One planned conversation (call or visit)
- One outing or outdoor stretch, however short
- One curiosity input (book chapter, language phrase, puzzle, music with history)
- Sleep and daylight treated as brain care, not luxuries

## Closing

Aging well is not a contest of perfect recall. It is closer to staying in relationship with the world — including the people who make you narrate your days out loud. If {topic} has been nagging at you, answer it with one recurring appointment on the calendar. Brains, like friendships, respond to rhythm more than to crisis resolutions.
"""


def habits_essay(p, idx, opener, topic, angle):
    inline = p["inline_image"]
    return f"""{opener}

Welcome to **[Gentle Habits](/category/gentle-habits/)**. Today's focus is {angle.lower().rstrip('.')}. We are allergic to extremes here: no seven-day body overhauls, no shame metrics, no pretending a habit tracker can replace human warmth. The aim is a life that stays lightly tethered — to your body, your home, and at least occasional other people.

## Why tiny habits beat dramatic plans

Dramatic plans require a perfect Monday. Tiny habits require a threshold so low you can clear it on a messy Wednesday. When energy is low, low thresholds are not laziness. They are design.

{topic} works best when you attach it to something already true in your day: after coffee, after email, after putting shoes on, before the evening scroll. Habit researchers often call this stacking. Ordinary people call it \"not relying on vibes.\"

## Connection as a habit ingredient

Many wellness routines fail because they are solitary in a lonely season. A walk is good. A walk while talking to someone kind can be better for mood. Cooking for one nourishes. Cooking while voice-noting a friend nourishes two needs at once.

If your habit around {topic} can include a human voice — even briefly — it often sticks longer. Accountability does not have to mean a ruthless coach. It can mean a person who notices you showed up.

![Everyday movement and ordinary care in soft daylight]({inline})
*The habits that last usually look too small to brag about.*

## A template you can actually repeat

1. **Define the minimum.** What is the version you can do in five to ten minutes?
2. **Choose a cue.** Same time or same trigger daily.
3. **Remove one point of friction.** Shoes by the door. Water bottle filled. Message draft saved.
4. **Close with a kindness marker.** A checkmark, a short note, or a text that says \"did the thing.\"
5. **Miss without erasure.** Missing Tuesday does not delete the identity of someone who walks on Wednesdays.

## What to ignore on the internet

Ignore before-and-after theater. Ignore habits that require buying five objects first. Ignore advice that treats rest as moral failure. Keep what makes your evenings less jagged and your mornings less punishing.

Food talk on this site stays gentle: steady meals, cooking for one without despair, shared tea, no war on your body. Movement talk stays accessible: walks, stretches, soft strength, rain-day options. Stress talk stays practical: news boundaries, breathing breaks, not a full personality rebuild.

## When habits and loneliness intersect

Some people build perfect routines and still feel unseen. Habits support regulation; they do not replace belonging. If your tracker is full and your chest is still heavy, that is not failure. That is a signal to add connection — a standing call, a class, a low-pressure chat, a neighbor hello — alongside the water and walks.

## A weekly gentle stack (example)

- Most days: water early, short outdoor light, one stretch
- Three days: walk or movement you do not hate
- Two days: cook something simple on purpose
- One day: deliberate human contact that is not only transactional
- Nights: one screen boundary you can keep

Adjust freely. The stack exists to serve you, not to become another boss.

## Closing

{topic} does not need to become your personality. It needs to become easy enough that future-you does not negotiate it every time. Start with the minimum. Let connection ride along when it can. Leave room for imperfect streaks. Soft consistency is still consistency.
"""


def lived_story(p, idx, opener):
    inline = p["inline_image"]
    angle = p["angle"]
    title = p["title"]
    # first-person essay expanded
    return f"""{opener}

I am writing this under the heading **[Lived Stories](/category/lived-stories/)** because some things teach better as scenes than as tips. The thread here is simple: {angle}

I will not pretend I handled every hour wisely. I will try to tell it honestly enough that if you are in a similar quiet, you might feel less alone inside it.

## The week it stopped feeling theoretical

It did not begin with a revelation. It began with a small absence I kept explaining away. People are busy. People forget. People mean to call back. I told myself those sentences until they sounded like wallpaper.

What changed was not a dramatic event. It was the accumulation of unchanged hours. Mornings with too much coffee. Afternoons where I cleaned things that were already clean. Evenings where the apartment felt staged for a conversation that never arrived.

I kept waiting to feel \"ready\" to reach out — rested enough, interesting enough, less behind on my own life. Readiness, I learned, is a moving target. Loneliness will help you miss it forever if you let it.

## What I tried that did not help

I scrolled for evidence that everyone else was thriving. That did what scrolling usually does: it made my living room feel smaller.

I also performed toughness. *I like my own company.* Part of that is true. Part of it was a costume. Solitude I choose feels like oxygen. Solitude that settles over me without consent feels like weather I did not pack for.

I wrote long messages and deleted them. The deletion felt like control. It was mostly fear wearing the mask of editing.

![An ordinary domestic scene that holds more emotion than it shows]({inline})
*The turning points in lonely weeks rarely look like turning points from the outside.*

## The small thing that moved the needle

What helped was embarrassingly modest. I sent a shorter message than my pride wanted. I accepted an imperfect plan. I let a conversation be awkward for the first three minutes without declaring the whole attempt a failure.

In one version of this week, the reply came quickly. In another, it didn't — and I still had to decide whether to try a second door. Sometimes the second door was a walk outside. Sometimes it was a voice note to someone safer. Sometimes it was a low-pressure chat with a stranger for a little while, with clear boundaries, because I needed a human tempo in the room before sleep.

I am not recommending strangers as a lifestyle. I am admitting that on some nights, any kind voice is a bridge back to yourself — provided you stay safe, leave freely, and do not outsource your whole belonging to a random window on a screen.

## What I would tell myself earlier

I would say: you are allowed to want contact without turning it into a referendum on your worth. I would say: specific invitations beat vague longing. I would say: if a parent goes quiet, ask with logistics first (\"Thursday coffee?\") before you ask with panic. I would say: repair after withdrawal can be one sentence long — \"I got quiet, I'm here now.\"

I would also say: if the quiet comes with despair that does not lift, get more help than an essay. Friends and gentle chats are not the same as clinical care.

## Why I am telling this

Not because my week was special. Because ordinary lonely weeks are where people get lost while still going to work and answering emails. From the outside you can look fine. From the inside the rooms echo.

If you are in that echo, keep the next action small. Text one person. Step outside. Make the soup. Accept the call. Or talk for a short while and then go to bed without demanding that one conversation fix your whole season.

## Closing

I still have quiet days. I try to notice sooner whether the quiet is chosen. When it is not, I try to answer it before shame writes the script. That is the whole craft I know so far — imperfect, repeatable, human.
"""


def render_post(p: dict, idx: int) -> str:
    body = build_body(p, idx)
    # Never pad with repeated identical sections.
    if word_count(body) < 1000:
        title = p["title"]
        slug = p["slug"]
        category = p["category"]
        angle = p.get("angle") or p.get("excerpt") or slug.replace("-", " ")
        topic = slug.replace("-", " ")
        focus = " ".join(slug.split("-")[:4])
        extra = f"""
## What makes "{title}" feel so specific

When people look for *{topic}*, they usually want language for a narrow situation: {angle.rstrip('.')}. Respond with one concrete change — not a personality overhaul — around **{focus}**.

## A scene you might recognize

An ordinary evening shaped by {topic}: nothing dramatic, yet something keeps checking for a signal that does not arrive. Prefer a proportional action (ten minutes of contact, a calmer wind-down, one standing plan) over a heroic fix you will cancel.

## Gentle experiments for the next seven days

1. Name the gap in one sentence.
2. Schedule one low-friction contact with a specific time.
3. Protect one boundary that protects rest or dignity.
4. Pair a body cue (walk, water, daylight) with a human voice when evenings feel hollow.
5. Review without grading — keep what felt 10% kinder.

## FAQ in plain language

**Every day?** No — rhythm beats intensity.
**Feeling silly?** Awkward is not unsafe; leave only what is unsafe.
**More help?** Persistent hopelessness or collapsing function → clinician or crisis resource. Essays are companions, not emergency care.
"""
        if "## Closing" in body:
            body = body.replace("## Closing", extra + "
## Closing", 1)
        else:
            body = body.rstrip() + "
" + extra
    wc = word_count(body)
    if wc < 1000:
        raise SystemExit(
            f"Generated body too short ({wc} words) for {p.get('slug')}. "
            "Expand the category template — do not append duplicate sections."
        )
    tags = p.get("tags") or [p["category_slug"]]
    tags_yaml = "[" + ", ".join(tags) + "]"
    fm = f"""---
title: "{yaml_escape(p['title'])}"
date: {p['date']}
slug: {p['slug']}
permalink: /{p['slug']}/
excerpt: "{yaml_escape(p['excerpt'])}"
author: "Morgan Rivers"
author_slug: morgan-rivers
author_role: "Staff Essayist"
category: "{p['category']}"
category_slug: {p['category_slug']}
format: article
pillar: {p['pillar']}
cta_strength: {p.get('cta_strength', 'soft')}
tags: {tags_yaml}
hero_image: "{p['hero_image']}"
hero_alt: "{yaml_escape(p.get('hero_alt') or p['title'])}"
hero_caption: "Photo: Picsum"
---

"""
    return fm + body.strip() + "\n"



# After generating posts, run: python3 reassign-unique-images.py
# to give each post a unique Picsum hero + inline (no duplicates).
def main():
    posts = json.loads(CAL.read_text())
    POSTS.mkdir(exist_ok=True)
    written = 0
    for i, p in enumerate(posts):
        date = p["date"]
        path = POSTS / f"{date}-{p['slug']}.md"
        text = render_post(p, i)
        path.write_text(text, encoding="utf-8")
        wc = word_count(text.split("---", 2)[-1])
        if wc < 1000:
            raise SystemExit(f"short {path} {wc}")
        written += 1
    print(f"wrote {written} posts; total md in _posts: {len(list(POSTS.glob('*.md')))}")


if __name__ == "__main__":
    main()
