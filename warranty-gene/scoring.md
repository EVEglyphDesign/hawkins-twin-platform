# Warranty GENE — Scoring formula

A rich-target score is a single number between 0 and 100, computed
deterministically from three inputs already present in the row. It is written
out under `score.total` so the executive control surface can order the fourth
cohort without recomputing.

## Inputs

- **margin_estimate_cad** — sum, across every open job whose `coverage_bucket`
  is not `none`, of `SRT_hours × labor_rate + parts_estimate`. Parts are
  approximated at 0.6× labor when the row is generated from bulletin data; on
  the live twin, parts come from CDK inventory. When `parts_on_hand=false` the
  parts side is multiplied by the standard parts markup, because ordering fresh
  captures margin the counter would otherwise lose.
- **booking_urgency** — derived from PACCAR Solutions telemetry:
  - `inbound-tonight` — currently inside the Hawkins region **and** projected
    to sleep in Hawkins-NB
  - `inbound-this-week` — projected to enter Hawkins-NB within the projection
    window, not yet in region
  - `in-region` — inside the region but projected to leave
  - `out-of-region` — everything else
- **time_to_expiry_days** — the smallest of `(months_remaining × 30)` and
  `(distance_remaining_km ÷ 500)` across every coverage bucket touched by an
  open job. The 500 km/day assumption is the fleet-average line-haul figure and
  is documented here so it can be swapped without rewriting the formula.

## Composition

```
margin_c    = min(50, margin_estimate_cad / 10000 * 50)
urgency_c   = { inbound-tonight: 30, inbound-this-week: 22,
                in-region: 15, out-of-region: 0 }[booking_urgency]
expiry_c    = 20 if tte <= 90
              14 if tte <= 180
              8  if tte <= 365
              3  otherwise
total       = round(margin_c + urgency_c + expiry_c, 1)
```

Ceilings, not multipliers. A single very-large-margin job cannot dominate the
list; a truck sleeping in-region tonight cannot be ignored just because its
margin is modest. Expiry contributes only when the coverage window is actually
narrow — Warranty GENE is not in the business of manufacturing false urgency.

## Lane routing

`compliance.clean == false` sends the row to the **review lane** regardless of
score. A truck missing Prior Approval for a job that requires it, or carrying
an ineffective-repeat flag, is not a booking candidate — it is a human
decision. This is why VIN `1XPBSYN00M1000303` (MX VGT, missing Prior Approval)
appears in the samples with a healthy in-region urgency but is not offered to
the booking lane.

## Not in the score

- Customer historical loyalty. Kept out on purpose — the twin surfaces the
  opportunity, the counter person owns the relationship.
- Weather or road-closure state. The overnight-region projection already
  captures whether the truck is realistically inbound.
- Any prediction about whether the customer will accept the appointment. That
  is the outreach team's judgment call.
