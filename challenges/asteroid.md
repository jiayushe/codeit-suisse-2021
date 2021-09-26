# Asteroid

### Instructions

Earth is in imminent danger from natural disaster! A line of asteroids of similar sizes are hurtling pass Mars at an
astounding speed and will reach Earth in a matter of days. You are part of a military research team tasked with stopping
the world-ending catastrophe, your experimental graviton bomb can finally be put to good use.

The graviton bomb creates multiple waves that is able to pull in asteroids resulting in mutual destruction. The
resultant explosion increases the strength of the gravity waves, leading to a stronger pulling force and wider affected
radius. If there are no similarly sized asteroids remaining, the gravity wave weakens and dissipates.

Design an algorithm that decides where to fire the bomb into the line that destroys the most asteroids based on the score so that Earth can
be saved!

Expose a `POST` endpoint `/asteroid` for us to verify!

### Damage Score Multiplier

The gravity wave expands on both the left and right of the origin within the asteroid line. Aggregate the number of
asteroids on both sides of the wave that are the same size and tally the score together with the multiplier! As the wave
meets a different asteroid size, it will be reset.

| Number of Asteroids Destroyed per Asteroid Size | Multiplier |
|:----------------------:|:----------:|
|          >= 10         |      2     |
|          >= 7          |     1.5    |
|          <= 6          |      1     |

### Information

1. `input` represents the asteroid line that the system will be generating.
2. `score` represents the total number of asteroids destroyed based on the score multiplier.
    * The score multiplier of the number of asteroids is calculated per asteroid size.
3. `origin` represents the zero-based position within the line on where to send the graviton bomb to.
4. Alphabets in uppercase are used to represent asteroid sizes.
5. Only similar sized asteroids will be pulled into the bomb detonation point.
6. All origin points that gives the same score will be accepted. See example below for more details.
7. Minimum score is 1 as the bomb will destroy the asteroid at the point of origin even if the gravity wave dissipates immediately.
8. The gravity wave will travel not per asteroid but as per the asteroid size.

Test cases given may change.

#### Example Input

```json5
{
  "test_cases": [
    "CCCAAABBBAAACCC",
    "BBAAABBB",
    "CCCAAAAABBBAAACCC",
    "ABBBBA"
  ]
}
```

#### Output Expected

```json5
[
  {
    "input": "CCCAAABBBAAACCC",
    "score": 15,
    "origin": 7
  },
  {
    "input": "BBAAABBB",
    "score": 8,
    "origin": 3
  },
  {
    "input": "CCCAAAAABBBAAACCC",
    "score": 21,
    // AAAAA + AAA has a length of 8 which has a multiplier of 1.5. The multiplier then resets for CCC + CCC.
    "origin": 9
  },
  {
    "input": "ABBBBA",
    "score": 6,
    "origin": 2, // or 3. Both origin points would give the same score.
  }
]
```
