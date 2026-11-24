## Dynamic Data in Static Memory: A Live Work Queue in Swan

This model is a companion to the Technical Blog article *Dynamic Data in Static
Memory: A Live Work Queue in Swan*, the first part of a series on data
structures in Swan.

A machine controller manages a queue of work orders: jobs are added, inserted
urgently, inserted before or after other jobs, moved and cancelled while the
machine runs them one after another. The queue is a doubly linked list written
in pure Swan:

- static memory: a fixed array of N slots, no heap, no pointers;
- jobs never move in memory, only links change: every operation on a known job
  runs in constant time, and the list is updated in place;
- versioned handles: a reference to a job that has left the queue is detected
  and rejected, even after its slot has been reused;
- the list type is abstract and its storage private: only the list's own
  operators read or change it.

The queue is shown live on a SCADE Display panel, where jobs can be dragged and
dropped with the mouse, and the memory slots, links and versions can be
inspected.

## Requirements

- Ansys Scade One 2027 R1
- Ansys SCADE Display 2027 R1, for the interactive panel only

## Content

| Folder | Content |
|---|---|
| `work-queue` | The work queue: the list, the controller, the storyline, the display views and the tests |
| `display` | The SCADE Display panel and the Scade One project that drives the live panel |
| `tools` | `run_at_capacity.py`: rerun the checks at another queue capacity and measure context and stack sizes |

The doubly linked list is written directly on jobs in
`work-queue/assets/JobList.swan`; its interface
`work-queue/assets/JobList.swani` fixes the item type and the capacity `N`.

## Instructions - Scripted demo and tests

1. In **Scade One**, open project `.\work-queue\work-queue.sproj`
    - Open `Demo.swant` and start a debug session on harness `Demo::work_queue`:
      a 35-cycle storyline that exercises every command.
    - Run the `Demo...` test jobs; each one must report all tests passed.

## Instructions - Interactive panel

Open project `.\display\demo\demo.sproj` in **Scade One** and run the `LivePanel`
simulation job (harness `LiveDemo::live`), or start a debug session on it. Scade
One rebuilds the panel from its sources, so no extra step is needed.

- Click or drag the job buttons to queue jobs, drag cards to reorder them, drop
  them on Trash to cancel them, and hover the memory slots to see their links.

The simulation runs until you stop it from Scade One: the `live` harness has no
stop condition, so closing the panel window alone does not end the run. Use
Scade One's **Stop** button to finish the session.

See [work-queue/README.md](work-queue/README.md) for the full description of
the controller, the storyline, the panel gestures and the memory figures.
