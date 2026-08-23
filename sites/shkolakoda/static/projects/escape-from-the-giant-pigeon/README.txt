ESCAPE FROM THE GIANT PIGEON — PROJECT FILES

Use the starter to build the game yourself, or inspect the finished game when
you need to compare one of its systems with your own.

Files
-----
- escape-from-the-giant-pigeon-starter.sb3: setup, media, variables, positions,
  and short in-editor instructions; students still build the game systems.
- escape-from-the-giant-pigeon-finished.sb3: completed playable game.
- escape-from-the-giant-pigeon-assets.zip: editable art and sound pack.
- assets/: SVG artwork and WAV sounds used by the Scratch files.
- project-sketch.svg: map of the game's movement, collision, and state rules.

Sprite and costume mapping
--------------------------
Player: player.svg (normal), player-caught.svg (caught); centre 35, 45.
Giant Pigeon: giant-pigeon.svg (wings up), giant-pigeon-wings-down.svg
(wings down); centre 75, 55.
Safe Zone: safe-zone.svg (inactive), safe-zone-active.svg (active); centre 45,
52.5.
Stage: stage-backdrop.svg (Pigeon Chase Map); centre 240, 180.

Sound mapping
-------------
Stage: start.wav. Player: caught.wav. Safe Zone: safe.wav.

Students may redraw, repaint, rename, or replace any artwork. If a sprite or
costume name changes, update the matching Scratch dropdowns too. Keep the
suggested costume centres when swapping artwork of the same size, then test
collision again.

Useful first tests
------------------
- Start three times and check that every run begins in the same state.
- Reach the Safe Zone and confirm that the game ends once.
- Let the pigeon catch the Player beside the Safe Zone and check which ending wins.
- Press R after both endings and look for any position, costume, message, or value
  that failed to reset.
