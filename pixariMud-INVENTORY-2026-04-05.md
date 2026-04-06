# pixariMud - Inventory Report (2026-04-05)

## Summary

pixariMud is a narrative-driven MUD (Multi-User Dungeon) game built on the Evennia Python/Django framework. The game casts players as incomplete robots awakening in the underdark of a dystopian city — with only one arm, no legs, and no memory. The core gameplay loop involves scavenging robot parts to assemble a functional body, navigating a contamination ("The Substance") mechanic, aligning with or against three factions (Executors, Cogborn, Neutrals), and climbing through eight underground levels to reach the surface. The project features a rich automated testing framework, demo scripts, NPC AI behaviors, and detailed documentation for AI-assisted development.

## Technologies & Libraries

- **Language**: Python 3
- **MUD Framework**: Evennia (Python/Django-based multiplayer game framework)
- **Database**: SQLite (via Django ORM, managed by Evennia)
- **Protocol**: Telnet (port 4000), HTTP web interface (port 4005)
- **Testing**: Custom AI-driven test framework using `telnetlib` for automated gameplay scenarios
- **Virtual Environment**: `venv`
- **Dependencies**: `requirements.txt` (Evennia and its dependencies)

## Timeline of Work

- **Project started**: 2025-03-19 (Create README.md)
- **Initial Evennia setup**: 2025-03-22 (basic templates and setup instructions)
- **Combat and XP mechanics**: 2025-06-02 (hitting, death, XP)
- **Keycard security system**: 2025-06-13 (vault doors, multi-level access)
- **Robot awakening narrative system**: 2025-06-14 (full narrative, NPC factions, substance mechanics, world builder)
- **Most recent commit**: 2025-08-04 ("draft work of novelized gameplay")
- **Total commits**: 6 (all in 2025)
- **Current branch**: `jpm_environment-setup-1`

## Current State

- **Runnable**: Yes — Evennia setup instructions are complete and a `venv/` directory exists, indicating local setup has been done
- **Uncommitted changes**: One untracked file — `pixarimud/TICKER_HANDLER_FIX.md` — suggesting an active bug investigation or fix was in progress when work stopped
- **Last thing worked on**: "Draft work of novelized gameplay" (2025-08-04) — suggesting an attempt to add narrative writing/flavor text to gameplay events, on a branch still not merged to main
- **Branch status**: Working on `jpm_environment-setup-1`, which is up to date with origin but diverges from any main/master branch integration

## Successes

- Full Evennia project structure bootstrapped and functional
- Comprehensive character system: health, XP, leveling, gold, death/respawn
- Combat system with multiple object types (CombatDummy, WornOutDummy with respawn timer, BottomlessPit)
- Shop and trading system with EvMenu interface, merchant NPCs, consumables, weapons, armor
- NPC AI behavior framework: ScannerBot, WhisperBot, FactionGuard, MerchantNPC with memory and reaction systems
- Keycard security system with four access tiers and specific-ID locking
- Robot body assembly: modular parts, slot system, movement restrictions without legs
- "The Substance" contamination system with faction-driven mechanics
- AI-driven automated test framework for running gameplay scenarios headlessly
- Detailed CLAUDE.md and CLAUDE_robot_docs.md for AI-assisted development
- 6 commits all representing meaningful feature work, not just scaffolding

## Open Items / Failures

- `TICKER_HANDLER_FIX.md` indicates a known issue with Evennia's ticker handler that was being investigated
- Only 6 commits total — the project's depth (as documented in CLAUDE.md) appears to outpace the commit history, suggesting much work was done in large uncommitted sessions
- The most recent commit is "draft work" — narrative layer is incomplete
- No unit tests beyond the demo/scenario scripts; Evennia's test runner is not wired up
- The branch `jpm_environment-setup-1` name suggests environment setup work was never finished or merged
- Multi-level world (8 underground levels) is designed but the extent of actual room/exit creation is unclear from the commit messages

## Long-term Vision

The project envisions a fully playable, community-ready MUD with a strong narrative identity: robots waking up, not knowing who they are, in a hostile underground world split by faction conflict. The themes of identity, evolution, and survival in a post-human world are explicitly called out in the README. The long-term goal is a live, multi-player game server with interconnected community infrastructure (see the companion PixariMUDdocumentation project). The existence of an AI testing framework and detailed AI-guidance documents suggests the developer intended to use LLM assistance aggressively for continued development.

## Portfolio Fit

This project demonstrates proficiency with Python game development, Django/ORM patterns (via Evennia), complex object-oriented game systems design, and the ability to implement sophisticated AI NPC behaviors. The automated telnet-based test framework is an unusual and impressive engineering choice. Combined with the companion documentation repository and organized GitHub presence, this shows the developer can manage an open-source community project with proper governance, contributor documentation, and outreach (Reddit post for community building). It is the most "creative" project in the portfolio and demonstrates breadth beyond web development.
