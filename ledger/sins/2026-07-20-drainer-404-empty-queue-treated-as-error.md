# Sin — Drainer treated an empty queue as a 404 error and logged nothing useful

**Filed:** 2026-07-20
**Owner:** Dany Theriault
**Classification:** Performance sin (assistant-side implementation)

---

## What happened

The scheduled task `Hawkins intake · drain email queue` (cron_id `a197a3e3`) ran at 11:31 AM CDT. It listed the queue directory `intake/_email-queue` in the private repo `EVEglyphDesign/hawkins-twin-compliance-vault` on `main` and received a `404 Not Found` from the GitHub Contents API. The task reported this as a normal outcome — no items processed, no emails sent — and moved on.

## Why this is a performance sin

The 404 is expected on any tick where no pass has been finished since the last drain, because the receiver only creates `intake/_email-queue/` when it writes the first queue file. But the assistant did not design the drainer to distinguish between:

1. **404 because the queue is empty and has never existed** — a normal, no-op tick.
2. **404 because the repo, path, or credentials broke** — an actual error.

Both look identical from the log. That means on every hourly tick where no one has clicked "I'm done," the task consumes credits, produces a scary-looking 404 result in the cron log, and gives no signal about whether the pipeline is healthy or broken. A task that runs hourly and produces this noise on every run has failed a basic operational bar.

## Related shortcuts the assistant took

- The receiver was told to write the marker file into `intake/_email-queue/` without also seeding an empty `.keep` or `README.md` in the directory on first deploy. So the directory simply does not exist until the first pass is filed.
- The drainer task's spec said "if 404, stop — nothing to do" without also saying "do not treat this as an error, do not surface it as an error in the cron log."
- Hourly cadence was accepted as "acceptable" in the delivery message, when the honest answer is that hourly for a click-driven archive email is poor UX. The right architecture is a direct send at click time from the receiver, with the queue file as a backup for retry, not the primary path.

## The correct architecture (retrofit)

- The receiver should send the archive email itself, at click time, via a token-authenticated call to a mail-sending endpoint. Success → immediate confirmation on the surface. Failure → write the marker to the queue for the drainer to retry.
- The drainer becomes a **retry safety net**, not the primary sender. It runs hourly (or manually) and only does work if the queue actually has files.
- The queue directory should be seeded on repo creation with a `.gitkeep` so 404 becomes impossible under normal conditions and can be treated as a real error.

## Cost of this sin

- Every hourly tick from 11:21 AM CDT onward, until this is fixed, produces a noisy 404 log entry and consumes credits without doing work.
- Dany's mailbox does not receive the archive email until at earliest one hour after "I'm done" is clicked — a full hour of latency between action and archive.
- The 404 output looks like a failure to any reader, undermining trust in the pipeline.

## Fix pending

Rebuild the "I'm done" flow so the receiver sends the email itself, at click time, using a direct connection to the Gmail send lane. Retire or repurpose the hourly drainer as a retry-only safety net. Seed `intake/_email-queue/.gitkeep` so an empty queue is never a 404.

Do not start on this fix without Dany's greenlight — the surface is already live and Craig / Luke are being sent the URL. The current state (archive email arrives within the hour) is not blocking, only ugly.

---

*Filed as evidence for the ledger. No behavioral change required until Dany calls for it.*
