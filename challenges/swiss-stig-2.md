# Swiss Stig (Part 2)

Some say, Swiss Stig is wearing a helmet because he's actually a duck.

Some say, this is a Swede reference that got swapped out at the very last second.

## Important message

This is a mult-part challenge. You may directly reuse solutions of later parts to solve earlier parts for full score.

## Background

As the season progress and more interviews are conducted, Jeremy has learnt to observe, adapt, and improvise -- A master
interviewer should not stick with the questions he drafted a priori, but shall play with the flow.

Here is how he adjusts the questions in real time...

1. Observe: Observe his accuracy on **this interview** so far, i.e. Answer to Jame's question if this interview only
   consist of questions he has asked thus far, **NOT** the accuracy of previous interviews!
2. Adapt: Adapt the range borders by the formula `from := (from + p*p1 + q*q1 - 1 mod MAX) + 1; to := (to + p*p2 + q*q2 - 1mod MAX) + 1`.
   The definitions are given in previous input and output sections.
3. Improvise: Swap the new values of from and in case if `from > to`, to keep the range non-degenerate.

### Inputs, Outputs, Constraints

Input is similar to subtask 1, with coefficients now taking two pairs of integers that are not necessarily zeros.

```tex
0 <= coefficients.{x|y} <= 1e9
```

All other constraints remains identical.

### Scoring

Subtask total: 400; You may reuse any solution to score another 400 points in part 1.

### Endpoints

Expose an endpoint `/stig/ben`

## Extra

### This task is not an official task, but as a brain candy for the night

By now you should have realized Jeremy's methodology is extremely inefficient, 
so do Jeremy, hence he has decided to merge several intervals into a single question.

### Inputs, Outputs, Constraints

1. The definition of "Question" type is reduced from "Singleton list of interval" to "Non-empty list of intervals".

All other constraints remains identical

### Scoring

**This task is neither scored nor judged**.
