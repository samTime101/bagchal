@Author: Samip Regmi

## Execution
- from root , create a virtual environment and activate it
- `pip install -r requirements.txt`
- `python -m src.server.server.py` 

---

This is complete informal document, made for me, I will refactor on some other day
## Basic Information about players
Number of goats: 20
Number of Tigers: 4

---
### Denitions of players by me
Tiger Denotion: -1 
Goat Denotion: 1
Empty position: 0

---
## Board Initialization
Possible grid: 25
Initialized from 0 to 24

| 0   | 1   | 2   | 3   | 4   |
| --- | --- | --- | --- | --- |
| 5   | 6   | 7   | 8   | 9   |
| 10  | 11  | 12  | 13  | 14  |
| 15  | 16  | 17  | 18  | 19  |
| 20  | 21  | 22  | 23  | 24  |
### First Move
According to game rule, the first move is always fixed to tiger as far as i have understood so their initial position is also fixed
Board[0] = Board[4] = Board[20] = Board[24] = -1

| -1 (0) | 1   | 2   | 3   | -1(4)  |
| ------ | --- | --- | --- | ------ |
| 5      | 6   | 7   | 8   | 9      |
| 10     | 11  | 12  | 13  | 14     |
| 15     | 16  | 17  | 18  | 19     |
| -1(20) | 21  | 22  | 23  | -1(24) |

So the actual values are -1 , the 0,20,4,24 are their index i.e their positions

---
## Possible Moves from each position
#### Default Case
As the default move from initial position is fixed, we will hard code
This will only differ in the case of `jump` but we will handle that case later
Table Name : **N**

| From | To                      |
| ---- | ----------------------- |
| 0    | 1,5,6                   |
| 1    | 0,2,6                   |
| 2    | 1,3,6,7,8               |
| 3    | 2,4,8                   |
| 4    | 3,8,9                   |
| 5    | 5,10                    |
| 6    | 0,1,2,5,7,10,11,12      |
| 7    | 2,6,8,12                |
| 8    | 2,3,4,7,9,12,13,14      |
| 9    | 4,8,14                  |
| 10   | 5,6,11,15,16            |
| 11   | 6,10,12,16              |
| 12   | 6,7,8,11,13,16,17,18    |
| 13   | 8,12,14,18              |
| 14   | 8,9,13,18,19            |
| 15   | 10,16,20                |
| 16   | 10,11,12,15,17,20,21,22 |
| 17   | 12,16,18,22             |
| 18   | 12,13,14,17,19,22,23,24 |
| 19   | 14,18,24                |
| 20   | 15,16,21                |
| 21   | 16,20,22                |
| 22   | 16,17,18,21,23          |
| 23   | 18,22,24                |
| 24   | 18,19,23                |
#### In the case of Jump by tiger
Now this is the case of all possible jumps 
Table Name : **J**

| From | To  | Jump |
| ---- | --- | ---- |
| 0    | 2   | 1    |
| 2    | 0   | 1    |
| 1    | 3   | 2    |
| 3    | 1   | 2    |
| 2    | 4   | 3    |
| 4    | 2   | 3    |
| 5    | 7   | 6    |
| 7    | 5   | 6    |
| 6    | 8   | 7    |
| 8    | 6   | 7    |
| 7    | 9   | 8    |
| 9    | 7   | 8    |
| 10   | 12  | 11   |
| 12   | 10  | 11   |
| 11   | 13  | 12   |
| 13   | 11  | 12   |
| 12   | 14  | 13   |
| 14   | 12  | 13   |
| 15   | 17  | 16   |
| 17   | 15  | 16   |
| 16   | 18  | 17   |
| 18   | 16  | 17   |
| 17   | 19  | 18   |
| 19   | 17  | 18   |
| 20   | 22  | 21   |
| 22   | 20  | 21   |
| 21   | 23  | 22   |
| 23   | 21  | 22   |
| 22   | 24  | 23   |
| 24   | 22  | 23   |
| 0    | 10  | 5    |
| 10   | 0   | 5    |
| 5    | 15  | 10   |
| 15   | 5   | 10   |
| 10   | 20  | 15   |
| 20   | 10  | 15   |
| 1    | 11  | 6    |
| 11   | 1   | 6    |
| 6    | 16  | 11   |
| 16   | 6   | 11   |
| 11   | 21  | 16   |
| 21   | 11  | 16   |
| 2    | 12  | 7    |
| 12   | 2   | 7    |
| 7    | 17  | 12   |
| 17   | 7   | 12   |
| 12   | 22  | 17   |
| 22   | 12  | 17   |
| 3    | 13  | 8    |
| 13   | 3   | 8    |
| 8    | 18  | 13   |
| 18   | 8   | 13   |
| 13   | 23  | 18   |
| 23   | 13  | 18   |
| 4    | 14  | 9    |
| 14   | 4   | 9    |
| 9    | 19  | 14   |
| 19   | 9   | 14   |
| 14   | 24  | 19   |
| 24   | 14  | 19   |
| 0    | 12  | 6    |
| 12   | 0   | 6    |
| 2    | 14  | 8    |
| 14   | 2   | 8    |
| 2    | 10  | 6    |
| 10   | 2   | 6    |
| 4    | 12  | 8    |
| 12   | 4   | 8    |
| 10   | 22  | 16   |
| 22   | 10  | 16   |
| 12   | 24  | 18   |
| 24   | 12  | 18   |
| 12   | 20  | 16   |
| 20   | 12  | 16   |
| 14   | 22  | 18   |
| 22   | 14  | 18   |
| 6    | 18  | 12   |
| 18   | 6   | 12   |
| 8    | 16  | 12   |
| 16   | 8   | 12   |

---
## Validating Moves
### Case of a valid normal move
A move will be valid if our target is defined in as Table[current] and target is empty
i.e. To move from 0 to 1 , we will check if N[0]  has `requested_target` where in this case `requested_target` is 1 and if we look at table `N` , its valid and we also have to check if that requested position is empty
i.e

```
func is_valid(current_index, target_index):
	if N[current_index] has target_index and is_empty(target)
```

```
is_valid(current_index,target_index)
```

| From | To    |
| ---- | ----- |
| 0    | 1,5,6 |

### Case of a Jump move
i will write later, byeeeeeeeeeeeeeeee