# Parasite

### Background
___
A mad scientist decided to create an infectious parasite which he released to several rooms filled with subjects. These subjects were bound to their positions and were unable to move around in the enclosed room. He then carried out the experiments according to the parameters. Your job is to calculate and corroborate with the results of the scientist.

### Description
___
Given a 2-D array with the 4 possible representations:

| Number | Representation |
| ------- | ------------- |
| 0 | Vacant |
| 1 | Healthy |
| 2 | Vaccinated |
| 3 | Infected |

#### Assumptions:
1. A vaccinated person will provide 100% immunity from the parasite.
2. An infected person can spread to multiple healthy people per tick
3. Time starts from 0 in each room
4. Parasite can only travel across subjects and not vacant space
5. There is only one parasite released per room

The challenge is divided into 4 parts:
1. Parasite A can travel both horizontally and vertically. Calculate the time taken to infect a healthy person. Return `-1` if person remains healthy or if the person is infected to begin with.
2. Find the time taken to infect the whole room with Parasite A. If it is impossible to infect healthy persons, return `-1`
3. A new mutated strain, Parasite B, is released to the room. Parasite B could infect diagonally on top of Parasite A's. Find the time taken to infect the whole room. Return `-1` if impossible to infect all healthy persons.
4. A third strain, Parasite X, is able to cross through vacant spaces. This strain is only able to move horizontally and vertically. Calculate the energy needed to infect all healthy persons assuming one energy is used when moving across vacant space (Treat a vaccinated person as vacant space).
NOTE: For parts (1-4), we are looking at the minimum time/energy

### Task Objective
___
Provide an endpoint `/parasite` that will take in an `application/json` request body and return an `application/json` on `200` response within 15 seconds.

#### Constraints
- `2` <= _rows_ <= `50`
- `2` <= _columns_ <= `50`
- _rooms_ == `20`

#### Input format
The input given is in the format of a json array.

Each element in the array contains an object with the following parameters:
1. `room: int`
2. `grid: list [ list [int] ]`
3. `interestedIndividuals: list [ string ]`
Note: list of interested individuals are given in `(row, col)`

#### Sample Input
```json
[
  {
    "room": 1,
    "grid": [ [0, 3], [0, 1] ],
    "interestedIndividuals": [ "0,0" ]
  },
  {
    "room": 2,
    "grid": [ [0, 3, 2], [0, 1, 1], [1, 0, 0] ],
    "interestedIndividuals": [ "0,2", "2,0", "1,2" ]
  }
]
```

#### Output format
An object with the following parameters will be returned as response:
1. `room: int`
2. `p1: dict { string : int }`
3. `p2: int`
4. `p3: int`
5. `p4: int`

#### Sample Output
```json
[
  {
    "room": 1,
    "p1": { "0,0": -1},
    "p2": 1,
    "p3": 1,
    "p4": 0
  },
  {
    "room": 2,
    "p1": { "0,2": -1, "2,0": -1, "1,2": 2},
    "p2": -1,
    "p3": 2,
    "p4": 1
  }
]
```

#### Explanation
For room 1:
1. `p1` has value of `-1` as it is not possible to infect vacant cell at `(0,0)`
2. `p2` has value of `1` as it takes 1 tick to infect whole room
3. `p3` has value of `1` as it takes 1 tick to infect whole room
4. `p4` has value of `0` as it takes 0 energy to infect whole room

For room 2:
1. `p1` has values of
  1. `-1` as person at `(0,2)` is vaccinated
  2. `-1` as it is impossible to infect healthy person at `(2,0)`
  3. `2` as it takes 2 ticks to infect person at `(1,2)`
2. `p2` has value of `-1` as it is impossible to infect whole room (healthy person at `(2,0)` cannot be reached)
3. `p3` has value of `2` as it takes 2 ticks to infect whole room (infection moves to `(2,0)` during 2nd tick)
4. `p4` has value of `1` as it takes 1 energy to reach `(2,0)`

### Scoring
___
1. Total score is summation of individual room score rounded down out of 100%
2. Each room score is calculated as follows:
  1. Getting all of p1 correct gives `15` marks
  2. Getting p2 correct gives `15` marks
  3. Getting p3 correct gives `10` marks
  4. Getting p4 correct gives `60` marks
  5. Marks for higher parts are only given when lower parts are answered fully

#### Example
1. Participant is given 3 rooms
2. Participant answered p1, p2, p3, p4 correct for room 1 (`100` marks for room 1)
3. Participant answered p2, p3, p4 correct for room 2 (`0` marks for room 2 as p1 is not answered correctly)
4. Participant answered p1, p2 correct for room 3 (`30` marks for room 3 )
5. Total score for participant will be `130/300 = 43%`
