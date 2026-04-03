---
layout: post
title: "Side Project - Building the Goblin Horde Checklist"
date: 2026-04-03
---

# Side Project - Building the Goblin Horde Checklist

Apr 03, 2026

This one started as a Magic: The Gathering problem and ended up being my first real deployed web app.

I play Commander and I've been trying to track every Magic card that has a goblin connection - whether that's the creature type, the name, the rules text, or the art. There's no clean way to do this inside Scryfall or ManaBox, so I decided to build something.

The goal was simple: a checklist of every goblin-adjacent card in Magic history that I could check off as I acquire them.

---

## The Query

Scryfall has a powerful search syntax. I put together a query that covers all four ways a card can be "goblin-related":

```
game:paper (art:goblin or t:goblin or goblin or o:goblin)
```

This hits cards with the Goblin type, cards with "goblin" in the name, cards that mention goblin in the rules text, and cards where Scryfall's art tagging identifies a goblin in the illustration.

The problem was I had no way to turn those search results into a persistent, interactive checklist. That's where the build started.

---

## First Attempt - Claude Artifact

My first instinct was to build it as an interactive artifact in Claude. The idea was to call the Scryfall API directly from the browser and render a checklist in real time.

That failed immediately. Scryfall blocks direct browser requests from embedded iframes due to CORS restrictions. The artifact environment couldn't reach the API at all.

---

## Second Attempt - Local HTML File

The next approach was a standalone HTML file that could be opened directly in a browser. Local files bypass CORS because they aren't making cross-origin requests from a remote domain.

This worked. The file loaded, called Scryfall, paginated through the full result set with a small delay between requests to be polite to their API, and rendered the full list with checkboxes. State was saved to localStorage so checks persisted between sessions.

I also added ManaBox CSV import. ManaBox exports include a Scryfall ID column, which meant I could match imported cards directly against the checklist and auto-check anything I already owned. The fallback for CSVs without Scryfall IDs was to match on card name plus set code plus collector number.

This was working well on desktop but useless on mobile, which was the whole point.

---

## The Real Problem - Cross-Device Sync

localStorage is per-browser, per-device. There's no way to sync it. Checking something off at an LGS on my phone would never show up at home on my desktop.

The solution was Firebase - specifically Firestore for the database and Firebase Auth for Google sign-in.

The architecture ended up being:

- Scryfall API fetches the full card list on load, paginated
- Firebase Auth handles Google sign-in, one click
- Firestore stores the checked state, ManaBox import data, and UI state (collapsed groups, etc.) keyed to the user's UID
- An `onSnapshot` listener keeps everything in sync in real time across devices

The Firestore security rules lock each document to its owner:

```
match /goblin-checklist/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

---

## Deployment Friction

Getting it live took a few tries.

The first attempt was opening the HTML file locally. Firebase's Google sign-in popup is blocked from `file://` URLs, so that failed.

Next I tried Netlify Drop. The file uploaded but returned a 404 because it wasn't named `index.html`. Renamed it, re-uploaded, got a working URL. Added that URL to Firebase's authorized domains and sign-in worked.

Netlify Drop sites expire after a week without an account, so I moved it to GitHub Pages instead. Created a new repo, ran into a conflict trying to initialize it through VS Code after already creating it on GitHub, deleted and restarted, pushed the file, enabled Pages in the repo settings, waited about a minute for the deploy, got a 404 because again the file wasn't named `index.html`, pushed the rename, and then got a Firebase auth error because the GitHub Pages domain wasn't in the authorized domains list yet.

Added `skrunji.github.io` to Firebase authorized domains and it worked.

The app is live at [skrunji.github.io/goblin-horde](https://skrunji.github.io/goblin-horde).

---

## What This Covers

Looking back at the stack:

- **Scryfall REST API** - pagination, query encoding, rate limiting
- **CSV parsing** - RFC 4180 compliant, handles quoted fields, multiple column name conventions
- **Firebase Auth** - Google OAuth, auth state listeners
- **Firestore** - real-time listeners, security rules, document structure
- **GitHub Pages** - static hosting, deploy workflow
- **Vanilla JS** - no frameworks, DOM manipulation, event handling

The thing I kept running into was that each environment had different restrictions. What worked locally didn't work in an iframe. What worked in an iframe didn't work on mobile. What worked on mobile didn't persist across devices. Each constraint forced a more complete solution than the one before it.

---

## Takeaway

The biggest thing this reinforced is that deployment is part of the project. Writing code that works on your machine is step one. Getting it to work reliably for a real user in a real environment is a different problem, and that's where most of the actual learning happened here.

Also I now have a checklist of 1,400+ goblin cards. So there's that.
