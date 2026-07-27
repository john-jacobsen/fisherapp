"""
Generator for the stat-hyp-setup walkthrough.

Set up a one-sample hypothesis test about a population mean: identify the
parameter, the hypothesized value mu0, the null H0 (equality), the alternative
Ha (>, <, or != depending on the wording of the claim), and whether the test is
one- or two-tailed.

The scenario DIRECTION is chosen at random (greater / less / different), which
drives the correct Ha symbol, the correct-option index for the Ha step, and the
correct-option index for the tail step. Every direction keeps the multiple-choice
options unique and the hydrated correct indices in range.

Returned variables:
  who           the actors making the claim (subject of the scenario sentence)
  noun          the quantity being measured (e.g. "battery life")
  unit          the unit of measurement (e.g. "hours")
  mu0           the hypothesized value stated in the claim (integer)
  scenario      the full worded problem statement
  direction     'greater' | 'less' | 'different'
  claim_verb    verb phrase matching the direction ("exceeds" / "is less than" / "differs from")
  ha_symbol     LaTeX comparison for Ha: '>', '<', or '\\neq'
  ha_index      correct option index in the Ha step (0='>', 1='<', 2='\\neq')
  ha_words      plain-English direction ("greater than" / "less than" / "different from")
  tail_index    correct option index in the tail step (0=left, 1=right, 2=two-tailed)
  tail_full     descriptive tail phrase ("one-tailed (right-tailed)" / ... / "two-tailed")
  tail_side     'right' | 'left' | 'neither'
"""
import random

_CONTEXTS = [
    {"who": "Quality-control engineers at a battery plant",
     "noun": "battery life", "unit": "hours", "lo": 8, "hi": 20},
    {"who": "A team of city traffic researchers",
     "noun": "daily commute time", "unit": "minutes", "lo": 20, "hi": 45},
    {"who": "Nutrition analysts at a cereal company",
     "noun": "sodium content per serving", "unit": "milligrams", "lo": 120, "hi": 220},
    {"who": "Agronomists at a seed company",
     "noun": "corn yield per acre", "unit": "bushels", "lo": 140, "hi": 200},
    {"who": "The operations staff at a coffee chain",
     "noun": "wait time in the drive-through", "unit": "seconds", "lo": 90, "hi": 180},
]

# direction -> (claim_verb, ha_symbol, ha_index, ha_words, tail_index, tail_full, tail_side)
_DIRECTIONS = {
    "greater":   ("exceeds",      ">",     0, "greater than",   1, "one-tailed (right-tailed)", "right"),
    "less":      ("is less than", "<",     1, "less than",      0, "one-tailed (left-tailed)",  "left"),
    "different": ("differs from", r"\neq", 2, "different from", 2, "two-tailed",                "neither"),
}


def generate() -> dict:
    ctx = random.choice(_CONTEXTS)
    direction = random.choice(list(_DIRECTIONS.keys()))
    claim_verb, ha_symbol, ha_index, ha_words, tail_index, tail_full, tail_side = _DIRECTIONS[direction]

    mu0 = random.randint(ctx["lo"], ctx["hi"])

    scenario = (
        f"{ctx['who']} suspect that the mean {ctx['noun']} {claim_verb} "
        f"{mu0} {ctx['unit']}. They want to set up a hypothesis test for this claim."
    )

    return {
        "who": ctx["who"],
        "noun": ctx["noun"],
        "unit": ctx["unit"],
        "mu0": mu0,
        "scenario": scenario,
        "direction": direction,
        "claim_verb": claim_verb,
        "ha_symbol": ha_symbol,
        "ha_index": ha_index,
        "ha_words": ha_words,
        "tail_index": tail_index,
        "tail_full": tail_full,
        "tail_side": tail_side,
    }
