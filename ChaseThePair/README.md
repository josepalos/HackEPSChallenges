# Chase The Pair Challenge by HackEPS2019

## Description

To solve this problem the first approach was to sort the numbers in the set,
and then do a binary search in this sorted list to find the closes numbers to
the point where the chasen value should be found. This had a worst case cost of
O(n log(n)) due to the sorting step. As we have to iterate the vector, and we
have a way to give an score for each element in an independent way (the
distance of its value to the chasen value) we don't need to sort the set, as we
can just keep track of the closest number we have found so far (with its
distance), and update it if we find something better. Thus, in just one
iteration of the set, we can find the closest value in the set.

## Information

- Group name: LoneWolves
- Time cost: O(n)
- Space cost: O(1) for version 1, O(n) for version 2.
- Time expend: 0.496549 seconds 
- Sets size: 100.000.000 (the biggest set that could be generated using the
available system)

Output of the solver
STATISTICS
Loading time:		9.426174
Chasing vector 1:	0.243098
Chasing vector 2:	0.241900
Total Chasing time:	0.496549
Total time:		9.922723

**Note** that the times were found using the version 2 of the solver, to
separate between solving time and loading time.


## Usage
### Version 1

This version solves the problem while reading the file, so there is no
disctinction between the loading time and the solving time.

To generate this version use:
```{bash}
$ make chase
```

Use this version as following:
```{bash}
$ ./chase <value> <sets_file>
```

### Version 2

This version loads the vectors in an array, and then they are solved using the
procedure explained before.

To generate this version use:
```{bash}
$ make chase2
```

Use this version as following:
```{bash}
$ ./chase2 <value> <sets_file>
```

## Extra

Use the tool "visualize_costs.py" to get the plot of the time spent for solving
the problem for different sizes. It requires the version 2 of the solver.

## TODO

- [ ] Add legend to "visualize_costs.py"
- [ ] Chase different numbers in "visualize_costs.py"
- [ ] Test if loading the entire file in memory the time between loading and
solving can be differentiated in version 1.
