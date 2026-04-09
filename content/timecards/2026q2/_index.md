+++
date = '2026-04-08T16:36:24-07:00'
title = '2026 Q2 Timecards'
+++

---

## Tuesday 2026/4/7

* 3.5 hours today, 160.75 hours this track year.

Rust removal, signal board replacement, fire extinguisher check.

#### 2.45PM - 6:15PM (3.5 hours)

Came back to finish the job on the south side tool car door. Now it is wholly
shiny.

![Tool car south door all shiny](./20260407_tool_car_door_south_fully_shiny.jpg)

There are still a few spots around fasteners, and I could only get one edge
out of four, but I got the most exposed surfaces so while not perfect it'll go
a long way.

After that was complete I proceeded to execute step 3 of detector block
musical chair and replaced flaky panel G dual block detector board with a
working unit freed up from panel K consolidation.

After that was done I walked around to visually inspect fire extinguishers to
verify their gauges still show needle in the green zone. Helping in this task
is a location map I created on top of a screen shot of LALS layout from
[https://openrailwaymap.app/](https://openrailwaymap.app/#view=17.19/34.155202/-118.303838)

![LALS fire extinguisher locations](./lals_extinguishers.jpg)

Everything looks good though I couldn't access three units: #34 in the ticket
booth, #35 in the caretaker caboose, and #37 in the meeting car. I'll ask about
them later.

---

## Monday 2026/4/6

* 3 hours today, 157.25 hours this track year.

#### 3:15PM - 4:45PM (1.5 hours)
#### 5:30PM - 7:00PM (1.5 hours)

On [March 17th](http://localhost:1313/lals/timecards/2026/#tuesday-2026317) I
took all the loose brown rust off the already mounted (south side) tool car
door. Now I'm back to work on the tougher black layer underneath. I got about
60% of the way down before I had to put the project on hold for board meeting.

![Tool car south door 2/3 shiny](./20260406_tool_car_door_south_two_thirds_shiny.jpg)

Interleaved with this work was a quick experiment trying to buff out the paint
on the meeting car to see if it's a viable alternative to repainting. It helps
but the final decision was to proceed with repaint plan.

---

## Sunday 2026/4/5

* 8 hours today, 154.25 hours this track year.

Sunday public train crew.

#### 8:00AM - 10:45AM (2.75 hours)

Engineer training on UP1989. Includes performing air line and brake check.
Staged it properly in station with a full tank of gas for a certified engineer
to do public runs with it for the day.

#### 10:45AM - 3:15PM (4.5 hours)

Conductor for CN2002 pulling public train rides.

#### 4:15PM - 5:00PM (0.75 hours)

After the public rides wrapped up there was an hour of socializing. After that
we put CN2002 away. This was the first time putting it on its storage track so
there were a few wrong turns. Next time it shouldn't take 45 minutes.

---

## Saturday 2026/4/4

* 1.75 hours today, 146.25 hours this track year.

Some club work but mostly focused on CN2002.

#### 10:30AM - 11:30AM (1 hour)

Execute step 2 of detector block musical chair plan. Move wires from existing
dual-block detector board...

![Panel K detectors before consolidation](./20260404_panel_k_detector_consolidation_before.jpg)

... and move them into the quad-block detector board as well as moving the
board up one slot.

![Panel K detectors after consolidation](./20260404_panel_k_detector_consolidation_after.jpg)

#### 1:00PM - 1:45PM (0.75 hours)

Merchant was here working on the new tool car door that I had partially de-rusted.
Moving it for work meant some previously-inaccessible portions are now
accessible. While Merchant enjoyed a late lunch I went in with my tools to remove
more rust.

#### Other activity (no logged hours)

Potential new club member Stark was on site to look around and meet people.
I will be one of his membership sponsors.

Help Alexander get CN2002 ready for inspection so it can be certified to pull
public ride trains tomorrow.

---

## Thursday 2026/4/2

* 6.25 hours today, 144.5 hours this track year.

Mid-week signals work

#### 8:00AM - 12:45PM (4.75 hours)

Started the day intending to fix false reds that came up during this past
Sunday public run and, annoyingly, they were all clear in the morning.
Intermittent issues, ugh!

![Panel G and toolbox](./20260402_panel_g_and_toolbox.jpg)

Fortunately the panel G false red came back later in the day so I could probe
it to find the track voltage within range so the fault is not a bad bond wire
or track resistor. I probed voltage from detector board input ground to the
track wire and... the fault LED cleared up! That's new.

Several minutes later, the fault returned and I could clear it the same way.
(Measure voltage from board input ground to track output.) It came back within
a minute, and I cleared it again, but then it didn't come back. Doesn't matter,
this board is now untrustworthy and on the replacement queue.

Panel K false red was tracked to a detector board as well. The failure mode on
this one is: we can trigger a false detection just by lightly touching the
circuit board. Behavior implies a loose solder joint somewhere but there were
no obvious candidates.

Plan:
1. Replace touch-sensitive panel K dual block detector board with newer quad
block detector board. This uses half the new board.
2. Move wires from adjacent dual block detector board to the new quad block
board. This frees up a currently-working dual block detector board.
3. Replace the faulty panel G dual block board with one freed up from panel K
in step 2.

Step #1 was done today, I'll come back for #2 and #3 later because we needed
the full team on installing a network timer node in panel M. This started with
cutting the track to install a timer-specific detector block, and we have to
return the rails to operating condition before we break for lunch. For one
thing, our work train is stranded until the track is back in! It is past the
cut point and there's a tree trimmer crew onsite today and they're blocking the
track ahead with cut branches.

Once the track was back and the wiring installed, our work train had the honor
of being the inaugural train to trigger the new timer as it backed over the new
detector block. That was a very satisfying relay **click**.

![Panel M with new timer](./20260402_panel_m_new_timer.jpg)

#### 1:30PM - 3:00PM (1.5 hours)

After lunch the team reviewed plans on how the track blocks will be rearranged
to support the new siding. Most of this will be handled in panel M, but there
will need to be a few interface points to adjacent panels I and K. This is
where we needed the vault I cleaned up the other day and I may have to do the
same to the big tangle of wires in panel I.

![Panel I open](./20260402_panel_i_tangle.jpg)
