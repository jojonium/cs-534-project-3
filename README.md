# CS 534 Artificial Intelligence Project 3
This grid world program is written in python 3.7
To run this program make sure Python is installed
and numpy is installed as well. 

If numpy is not installed, you can install it from
the command line with the command
> pip install numpy

To run the Part 2 program go to the command line and type
> python gridworld.py [test.csv] [movecost] [probability of successful move]

Where test.csv is the grid world you want it to solve, the move cost is the
cost per move (should be a negative number), and probability of successful move
is the probability to make a correct move.

To run the Part 3 program go to the command line and type
> python truck.py [truck_capacity] [road_length] [start_penalty] [time_limit]

Where truck_capacity is the maximum number of packages the truck can hold, road_length
is the length of the road (or number of houses on the road), start_penalty is the penalty
for starting to deliver from the warehouse when there are no packages in the truck (should
be a negative number), and time_limit is the number of ticks to run for (-1 for infinite
time until program converges).