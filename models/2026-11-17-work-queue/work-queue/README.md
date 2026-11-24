# Live Work Queue - a Swan 27R1 demo

The demo runs in the Scade One debugger, and on a SCADE Display panel through
[View::panel](assets/View.swan). Open [work-queue.sproj](work-queue.sproj) and
start the `Demo::work_queue` harness in [Demo.swant](assets/Demo.swant), or
`Demo::panel_gestures` for scripted gestures. The scripted storyline lasts
35 cycles. For the clickable panel, see [Interactive panel](#interactive-panel).

## Jobs are designated by their handle

When the controller queues a job, it returns the job's list handle
`Ref {idx, version}`, and later commands designate the job by that handle. Jobs
never move in the underlying array, so the handle stays valid when the job
changes position in the queue.

- The handle stays valid while the job is pending, whatever moves around it.
- It goes stale when the job is cancelled or starts running. A stale handle is
  rejected with `UnknownJob`, even after its slot has been reused: reuse
  increments the slot's version.
- Finding a job from its handle is a direct, O(1) access to its slot.

## Controller interface

[WorkQueue::controller](assets/WorkQueue.swan) has one input:

```swan
type command =
  Add {job: Job::t}
  | Urgent {job: Job::t}
  | InsertBefore {target: L::ref, job: Job::t}
  | InsertAfter {target: L::ref, job: Job::t}
  | Move {item: L::ref, before: L::ref}
  | Cancel {target: L::ref}
  | CancelType {operation: Job::operation}
  | Wait {};
```

and four outputs:

- `current`: `Idle {}` or `Working {job, remaining_cycles}`.
- `queue_length`: the number of pending jobs, excluding the running job.
- `command_status`: `Accepted`, `QueueFull`, `UnknownJob`, `InvalidDuration`,
  or `NoCommand` (for `Wait`).
- `accepted`: the handle of the job queued this cycle, `Null` otherwise.

The list stays internal state; it is not copied to an output every cycle.

## Machine semantics

- One command is applied per cycle, before advancing the machine. The
  controller diagram shows this as two blocks, `apply` then `advance`; the queue
  and the machine state return to the next cycle through two `pre` wires.
- The machine starts the next pending job when idle or when the previous job
  ends. A duration of D means D cycles of work, with no idle cycle between jobs.
- [Job::t](assets/Job.swani) is `{operation, duration_cycles}`;
  `Job::make(operation)` gives the standard duration. Zero durations are rejected.
- `Urgent` inserts at the front of the pending queue; it does not preempt the
  running job. `InsertBefore` with `Null` appends; `InsertAfter` with `Null`
  prepends, as in the list API.
- `Move {item, before}` relinks a pending job before another one (`Null`: at the
  end). The job keeps its slot and its handle. Moving a job onto itself or next
  to its current position is an accepted no-op.
- Cancellation affects pending jobs only. `CancelType` removes every matching
  pending job in one cycle and keeps the survivors' order.
- A rejected command leaves the pending queue unchanged; the machine still works
  during that cycle.

## Presentation storyline

[WorkQueue::scenario](assets/WorkQueue.swan) keeps the handles it receives on
the `accepted` output and reuses them in later commands.

| Cycle | Command | What to show |
|---|---|---|
| 1 | Add Inspect | Inspect starts at once, for 8 cycles. |
| 2-3 | Add Paint, Add Pack | Both wait. Paint is in slot 0 at version 1: Inspect used it first. |
| 4 | Urgent SafetyCheck | Inserted at the front of the pending queue. |
| 5 | InsertAfter Paint: Drill | Inserted in the middle, using Paint's handle. |
| 6 | Cancel Drill | Neighbours reconnect; slot 3 is freed. |
| 7 | Add Rework | Reuses slot 3, now at version 1. |
| 8 | Move Rework before Paint | Rework changes position but stays in slot 3. |
| 9 | Cancel Drill again | Rejected: the old handle is stale although slot 3 is in use. |
| 10 | CancelType Paint | SafetyCheck runs; Paint leaves the queue. |
| 11 | InsertBefore Pack: Drill | Rework starts; Drill reuses slot 0, at version 2. |
| 12 | Add Paint with duration 0 | Rejected with `InvalidDuration`. |
| 13 | CancelType Rework | The running Rework job is not affected. |
| 23-33 | | Drill, then Pack run. |
| 34-35 | | Idle, empty queue. |

The `Demo::work_queue` harness checks every cycle against this trace: status,
returned handle, running job, remaining cycles and queue length.

## Display panel

[View.swan](assets/View.swan) provides fixed-size views for a SCADE Display
panel, independent of the capacity N:

- `queue_view`: the first `CARDS` (8) pending jobs in order, each with its handle
  and slot. Built on `L::copy_front <<CARDS>>`, so it copies 8 jobs: O(CARDS).
- `page_view`: one page of `PAGE` (64) slots: state, operation, version, next
  and prev links (`ToSlot {slot}` or `NoLink` for a Null reference; prev is
  `NoLink` for a free slot), and head, tail and free-head markers. The panel
  draws `NoLink` as a ground symbol.
- `occupancy`: `STRIP` (64) cells, each giving the fill level in percent of an
  equal share of the N slots.
- `decode`: turns a panel `gesture` into a command. Gap k means "before card k";
  a gap past the last card means "at the end".

  | Gesture | Command |
  |---|---|
  | `NewCard {operation, gap}` | `InsertBefore` the card at the gap |
  | `DragCard {card, gap}` | `Move` the card before the card at the gap |
  | `DeleteCard {card}` | `Cancel` the card |
  | `CancelOperation {operation}` | `CancelType` |

  Handles come from the cards shown at the previous cycle. If that job has
  meanwhile left the queue, the command is rejected and nothing is corrupted.
- `panel (scripted, command, run, page)`: the controller plus all views.
  `scripted = true` plays the storyline; otherwise `command` is applied.
  The machine works one unit only on cycles where `run` is true, so a display
  can pace it independently of its own refresh rate; the storyline also moves
  one step per `run` cycle. `page` selects the memory page.

### Interactive panel

[../display/](../display) holds the SCADE Display panel and the Scade One
project that drives it. Open
[../display/demo/demo.sproj](../display/demo/demo.sproj) and run the `LivePanel`
simulation job (harness `LiveDemo::live`); the panel is rebuilt from its sources
by Scade One, so no extra step is needed. The `live` harness has no stop
condition: closing the panel window does not end the run, so stop the session
with Scade One's **Stop** button.

The panel passes no coordinates to the model. Each interactive item (queue
place, job button, End and Trash zones, control button) has its own rectangle
active area; the panel outputs one `inside` flag per item plus the pointer
`pressed` and `released` events. While a job
button or a card is dragged, a translucent ghost card follows the pointer. A
full-screen active area gives its position, as a ratio of the screen; that
position stays inside the panel and never reaches the model.

[Console.swan](../display/demo/assets/Console.swan) turns those flags into commands.
Its `console` node is a diagram of four small nodes: `drag` (press, drag and
release tracking), `fill` (the Fill sequencer), `transport` (Pause, Step and the
`pace_kind` Slow / Normal / Fast) and `pacer` (one `run` cycle per period).
`station` wires the hover flags through `console` into `View::panel`; every
`LiveDemo` harness is built on it.

| Gesture | Command |
|---|---|
| Click a job button, or drag it onto End | `Add` |
| Drag a job button onto a card | `InsertBefore` that card |
| Drag a job button onto Trash | `CancelType` of that operation |
| Click a card, or drag it onto Trash | `Cancel` |
| Drag a card onto another card | `Move` before that card |
| Drag a card onto End or an empty place | `Move` to the end |
| Click Pause / Step | Freeze the machine / work one unit while paused |
| Click Slow / Normal / Fast | One unit of work every 50 / 25 / 5 display cycles |
| Click Fill (set apart, under "Queue") | `Add` one job of each kind, one per cycle |

The top right corner shows the last command, spelled out (for example
`Insert Drill before Pack`), with its result below it: green when accepted, red
when rejected. Both stay until the next command.

At the 20 ms cycle of the simulation job, Normal speed is two units of work per
second, so an Inspect job (8 units) takes 4 s. A card being dragged keeps the
handle taken at the press; if that job starts running before the drop, the
command is rejected and the panel shows `Rejected: stale job` in red. Pressing
on an item, leaving it and releasing back on it is not a click.

The memory grid marks the queue head (H), tail (T) and free-list head (F) on
their slots. Hovering a memory slot, or a queue card, outlines that slot in
white, the slot its `next` link designates in yellow and, for a used slot, the
slot its `prev` link designates in cyan. A free slot has no `prev`; its `next`
is the free-list link. Each cell has its own active area, like the other items.

`LiveDemo::pointer_sessions`, `LiveDemo::pacing_and_fill`,
`LiveDemo::memory_focus` and `LiveDemo::command_text` (job `TestGestures`)
replay these gestures through the same hover flags the active areas produce and
check the resulting queue, highlights and last-command text.

## Capacity and memory

[JobList](assets/JobList.swan) is the doubly linked list, written directly on
jobs: [JobList.swani](assets/JobList.swani) fixes the item type (`Job`) and the
capacity `N`. The list body is generic in shape, so the same algorithms would
serve any item type by changing only the interface.

The list type is abstract: other modules hold, compare, delay and pass a
`L::list`, but only the list's own operators read or change it. Its storage
types (`Node`, `Slot`) are private to the list body. Handles (`L::ref`) and
operation results stay public, so clients still match on them. Walking the list
also stays inside the module: `L::remove_matching` does the bounded scan behind
`CancelType`, with the matching rule supplied by the item module
(`Job::matches`), since Swan operators cannot take functions as parameters.
`L::slot_info` and `L::free_front` give the memory grid a read-only view of the
slots.

The project uses N = 64, so a full memory page fits on screen. Changing `N` in
[JobList.swani](assets/JobList.swani) is the only change needed for another
capacity: the controller, the views and the display keep the same interface.
To check another capacity without modifying the project:

```powershell
python tools\run_at_capacity.py 10000
```

It runs all harnesses, generates C for the controller and the panel, and
measures them. With Scade One 2027 R1 and the bundled GCC 16.2, x86-64, `-O0`:

| | N = 64 | N = 10,000 |
|---|---|---|
| List (40 bytes per slot: version + node, plus 40) | 2,600 bytes | 400,040 bytes |
| Controller context | 2,620 bytes | 400,060 bytes |
| Panel context | 2,696 bytes | 400,136 bytes |
| Largest stack frame (`relink`) | 496 bytes | 496 bytes |
| All generated frames | 3,520 bytes (controller), 4,544 bytes (panel) | same |

Capacity affects persistent state only, not stack use. There is no heap
allocation. Keep the context in static storage: as an automatic C variable it
would put the whole queue on the caller's stack. These figures depend on the
compiler and target; remeasure for deployment.

- Insert, move, cancel, read at a handle, and dispatch: O(1).
- `CancelType` and `occupancy`: one bounded O(N) scan.

One-cycle bulk cancellation is bounded, not free: measure its execution time on
the target before claiming it fits a real-time budget.

## Repeatable jobs

| Job | Purpose |
|---|---|
| `DemoWorkQueue` | Scripted storyline; checks every cycle against the expected trace. |
| `DemoDurationBoundaries` | Durations 1 and 2, no idle cycle, identical jobs allowed, rejections. |
| `DemoCommandValidation` | Every command, handles returned, moves, stale handles after reuse. |
| `DemoBulkCancellation` | Full queue, saturation, removal of every other job in one command, survivor links, slot reuse. |
| `DemoPanelGestures` | Drag-and-drop gestures decoded and applied; queue, memory and overview views. |
| `DemoPanelScripted` | The panel's scripted mode reproduces the storyline. |
| `DemoWorkQueueCode` | C code for the controller and the script. |
| `DemoPanelCode` | C code for the panel node. |

```powershell
$launcher = Join-Path $ScadeOneHome 'tools\job_launcher\scade_one_job_launcher.exe'
& $launcher run --job DemoWorkQueue --project '.\work-queue.sproj'
```
