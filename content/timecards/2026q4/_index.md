+++
date = '2026-10-04T17:37:23-07:00'
title = '2026 Q4 Timecards'
+++

---

## Sunday 2026/11/15

* 9 hours today, 764 hours this track year.

Disney Sunday public run day.

#### 8:00AM - 5:00PM (9 hours)

Arrived to find signals on but nobody on track. Time for the usual panel-
opening ritual which found panel C NT to be continually resetting. I thought
we cured this by moving damp dirt off the tracks but apparently I thought
wrong.

Signals verification lap found an issue with ESM3 so we cleaned it out and
applied graphite lubricant. Seems OK... for now.

While working on ESM3 we opened up panel E for access to the test button and
saw the NT countdown timer was at 42 minutes. It should be at 120 because
Chessie just rolled over the block. But nothing would reset that timer, not
the track and not the remote control button. Feels like whatever was happening
at P yesterday is happening at E now.

Noticed that whoever put SF163 away forgot to put down the conductor's seat so
the seat back I just replaced is broken again. Grumpy.

Floated around various tasks during run day, including a noon shift at east
gate so Campbell can go sit for a while and get lunch. Plus my November check
of fire extinguishers.

No need to pull Sankey out today because we had real steam locomotives running
on track today. Always a good thing.

---

## Saturday 2026/11/14

* 10 hours today, 755 hours this track year.

Signals work day during official club monthly work day.

#### 8:00AM - 6:00PM (10 hours)

Started the day with my show-and-tell with reed switch sold for home security
system window sensors. Michael thinks it looks promising, let's keep an eye
open for good field trial opportunities.

Work day was greeted by the twitching GSM1, so we took it as an omen to replace
its switch motor board with another. It stopped twitching, but we'll need to
keep an eye on it.

Next stop on the way out is the switch to valley division... it wasn't always
working. Looking in panel I we saw it is an unique motor board with additional
circuitry for the automatic switch to mainline. We have no replacements if it
should go bad, not a great position to be in.

Bagley siding switch moves but does not always indicate correctly. Position
sensing microswitch enclosure is dirty and the switch is rusted out. Maybe we
want that reed switch sooner rather than later.

I got an introduction to the full sized railroad signals in the showcase
garden area. It's weird to see tiny proto boards connected to beefy industrial
equipment. One side is controlled by unplugging from a socket, the other side
has an actual power switch.

Disney crossing bell disassembled, cleaned, and reassembled so now it rings
as intended. Also re-fastened the railroad crossing sign as well.

Signal WB false red quickly traced to a bad track resistor, routine replacement
followed and WB is back again.

RFA/B is also not indicating correctly even after cleaning and adjustment. Not
on mainline (unlike Bagley siding) so a better reed switch field test
candidate.

"Oh let's hook up panel P NT. It should be quick." It was not. There's some
electrical path we couldn't figure out. The NT track blocks aren't really open
circuits when there's no train over it, so the timer board logic is stuck and
never resets the timer. Maybe it'll do so after the timer expires but we can't
renew the timer in this state. Mitigation: since the tracks aren't working
anyway, we leave then disconnected so at least the maintenance bay button can
reset the timer.

Finished the day by putting the flash relay on signal ACB so AC can show red
and blinking-red when the adjacent switch is set to go into the narrow gauge
barn.

I went to LB+LC driver board to check its current draw on yellow-in port. I
thought it was 0.890A which is way too much! Turns out it's just 0.890mA
which is fine and doesn't explain driver board failure.

---

## Tuesday 2026/11/10

* 9.5 hours today, 745 hours this track year.

Signals work day.

#### 8:00AM - 12:30PM (4.5 hours)

Started by replacing the power board in panel B. It's a hairy nest of wires in
there but it seems like we didn't break anything doing it. C was then turned
back on "Auto" mode. Later in the afternoon NT ring shut down and I was able to
verify B and C both turned off as expected. Pushed the button in Sherwood
station (panel E) and they all came on.

Took a look at the loose rail in Phil West track 7. We'll need a few things
from Home Depot before we can tackle this job.

GSM1 is still doing its weird twitch but, since it's switching reliably today,
we'll leave it. We've got enough to do today.

Signal RF was occasionally not showing correctly due to RSM2 position sensing
micro switch not responding to rail switch movement. Opened up the enclosure to
find a big mess as expected. After cleaning it up RF indicated properly, but
RSM2 was not acting right. It's doing the bounce thing it did before. Motor
driver board ref F supposedly have a fix. We'll see.

Made some progress in panel L ESP32 upgrade prep with the new opto isolator
board. We had to sort out two bundles of wires and find an unused one we can
use as reference for panel K signal ground. Then we got three good signals
getting sent across before brain performance went downhill. Lunchtime!

#### 1:30PM - 6:30PM (5 hours)

Stopped by Home Depot on the way home so we could get started on Phil West
track 7 work. The very first Tapcon screw snapped its head so we're not
terribly confident this particular job will hold up. But it's what we have
today so let's see how it holds up. If it does, no need to devise another plan.

Went over to east gate and looked at the full sized crossing. It lights up and
rings bell just fine. The lights don't alternate regularly and we can hear the
clicks hinting at a mechanical switching mechanism. Maybe project for another
day.

After Strawn departed I returned to digging out the western signal bridge by
panel M. I moved two gondola loads worth of dirt today, which is overall number
4 and 5 for this project. I hit concrete on #4, and #5 lets us see the shape of
the concrete base. Probably need at least one or two more before we can shore
up this hillside.

![Signal bridge concrete base](./20261110_signal_bridge_concrete_base.jpg)

Those two gondolas of dirt went into squirrel holes, remainder spread over
downhill side of Akins hoping to replace erosion in that area.

Final lap around the track found LB and LC showing false yellow again. Probed
panel K driver board and saw the same problem as before: KB red out is logical
low but the driver output is logical high. Will ask Brock before moving to yet
another driver board I/O pairing.

---

## Sunday 2026/11/08

* 9.5 hours today, 735.5 hours this track year.

Sunday public run operations.

#### 8:00AM - 5:30PM (9.5 hours)

Morning signals check found no new issues, and thankfully it stayed that way.
Pulled out Sankey so guests can see a steam locomotive. When 10AM rolled
around there were only two trains out so I pulled CN2002 out of the barn for
a third option if needed. It turned out we didn't have enough people to run
three trains anyway so CN2002 sat looking pretty in the station. I ended up
conducting SF657 for several laps. Since we only had two trains we ran well
past 3PM to give rides to everyone who were in the gate by 3PM. And after
they were done... I got to put CN2002, Chessie and Sankey back in their
storage tracks.

![CN2002 refueling for a day's run](./20261108_cn2002_refueling.jpg)

---

## Saturday 2026/11/07

* 3 hours today, 726 hours this track year.

RailGiants event.

#### 8:00AM - 11:00AM (3 hours)

Arrived to set up SF163 to give rides at today's event, then brought out
Chessie to check signals status. Found panel B failed to power up, diagnosed
to power board not closing the AC circuit in response to NT signal nor manual
override switch. Pulled the wires out of terminals and connected them together
with a Wago connector so panel B is on all the time. Since B and C are very
closely linked, went and flipped panel C to be always-on until we can replace
panel B power board.

Found no other signals issues, and we had so many steam locomotives today
giving rides we ended up not needing SF163 at all. This is my ideal scenario:
so many steamers we don't need the electric.

At the end of the event I put SF163 away.

#### Other

Since I had no steamer to give rides and we didn't need the electric, Strawn
and I ended up working on Sankey for the rest of the day. We got the water tank
out of the tender for cleaning. The steam injector outlet is completely
plugged. I thought it was deliberately plugged but others present think it is
hard water buildup. Either way, we had to slice open the silicone seal to get
inside so it can be cleaned. There's a lot of rust in the space between the
tank and the tender, that should be removed and repainted before Sankey is put
back together.

![Sankey water tank lifted and opened](./20261107_sankey_water_tank.jpg)

---

## Tuesday 2026/11/03

* 9 hours today, 723 hours this track year.

Signals work day.

#### 8:00AM - 11:30AM (3.5 hours)

Started the day with installing replacement for HFB lens that has gone missing.

Next is ESM3 which required a cleaning of motor mechanism and replacement of
switch position sensing micro switch. It's a recurring issue that can be traced
to the fact water flows into this area and pools, bringing debris that jams up
mechanical components and corrodes parts that were not designed to handle water
exposure. In the short term we have to keep replacing these bits. In the medium
term better water drainage should help. In the long term I want to replace all
these components with waterproof equivalents.

While verifying ESM3 behavior we opened up panel E and found an ant infestation
requiring some chemical warfare. Harper noticed a large amount were hiding
between the two back-to-back boxes so they got sprayed too.

Then over to panel A for two AC circuit projects with McMurray: one restore
wires knocked loose from a wire nut, and the other retracing power path
connecting panels A+B+C to Inchberg.

Next work item was signal BD whose red has gone dark. Vault immediately
adjacent was cleaned out, and wire traced back to the next vault towards panel
B. There were a set of wire nut connections inside this vault and the red wire
is visibly degraded. At the wire nut, the red wire has disintegrated into
powder. About 6 inches back, the wire was mostly solid but strands are easily
broken. I had to cut about a foot before I got usable wire. These were
reconnected with fresh wire nuts filled with conductive grease to keep out
water, backed up by a wrap of electrical tape.

#### 12:30PM - 6:00PM (5.5 hours)

After lunch break Strawn and I commenced panel R upgrade to latest generation
of block detector and signal head driver boards. In parallel, Harper worked on
position sensing switch wiring to enable signal ACB. I got to move a lot of
wires around, some of which weren't in the best shape so they had to be fixed
before continuing.

![Frayed insulation in panel R wire](./20261103_frayed_wire_insulation.jpg)

This panel also had a bad ant infestation. Between panel E and R we used up
a lot or Raid and breathing the poisonous fumes afterwards probably took some
time off my lifespan.

We got the detector blocks and signal heads working and superficially tested
before Strawn had to leave. After that I continued working to connect
cross-panel communication wiring. These are difficult to test by myself so
they'll get tested later.

But on paper, panel R is back up and running at feature parity with its
pre-upgrade state this morning. The caveat is because RSM2 sensing switch is
not operating reliably, but that's not an upgrade issue. And we are missing
three driver board output wires, which meant they never worked before and thus
the counterpart input wires can wait for another day.

---

## Monday 2026/11/02

* 3 hours today, 714 hours this track year.

SF163 maintenance.

#### 3:00PM - 6:00PM (3 hours)

SF163 maintenance session before monthly board meeting.

* Brought my CRC battery cleaner spray to neutralize bits of battery acid that
has seeped out and corroding its terminals.

Before:

![Battery terminal corrosion](./20261006_battery_terminal_before.jpg)

After:

![Battery terminal corrosion cleaned](./20261103_battery_terminal_after.jpg)

* Topped off battery water level.
* Inspected air compressor filter and it doesn't look too bad.
* No charred wires or melted parts that indicate electrical component failure.
* Axle #3 is still the only dry axle. Axles #1, #2, and #4 continue to show
evidence of small amounts of gearbox lubricant seeping out.
* "Rattling chain" noise reported from yesterday's run pinpointed to the
locomotive brake mechanism, whose parts just dangle when released. The geometry
is such that the noise is only heard loudly when moving in reverse.
* Use damp cloth to wipe off muddy footprints from Sunday's rainy session.
* Conductor's chair mounting bolts tightened and the broken back swapped with
one from a currently offline caboose.

---

## Sunday 2026/11/01

* 9 hours today, 711 hours this track year.

Sunday public run + signals.

#### 8:00AM - 5:00PM (9 hours)

Sunday miscellaneous tasks support crew. Started with signals verification
finding erratic GSM1 and panel M false reds returned. Also restock beverage
refrigerator, emergency power disconnect for ESM2, etc. Rained out for about
30-45 minutes but tracks dried up quickly enough I didn't need to deploy my
sander.

After public run wrapped up I connected the new iteration of detector board
to panel M detector blocks and no joy: it still shows fault.

---

## Tuesday 2026/10/27

* 4 hours today, 702 hours this track year.

Bench car reassembly, track fixes, and signals

#### 8:00AM - 12:00PM (4 hours)

During Fall Meet our guests can help themselves to club owned bench cars to
carry people around. A side effect is our Sunday public run bench car sets get
scrambled up. Harper and I got them all put back together. Guests tend not to
use the air brakes, which meant those lines are usually dangling around and at
risk of damage. Fortunately they look fine, and none of them have disappeared.
The final exam will be Sunday morning when they are pressure tested.

When I arrived the signals were on but there was nobody else. I walked around
and saw NT counts on panel P and C. Panel C seems to be the most problematic
one with constant resetting. Harper decided damp dirt under the track is the
culprit and cleaning them out did stop the counter reset so I guess that's
good? Panel P NT might need the same treatment soon.

Yesterday I noticed the east end of Bowlus had a joiner plate with both bolts
missing from one side, which leaves the track flapping. There was also a dip
that threatened to derail trains going over it. Harper handled majority of
fixing while I was a minor assistant.

After lunch Harper started running a new conduit for narrow gauge barn switch.
I passed on helping and went to fill in a fresh squirrel hole before heading
home to rest.

---

## Monday 2026/10/26

* 3.5 hours today, 698 hours this track year.

Signals and squirrels.

#### 2:30PM - 6:00PM (3.5 hours)

I arrived hoping to perform a test with malfunctioning panel M, swap out its
detector with both older and newer types to see if they share the same issue.
We didn't want to do it during the meet because of risk of breaking something
else, but I arrived to see panel M signals working correctly. Our current
hypothesis says it's the damp soil after rain and if so the ground dried out
enough to make the symptoms disappear. We'll have to continue after the next
rain.

Since I was here anyway I first performed a survey lap to see if there were
any other signals issues. After they were logged, I thought the drying ground
is a good opportunity to move another gondola (or three) of dirt. This time
taking from the buildup near western signal bridge to the west end of O'Brien
Moore bridge.

---

## Sunday 2026/10/25

* 2 hours today, 694.5 hours this track year.

Taking Strawn's entrance gate shift.

#### 7:00AM - 9:00AM (2 hours)

Strawn was not feeling well so I took over his morning shift at the entrance
gate. Getting up early to arrive by 7AM is not something I would have done
by choice! It was also very cold at the booth so I was very eager to go get
hot food and coffee when the shift was over.

---

## Friday 2026/10/23

* 7 hours today, 692.5 hours this track year.

Frantic signals repairs before bulk of Fall Meet guests arrive.

#### 8:00AM - 12:30PM (4.5 hours)

Threat of rain (and a bit of actual rain) kept majority of our Fall Meet guests
away and that is good news for signals: we have some elbow room to make fixes
before everyone shows up.

Also good news: signal head HC started indicating correctly. We'll keep an eye
on it over the weekend and be ready to jump on it as needed.

IC didn't start working better, though, and this is a signal whose malfunction
could lead to head-on collisions so this was definitely the red alert work item
of the day. It wasn't just the micro switch that was bad, some of the wiring
and crimp connectors had to be redone as well for reliable operation.

Also very important was the Minden siding switch HS1, because that is around a
blind corner and steam locomotives do use that location to top off water. We
need the preceding signal HFA/B to warn incoming locomotives with red/yellow
if that switch was thrown.

A quick verification lap confirmed everything looked good beyond panel M. Time
to get some food in the belly then let's jump on that.

#### 1:30PM - 4:00PM (2.5 hours)

Spent the afternoon struggling to understand why panel M block detectors show
fault even though all the track voltages are within proper range. Eventually
pinned blame on an unexpected path for current to flow, aided by the damp soil
after rain. But exactly what power, and going where, remains mysterious.

Like I told people later: we never did figure out what it IS, but we did find
many things it was NOT. And that's still progress.

---

## Thursday 2026/10/22

* 6.5 hours today, 685.5 hours this track year.

Signal head cleaning service + situation survey.

#### 12:30PM - 7:00PM (6.5 hours)

I arrived just after a rainstorm to see what has gone haywire. There were many
small issues but I found two big ones: signal heads HC and IC were not
indicating correctly and these are important switches we need to work for the
upcoming Fall Meet. I had a shop vac and compressed air with me so it was
pretty quick to give those position sensors a quick clenaing. Better, but not
quite good enough. This will need more work.

I had the vacuum and the air compressor because another goal of today's visit
was a cosmetic appearance cleaning pass. First the shop vac for big clumps of
dirt tangled in spider webs, then a damp towel to wipe off bird poop and any
remaining residue, and a stream of compressed air to clean out details.

---

## Sunday 2026/10/18

* 9 hours today, 679 hours this track year.

Disney Sunday

#### 8:00AM - 5:00PM (9 hours)

Started the morning by pulling CN2002 out of the barn for a little bit of
exercise, starting with a trip down to Valley Division to replace a screw on
signal head SA. When replacing it with a side marker LED faceplate, I managed
to lose a faceplate screw. (It was in my small magnetic parts tray and I
unintentionally bumped it on its lip turning it into a catapult.)

No running public with CN2002 today as there were enough trains. We had SF163,
UP1989, SPSF, and Fuad's engine all pulling bench car sets. I also lacked the
Ryobi battery necessary to run the air compressor for air brakes. Which meant
CN2002 will be on show-and-display. To put on a good show and display, I pulled
out my pile of microfiber towels and used the Alexander-designated paint care
product to shine things up.

![CN2002 on display](./20261018_cn2002_on_show.jpg)

Since I had my train cosmetic care kit out, I put away Alexander's CN2002
product and switched over to my own bottles to give SF163 its own glow-up
treatment.

I was the east gate person for about two hours in the afternoon, where I had
the chance to chat with other lovely Carolwood staff at the booth in between
making sure the track is cleared when a train comes through.

Plus random other miscellaneous tasks as part of being the Sunday crew. I was
busy enough I didn't have time to bring out Chessie or Sankey for display.
Silver brought out his Nickel Plate Road locomotive which tempted Murphy to
bring out his NS Dash-9 set but he did not. The biggest novelty show train is
Horgan's steam locomotive pulling his sete of passenger cars. Choo-choo is
always a crowd pleaser.

---

## Saturday 2026/10/17

* 10 hours today, 670 hours this track year.

Signals work day.

#### 8:00AM - 12:30PM (4.5 hours)

Started the day with the most important mainline impact: ESM2 position sensing
switch, which has been working intermittent for several weeks, got replaced.
This should resolve the misleadingly reported "can't select track 1" issue.

After that was done, we went back to paying panel P the attention it has long
been deprived of. Most important for a sense of completeness, Strawn and Harper
found the failed power wire for that seventh dwarf and ran a replacement so it
illuminates along with the rest. Working in parallel, Katz and I installed a
set of side marker LED modules to the maintenance bay dwarf using my 3D-printed
TPU ring. The inner diameter proved to be a tad too large, allowing the LED
modules to pop out. Putting a loop of electrical tape will allow this initial
field test to proceed. Next round will have TPU rings with a smaller inner
diameter.

#### 1:30PM - 7:00PM (5.5 hours)

Once all seven lights were illuminating, we turned our attention back to P NT.
The ancient NT board did not allow adjustment of timeout, so it was swapped out
with a newer board that did. Then, to trigger that timer, we connected the
mainteance bay button as well as the currently working NT track block located
on south track east of the driveway. Finally, the previously-nonworking NT
track block located on the north track west of the driveway got a look see. I
found two breaks in underground wiring that had allowed water to seep in and
corrode the wire to nothing. Cutting them out and splicing the remaining wires
together brought the NT block back.

![Compromised wire insulation](./20261017_broken_p_nt_block_wire_insulation.jpg)

Now trains exiting Phil West yard westbound will be sure to trigger the NT ring.

---

## Friday 2026/10/16

* 2 hours today, 660 hours this track year.

Dwarf signal remains stubborn.

#### 12:30PM - 2:30PM (2 hours)

I stopped in for a quick work session, hoping to bring that final seventh
yard dwarf back online. Replacing bulbs and a socket allowed me to get the
dwarf running on battery power, but it still needs a power feed to actually be
useful.

![Grumpy dwarf on battery power](./20261016_grumpy_dwarf_on_battery.jpg)

---

## Tuesday 2026/10/13

* 10 hours today, 658 hours this track year.

Signals work day.

#### 8:00AM - 12:00PM (4 hours)

Following up yard/Sutchville yard dwarf work, today we brought the associated
motor back online so now it is a motorized switch again. This is expected to be
useful at the upcoming Fall Meet. Remaining yard switches remain manually
operated and no visual indication beyond watching the points. We won't have
time to do anything about that for this Fall Meet. Maybe the next one?

After that was up and running we revisited the crossover switch with my very
temporary zip-ties. Repositioning the microswitch (required drilling several
new holes) brought it back to operating condition without any zip ties at all.

Panel S main control ESP32 was upgraded so it can participate in cross-panel
communications. This required some rewiring work because the new code moved
some wires around for no functional need.

#### 1:00PM - 7:00PM (6 hours)

Panel P has no contact with public route and thus has rarely been considered a
high priority. Today we pay attention! First job is to get it to rejoin the
timer ring. We had to patch a broken connection inside a vault but first we
had to find the buried vault!

Cleaning up the buried vault also allowed us to find wires associated with NT
block that had stopped working. More answers would have to wait for another
work day.

After Strawn departed, Harper and I focused on the Phil West yard ladder
track dwarf signals, the "Seven Dwarves". Many had burnt out light bulbs,
several had damaged microswitches that had to be replaced, and three had bad
power wires. We were able to fix two of the bad power wires, but one dwarf
is still broken. Getting six out of seven dwarves back online is a great start.

![Six out of seven dwarves back online](./20261013_six_out_of_seven_dwarves.jpg)

But that last one taunts me. I took out my frustrations by shoveling some dirt.

![Gondola of dirt](./20261013_gondola_of_dirt.jpg)

---

## Sunday 2026/10/11

* 2 hours today, 648 hours this track year.

Fire extinguisher check, squirrel war continues.

#### 5:00PM - 7:00PM (2 hours)

Public run cancelled so I went to check out the Galpin auto show instead.
Stopped by the club on the way home and performed my monthly fire extinguisher
check. After that, loaded up a gondola with Crystal Springs Drive dirt and
filled some squirrel holes alongside minor signals work.

---

## Saturday 2026/10/10

* 7 hours today, 646 hours this track year.

Signals work day.

#### 8:00AM - 12:00PM (4 hours)

Started by wrapping up a loose end from last time: the yard/Sutchville dwarf
now has a proper dwarf faceplate instead of a full size faceplate with the
bottom chopped by a band saw.

Then we moved to BSM5 which had lost all power, and traced the problem to
wires disintegrated inside a wire nut. Trimming wire to expose fresh conductor
brought the motor back.

While testing that fixed motor we noticed BH showing the intermittent false
red that has been haunting us for a while. This opportunity allowed us to go
chase down the bad bond wire and get it fixed hopefully once and for all.

Onward to panel S where we diagnosed the cross-panel communication issues
and decided S and R need to send reference ground from each other as the design
originally specified and not try to do anything fancy with shared grounds.
That's just not going to fly in the new world of regulated power supplies.

#### 1:00PM - 4:00PM (3 hours)

Panel S received the next iteration of block detector and signal driver boards,
now each with their own ESP32 brain and communicate with the main ESP32 via
serial link. This cuts down on the wiring within the panel and I hope it will
pan out as hoped.

Griped about enclosure for RSM2 and how it defeated several of the points of
putting position sensing microswitch inside an enclosure. Why go through all
this effort just to expose it to the environment?

![RSM2 exposed even while enclosed](./20261010_rsm2_enclosure.jpg)

After Strawn departed I continued working on issues I found. False red on
KD and KEA traced to a bad bond wire that was replaced. Also found a bad
crossover signal head that was not indicating rail switch position reliably.
I could make it a bit better with zip-ties but that's still not a proper fix.

---

## Thursday 2026/10/8

* 9.5 hours today, 639 hours this track year.

Signals work day.

#### 8:00AM - 1:30PM (5.5 hours)

Started the day reviving the dwarf signal indicating yard vs. Sutchville.
How old was the old equipment? We found LEDs instead of incadescent bulbs so
they're not that old... but the LEDs were mounted in wood. Who needs circuit
boards when you have wood?

![Signal head LEDs mounted in wood](./20261008_dwarf_led_wood_circuit_board.jpg)

I didn't have a dwarf faceplate ready but I did have a B signal head with the
big side plates. In order to make things fit I trimmed the bottom part short
with a band saw so that plate will fit in a dwarf position allowing us to
deploy commodity side marker LED modules on this dwarf.

Once that was done we split up. I went up to fix the switch motor controlling
mainline/Akins while the rest worked on panel S NT. Fortunately my part only
needed a little cleaning then I started working on putting a switchmode power
supply in panel S. This took most of the day to figure out.

#### 2:30PM - 6:30PM (4 hours)

After lunch break I had fuel for my brain to wrap up the power supply upgrade.
While I was doing this Strawn went over to panel J to play with the NT block
and we found out the current generation switch motor boards can completely
freak out flipping the motor back and forth in the presence of power issues we
are still struggling to understand. We suspect this episode was triggered by
a regulated power supply interacts with a linear power supply via NT ring.
No good! And this means until we understand what's going on, we shouldn't
bring panel S NT block back online either. Sucks.

After I verified basic panel S functionality after the power supply upgrade,
I pulled out the old giant transformer. Since it was held with nuts on the rear
panel this meant dropping the entier panel to access those nuts. Not pleasant
but not as bad as I thought it might have been.

The problems didn't come up until I looked at cross-panel communication. The
ground reference has changed with the switchmode power supply so I disconnected
wires to panel R until we can understand what's going on.

The day ended with a bit of humor mirroring the morning's wood circuit board:
some old signals components were found buried in the dirt adjacent to the
siding resurrection project.

![Old signals encrusted in dirt](./20261008_ancient_mud_encrusted_siding_signals.jpg)

We're not going to be able to use... whatever this was.

![Old signal component encrusted in mud](./20261008_ancient_mud_encrusted_siding_signals_closeup.jpg)

---

## Monday 2026/10/5

* 3 hours today, 629.5 hours this track year.

SF163 maintenance.

#### 3:30PM - 6:30PM (3 hours)

Arrived in the afternoon to go through my normal routine before the monthly
board meeting: make sure SF163 is in tip top shape. The primary task was to
make sure the battery water is topped up. There was a broken chain on the
riding car lid that I had to repair by removing the broken link and hook up
the next link down.

![SF163 broken chain](./20261005_sf163_broken_lid_chain.jpg)

The positive (front) terminal on the rearmost battery is concerning. I thought
I cleaned off all the seeped-out acid but the terminal has continued to
corrode. I need to dig up my battery acid neutralizer spray and hit it next
month.

There's been conversation of having replacement gearmotors on stock at the club
for their eventual replacement. I asked how they've been failing in the past
and learned it was because the lubricant leaked out. Curiously, the gearbox has
neither an oil drain plug or an oil fill plug, meaning there's not really
anything we can do make sure the gearbox doesn't dry out. This seems like a
less than optimal design!

I looked from underneath the locomotive with an eye on lubrication. I can see a
thin ring of shiny liquid at the gearbox seal and the axle shaft is dirty from
dust sticking to a thin film of oil. This was visible to varying degree on the
first, second, and fourth axles.

![SF163 dirty oily fourth axle](./20261005_sf163_oily_fourth_axle.jpg)

The third axle looks dry and there's no gunk accumulation.

![SF163 clean third axle](./20261005_sf163_clean_third_axle.jpg)

Without an oil level check or a fill plug, there's nothing I can do for
the other three axles. I don't particulary enjoy that feeling, but oh well.

To make myself feel better, I pulled out the cosmetic maintenance kit and made
SF163 look pretty. I am not happy someone put her away with a big glop of bird
poop on the roof. It's gone now.

---

## Saturday 2026/10/3

* 4 hours today, 626.5 hours this track year.

#### 8:00AM - 12:00AM (4 hours)

Joined meeting at panel A with Strawn and Brock on what we would like panel A
to become in the future. I'm usually more focused on immediate problems and
this was a change of pace. I found myself feeling impatient with discussions
about far off dreams when we have mainline problems to fix. It didn't help that
the long term problems I personally want to fix (switch NT ring to wireless)
was shot down. On the upside, I asked why the layout is so focused on toggle
buttons to switch between state instead of buttons that let the user command a
desired state and there didn't seem to be any reason why not. Might be worth
chasing down in the near future to solve some immediate problems.

#### Signals electronics work afternoon (0 hours)

After lunch we continued working on next iteration of signals electronics in
Strawn's air conditioned home instead of heat wave outdoors. We switched in and
out of signals too often for me to know how many work hours I should claim so
I'm not going to claim any for this session.
