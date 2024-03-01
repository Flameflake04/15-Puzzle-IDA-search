Coding assignment: Iterative-deepening-search
Author: Duc Tran
The program helps user solved 16-puzzle by using 2 methods of IDA*. The program is written in Python.
To run the code, use latest version of Visual Studio Code, install Python 3.11.8 and install necessary library like time, psutil
System: Window 11
Python version: 3.11.8

We see that IDA* Manhattan Distance and IDA* Misplayed Tiles run usually slower than the normal A* version (due to repeated node by iterative deepening), but the two method will save memory more than the 2 normal A* version