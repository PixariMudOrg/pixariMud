# pixariMud Status — 2026-04-10

Branch: `jpm_environment-setup-1` (2 commits ahead of origin before this session)

---

## What Works (Code Complete)

### Character System
- Robot characters with chassis integrity, energy, XP, level, and gold
- `gain_experience()` / `level_up()` with per-level stat scaling
- `take_damage()` / `heal()` / `die()` with reconstruction chamber respawn
- `set_respawn_location()` / `setrespawn` command
- `ensure_stats_initialized()` for backward compat on pre-existing characters

### Combat Objects
- **CombatDummy**: Indestructible, awards 1 XP/hit, tracks total hits
- **WornOutDummy**: 100 HP, awards 1 XP/hit, drops 10 gold on destruction, respawns after 60 seconds via TICKER_HANDLER
- **BottomlessPit**: Instant-kill jump target, triggers character die/respawn

### Robot Body Assembly
- Modular part slots: head, torso, left_arm, right_arm, left_leg, right_leg
- Parts: `RobotArm`, `RobotLeg`, `RobotHead`, `RobotTorso` with quality tiers (damaged/standard/enhanced/pristine)
- Quality multipliers affect speed, strength, defense, energy_efficiency
- Movement restrictions: no legs = crawl-only; one leg = limp with cooldown
- `CmdAttach`, `CmdDetach`, `CmdParts`, `CmdCrawl`, `CmdDiagnostics` commands

### NPC System
- Base NPC class with memory, mood, faction tracking
- `ScannerBot`: Scans arrivals, escalates threat level on suspicious speech
- `WhisperBot`: Trust-based secret-sharing, recoils from loud speech
- `FactionGuard`: Checks player faction on arrival, warns/attacks enemies
- `MerchantNPC`: Keyword-driven trade, personalizes for repeat visitors
- Room hooks (`at_object_receive`/`at_object_leave`) notify NPCs of movement

### Shop & Trading System
- `NPCMerchant` with EvMenu shop interface
- Sells: HealthPotion, IronSword, SteelSword, LeatherArmor, ChainMail, LuckyCharm, TeleportScroll
- Merchants buy items at 50% value; `gold_value` attribute controls eligibility
- `CmdUse` / `CmdGold` / `CmdShop` commands

### Security System
- `Keycard`: Four access levels (standard < security < admin < master), optional specific ID
- `VaultDoor` exits: Check access level and/or specific keycard ID
- `holds_keycard()` custom lock function in `server/conf/lockfuncs.py`

### Faction System
- Three factions: Executors, Cogborn, Neutrals (designed in `factions.py`)
- `CmdSetFaction` for testing faction membership
- Faction-aware NPC reactions via `FactionGuard`

### Substance Contamination
- `substance_level` attribute on characters
- Contamination visible in `stats` and diagnostic displays
- Integration hooks in place (full mechanics in `substance_system.py`)

### Infrastructure
- AI-driven test framework (`tools/test_framework.py`): Telnet-based scenario runner
- Demo scripts (`tools/demo_scripts.py`): High-level automated gameplay demos
- Prototypes (`world/prototypes.py`): `@spawn`-able templates for all objects/NPCs
- Batch setup files: `demo_setup.ev`, `shop_demo_setup.ev`, `npc_demo_setup.ev`, `security_demo.ev`

---

## What Is Broken or Unverified

### TICKER_HANDLER — Fix Applied, Not Live-Tested
**Issue**: `WornOutDummy.respawn()` was receiving an unexpected `location` kwarg from TICKER_HANDLER because kwargs were passed incorrectly in `die()`.

**Fix applied** (commit `d9b4623`):
- `die()` stores respawn target in `self.db.pending_respawn_location` before scheduling the ticker
- `respawn()` signature changed to `def respawn(self):` — no args
- TICKER_HANDLER called with no extra kwargs

**Status**: Code fix is in place and matches the Evennia TICKER_HANDLER calling convention (verified by reading `tickerhandler.py` source). The ticker calls `getattr(obj, "respawn")()` with no args. **Not tested on a live server yet.**

**Test procedure** (from `pixarimud/TICKER_HANDLER_FIX.md`):
```
evennia reload
@create/drop Test Dummy:typeclasses.objects.WornOutDummy
@py self.location.contents[-1].db.respawn_timer = 5
@py self.location.contents[-1].db.health = 5
hit dummy  (×5)
wait 5 seconds → expect respawn message
```

### Character Creation: RobotArm (Fixed This Session)
**Issue**: `Character.at_object_creation()` was creating the starting arm via `RobotArm(key=...).save()` — direct instantiation bypasses Evennia's `at_object_creation()` hook, leaving the arm without `part_type`, `strength_modifier`, `speed_modifier`, `defense_modifier`, and `energy_efficiency`. This causes `attach_part()` to reject it (`"is not a robot part"`) and `recalculate_stats()` to compute zeroes.

**Fix applied this session**: Changed to `create_object(RobotArm, key="Right Robot Arm")`.

**Impact**: Affects **new character creation only**. Existing characters that were created under the broken code may have an arm attached with no stats. Use `@examine <char>` to inspect.

### `recalculate_stats()` — Duplicate Line
`robots.py:217` has `self.db.movement_mode = "limp"` set twice in the one-leg branch (lines 216–217). Cosmetic bug, no functional impact.

### Multi-Level World — Designed, Not Built
The design calls for 8 underground levels with interconnected rooms and progression. No rooms have been batch-created beyond the demo batch files. The batch files create demo rooms for each system but not the full world map.

### Narrative Layer — Draft State
`b5c2c5a` ("draft work of novelized gameplay") added flavor text to gameplay events. This work is incomplete; no specific file was identified as its home. Narrative hooks exist in the codebase but are inconsistently applied.

### Crawl Command Exit Lookup
`CmdCrawl` calls `exit_obj.reverse_exit()` — this method does not exist on Evennia's `DefaultExit`. This will raise `AttributeError` when a legless character crawls through an exit. Fix: replace with a search of the destination room's exits filtered by destination == current room.

### No Evennia Unit Tests
The project uses `tools/test_framework.py` (telnet-based integration tests) but has no Evennia `EvenniaTest` unit tests. Django/Evennia's test runner (`evennia test`) is not wired up. This makes refactoring riskier.

---

## Next Actions (Priority Order)

1. **Live-test the TICKER_HANDLER fix** — follow the procedure above; confirm WornOutDummy respawns cleanly. If it still fails, migrate to `evennia.utils.delay()` which is simpler for one-shot delays and doesn't have the kwargs-forwarding complexity.

2. **Fix CmdCrawl exit reverse lookup** — replace `exit_obj.reverse_exit()` with `destination.exits` filter or remove the arrival announcement gracefully.

3. **Verify existing characters** — log in as any pre-existing character, run `diagnostics`, and confirm the starting arm has stats. If not, use `@py` to manually fix or delete and recreate affected characters.

4. **Begin world building** — create the first 2–3 underground levels using batch commands. Start with the Scrap Heap (Level 1) and establish the narrative entry point. Prototypes for scrap rooms exist in `scrap_rooms.py`.

5. **Wire up narrative events** — identify where flavor text hooks should fire (room entry, first attachment of a part, first combat, faction join) and apply consistently across typeclasses.

6. **Add Evennia unit tests** — at minimum, test `Character.at_object_creation()`, `WornOutDummy.die()`/`respawn()`, and `attach_part()`.
