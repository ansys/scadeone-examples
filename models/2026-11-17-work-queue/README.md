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
- Python 3, to build the panel

## Content

| Folder | Content |
|---|---|
| `dll` | The generic list, on integers, with its tests (`TestDll...` jobs) |
| `work-queue` | The work queue: controller, storyline, display views and tests |
| `work-queue/display` | The SCADE Display panel generator and the Scade One project that drives the panel |

The list in `work-queue/assets/JobList.swan` is the same module body as
`dll/assets/Dll.swan`, instantiated on jobs: the two interfaces differ only by
`use Job as Item;` and the capacity `N`.

## Instructions - Scripted demo and tests

1. In **Scade One**, open project `.\work-queue\work-queue.sproj`
    - Open `Demo.swant` and start a debug session on harness `Demo::work_queue`:
      a 35-cycle storyline that exercises every command.
    - Run the `Demo...` test jobs; each one must report all tests passed.

2. In **Scade One**, open project `.\dll\dll.sproj`
    - Run the `TestDll...` test jobs.

## Instructions - Interactive panel

1. Build the panel (SCADE Display 2027 R1 command line, no GUI needed):

    ```powershell
    cd work-queue
    python display\tools\build_panel.py --snapshot
    ```

   If SCADE Display is not installed in `C:\Program Files\ANSYS Inc\v271`, set
   `SCADE_DISPLAY_HOME` to its `SCADE Display` folder first.

2. In **Scade One**, open project `.\work-queue\display\demo\demo.sproj`
    - Run the `LivePanel` simulation job.
    - Click or drag the job buttons to queue jobs, drag cards to reorder them,
      drop them on Trash to cancel them, and hover the memory slots to see their
      links.

See [work-queue/README.md](work-queue/README.md) for the full description of
the controller, the storyline, the panel gestures and the memory figures.
