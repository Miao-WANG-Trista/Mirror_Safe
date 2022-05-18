# Mirror_Safe
## Thinking process
### Where to put the mirror?
We know the positions of all other mirrors inside the safe, we can simulate both forward path, the ray trace starting from the laser, and backward path,  the ray trace starting from the detector, where we assume there is a laser beam from the detector and observe its path.

- if the forward path can reach the detector, it means the safe opens without inserting a mirror, we will output 0.
- if the forward path and backward path have overlaps, we know that's where we should insert a mirror, and there might be multiple such locations and orientations.
- if there is no overlap, we know the safe cannot be opened with or without inserting a mirror.

Below is the flow chart for this process.

<img width="588" alt="image" src="https://user-images.githubusercontent.com/77568908/168939544-9a944555-52a3-4b7e-ab69-7f3da11beed3.png">


### How to simulate the path?
Key points:

1. For the forward path, starting point is (1,1) with 'right' and 'horizontal' orientation. For the backward path, starting point is (r,c) with 'left' and 'horizontal' orientation.
2. The beam will continue moving in the current orientation until it meets another mirror or reaches the boundary. 
3. Once meeting a mirror, the beam will change its orientation and in total, there are 4 orientations: right & left & upward & downward

if the mirror is /:
- right -> upward
- left -> downward
- upward -> right
- downward -> left

if the mirror is \ :
- right -> downward
- left -> upward
- upward -> left
- downward -> right

4. there are two corner cases:
> the safe can be opened without inserting a mirror --> the laser beam can reach the detector without another mirror --> return 0
> there already exists a mirror in every overlap point --> should return 'impossible' too

Solutions:

1. In this problem, we have in total three classes:
> Laser()

| Attributes        | Notes                                |
|-------------------|--------------------------------------|
| orientation       | will be changed in set_orientation() |
| position(row,col) | will be changed in move()            |
| visited_cells     | the simulation of a beam path        |

| Methods(not inclusive) | Notes                                                                                           |
|------------------------|-------------------------------------------------------------------------------------------------|
| move()                 | will move one step with each call, position will be changed, and visited_cells will be appended |
| set_orientation()      | will be changed in move()                                                                       |

> Cell()

| Attributes/ Methods | Notes                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------|
| mirror_type         | the mirror type of that cell,'None',default value, means there is no mirror, 'left' or 'right' |
| reflect()           | based on input orientation and mirror type, return new orientation                             |

> Grid()
Grid is made of r * c cells and in _init_(), we will create a list of cells, where each element will be an instance of class Cell()

| Methods          | Notes                                                                                                      |
|------------------|------------------------------------------------------------------------------------------------------------|
| compute_path()   | with initialization of orientation and position, a simulated beam path can be generated inside such a grid |
| is_beam_inside() | a condition to be met for while loop inside compute_path()                                                 |
| find_solutions() | print output of required format                                                                            |

2. We will simulate laser's movement step by step. Once meeting a mirror, its orientation will be changed. To realize, we can create two dictionaries: LEFT_MIRROR and RIGHT_MIRROR.
3. For two kind of cases:
the condition for returning 0: the point at the right to the bottom right cell can be visited
<img width="179" alt="image" src="https://user-images.githubusercontent.com/77568908/168867005-86400215-4e5a-4f20-ba94-a1020346a387.png">

the condition for returning 'impossible': there is no element in the differnce between mirror_set and intersection (between forward_path and backward_path) 

### Any possibility of an infinite loop?
With below illustration, we can prove there cannot be a trap.

<img width="179" alt="image" src="https://user-images.githubusercontent.com/77568908/168870462-89958adf-a835-4131-9d99-b2aa06484d4d.png">

a light beam enters this trap and it won't get out of this box. However, if there was a trap, the light beam will eventually come back to this mirror, but it cannot hit it with 'right' direction since this direction implies the beam comes from outside. Meanwhile, for all other 3 directions, the beam will escape the trap.

**representation**
1. To be more memory efficient and flexible, we will map orientations to a tuple of 2 ints
    (0, 1): "right",
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left"
2. mirror_type: '/' --> 'left'; '\' --> 'right'

## Analysis on memory usage and runtime performance
Memory usage:
We have objects of three classes:
Cell(): each of its attribute 'mirror_type' 1 string 'left'/'right' will take around 54 bytes and there will be r * c cells.
Laser(): each of its attributes 'orientation' 2 ints 'position' 2 ints 'visited_cells' r * c * 3 ints (pointers considered). In total, it will take around 28 * (4+3rc) bytes and there will be 2 lasers, forward and backward
Grid(): each of its attributes 'rows' 1 int 'columns' 1 int 'mirror_set' (m+n) * 3 ints. In total, it will take around 28 * (2+3*(m+n)) bytes and there is only one grid.
Plus, there are three variables, total_rows, total_columns, joint_list, which will take around (m+n) * (2*28+54)+2*28 = 56+110 * (m+n)
Overall, this algorithm will take around 112+194*(m+n)+222* r * c

## How to run the code
Each test case should be stored in a txt file and each txt file only represents one test case.

Step 1. Put the txt file into the same directory with main.py and helpful_functions.py.<br>
Step 2. In the terminal, cd to the current directory<br>
Step 3. run 'python main.py test.txt'<br>
