## Requirements
* Ansys Scade One 2025 R2 or later
* Ansys SCADE Rapid Prototyper 2025 R2 or later

## Instructions
1. Open project `SantaPanel/SantaPanel.etp` in SCADE Rapid Prototyper.
2. Run build configuration `ScadeOnePanel` to (re)build `SantaPanel/SantaMonitor_ScadeOneCosimulation/SantaMonitor.sproj`.
3. Copy the newly-built `SantaPanel/SantaMonitor_ScadeOneCosimulation/SantaMonitor.sproj` to `SantaClaus/resources/SantaMonitor.spanel`. 
4. Open project `SantaClaus/SantaClaus.sproj` in Scade One.
5. Run a debug session on test harness `Tests::test_NorthPole`.

## Model details
The Santa Claus Problem is a synchronization problem in concurrent programming.

It involves Santa Claus🎅🏻, his elves🧝, and his reindeers🦌, and it is used to
illustrate the complexities of managing multiple concurrent processes.

### Problem Description
* Santa Claus: Sleeps until woken up by either all his reindeers being back from vacation or by a group of elves needing his help.
* Reindeer: After returning from vacation, they wait until all nine are back, then wake up Santa to get hitched to the sleigh.
* Elves: Work independently but occasionally need Santa's help. They form groups of three and wake up Santa for assistance.

### Constraints
* Santa should only be woken up by either all nine reindeer or a group of three elves.
* If Santa is helping three elves, other elves must wait until he is done.
* If Santa is preparing the sleigh, elves must wait (i.e. reindeer take priorities over elves).
* Reindeer should not wait indefinitely if there are elves needing help.

### Purpose
The Santa Claus Problem illustrates the synchronization challenges in managing shared resources, 
prioritizing tasks, and preventing issues such as:
* Deadlock: Processes wait indefinitely due to resource contention.
* Starvation: Some processes never get served.
* Fairness: Ensuring all threads get a chance to execute.
