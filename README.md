# Practicum 1 on Formal Languages
### variant XI
Finds length of the shortest string with k chars x.
An automat is built from a string..
#### 3 stacks are used:
1 for chars. They added till ' . ' or ' \* ' or' + ' appears
2 and 3 for left and right pointers. 
###
#### if ' . ':
A new node is added right pointer is moved
#### if ' \* ':
Path on 1 is added from left node to right and vice versa.
If branch does not include x, cicle is not made.
#### if ' + ':
If it is a char a new branch is created.
It unites 2 branches made on previous steps.
 
After that bfs goes through the automat and searches for the string. 

P.S.
Given data is checked for validity in decorator.
'#' represents the end of string
unittest library is used
