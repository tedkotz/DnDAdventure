# D & D Adventure
An old text based DnD adventure game originally written in high school for the Ti-85 in the 1990s

This game a simple dungeon crawler based on the AD&D 2nd edition rules.

I originally wrote this for the TI-85 graphing calculator back around probably 1993

In 2023, I found a printed copy of a version I had translated to I think QBASIC.

I ported it to python to give it a try.

Unfortunately any line over 80 characters was cut off the print out.

Also unfortunately the game stored monster data in another file so the only
monster is the default enemy fighter clone of the character.

As it was ported form the TI it was optimized to use short variable names.

It was somewhat structured for a BASIC program, but needed some real refactoring
to strip out all the goto statements.

What I initially committed was a first run though the port. I afforded some
modern conveniences, like using JSON for the save game file format.

Using basic python io I don't have a getkey equivalent so that needs to be solved

### TODO
- [x] Base game play
- [x] Adding Monsters save/load support
- [ ] replace getkey
- [ ] clean up UI
- [ ] Make more table driven so more choices can be made
- [ ] Replace Martial Artist with Monk
- [ ] make pylint like it
- [ ] get OCR copy of the original printout in this repo
- [ ] Add some monsters


