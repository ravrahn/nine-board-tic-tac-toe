# COMP3411 Project 3 - Nine-Board Tic Tac Toe
##### Due: Sunday 1 June, 11:59 pm 
##### Marks: 12% of final assessment

### Introduction
In this project you will be writing an agent to play the game of Nine-Board Tic-Tac-Toe.
This game is played on a 3 x 3 array of 3 x 3 Tic-Tac-Toe boards. The first move is made by placing an `X` in a randomly chosen cell of a randomly chosen board. After that, the two players take turns placing an `O` or `X` alternately into an empty cell of the board corresponding to the cell of the previous move. (For example, if the previous move was into the upper right corner of a board, the next move must be made into the upper right board.)

The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards. If a player is unable to make their move (because the relevant board is already full) the game ends in a draw.

### Getting Started
Copy the archive [src.zip](http://www.cse.unsw.edu.au/~cs3411/14s1/hw3/src.zip) into your own filespace and unzip it. Then type

```bash
cd src
make all
```

```bash
./servt9 -x -o
```

You should see something like this:

```
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . . | . . .
 ------+-------+------
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . x | . . .
 ------+-------+------
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . . | . . .
 next move for O ?
```
You can now play Nine-Board Tic-Tac-Toe against yourself, by typing a number for each move. 
The cells in each board are numbered 1, 2, 3, 4, 5, 6, 7, 8, 9 as follows:

```
+-----+
|1 2 3|
|4 5 6|
|7 8 9|
+-----+
```

To play against a computer player, you need to open another terminal window (and `cd` to the `src` directory).

Type this into the first window:

```bash
./servt9 -p 12345 -x
```

This tells the server to use port `12345` for communication, and that the moves for `X` will be chosen by you, the human, typing at the keyboard. (If port `12345` is busy, choose another 5-digit number.)

You should then type this into the second window (using the same port number):

```bash
./randt9 -p 12345
```

The program `randt9` simply chooses each move randomly among the available legal moves.
The Prolog program `random.pl` behaves in exactly the same way. You can play against it by typing this into the second window:

```bash
prolog 12345 < agent.wrap
```

You can play against a slightly more sophisticated player by typing this into the second window:

```bash
./lookt9 -p 12345
```

To play two computer programs against each other, you may need to open three windows. For example, to play agent against lookt9 using port 54321, type as follows:

+ window 1: `./servt9 -p 54321`
+ window 2: `./agent -p 54321`
+ window 3: `./lookt9 -p 54321`

(Whichever program connects first will play `X`; the other program will play `O`.)
Alternatively, you can launch all three programs from a single window by typing

```bash
./servt9 -p 54321 &
./agent  -p 54321 &
./lookt9 -p 54321
```

or, using a shell script:

```bash
./playc.sh 54321 lookt9
```
The server communicates with the player(s) using the commands `init`, `start()`, `second_move()`, `third_move()`, `last_move()`, `win()`, `loss()`, `draw()` and `end()`, as illustrated by this brief example:

| Player X |                      | Server |                     | Player O |
|----------|----------------------|--------|---------------------|----------|
|          | ←`init`              |        |                     |          |
|          |                      |        | `init`→             |          |
|          | ←`start(x)`          |        |                     |          |
|          |                      |        | `start(o)`→         |          |
|          |                      |        | `second_move(6,1)`→ |          |
|          |                      |        | ←`9`                |          |
|          | ←`third_move(6,1,6)` |        |                     |          |
|          | `9`→                 |        |                     |          |
|          |                      |        | `next_move(9)`→     |          |
|          |                      |        | ←`6`                |          |
|          | ←`next_move(6)`      |        |                     |          |
|          | `5`→                 |        |                     |          |
|          |                      |        | `last_move(5)`→     |          |
|          | ←`win(triple)`       |        |                     |          |
|          |                      |        | `loss(triple)`→     |          |
|          | ←`end`               |        |                     |          |
|          |                      |        | `end`→              |          |

You are free to write your player in any language you wish.

If you choose to write in C, your program will be invoked like this:

```bash
./agent -p (port)
```

You should submit your source files (no object files) as well as a `Makefile` which, when invoked with the command "`make`", will produce an executable called agent . Feel free to use the supplied files as a starting point (especially `agent.c` which is identical to `randt9.c`)

If you choose to write in Prolog, your program will be invoked like this:

```bash
prolog (port) < agent.wrap
```
You should submit your `.pl` files (including `agent.pl`). Feel free to use `agent.pl` (identical to `randt9.pl`) as a starting point, as well as `alphabeta.pl` (which implements alpha-beta search for regular Tic-Tac-Toe).

If you write in Java, your program will be invoked by

```bash
java Agent -p (port)
```
You should submit your `.java` files (no `.class` files). The main file must be called `Agent.java`

If you wish to write in some other language, let me know.

### Question
At the top of your code, in a block of comments, you must provide a brief answer (one or two paragraphs) to this Question:

> Briefly describe how your program works, including any algorithms and data structures employed, and explain any design decisions you made along the way.

### Groups
This assignment may be done individually, or in groups of two students. Each group should send an email to `blair@cse` by Sunday 18 May, indicating the names of the group members (or just your own name, if you intend to do the project individually).

### Submission

COMP3411 students should submit by typing

```bash
give cs3411 hw3 ...
```

COMP9414/9814 students should submit by typing

```bash
give cs9414 hw3 ...
```

You can submit as many times as you like - later submissions will overwrite earlier ones. You can check that your submission has been received by using the following command:

```bash
3411 classrun -check
9414 classrun -check
```

The submission deadline is Sunday 1 June, 11:59 pm.
15% penalty will be applied to the (maximum) mark for every 24 hours late after the deadline.

Additional information may be found in the [FAQ](http://www.cse.unsw.edu.au/~cs3411/14s1/hw3/faq.shtml) and will be considered as part of the specification for the project.

Questions relating to the project can also be posted to the MessageBoard on the course Web page.

If you have a question that has not already been answered on the FAQ or the MessageBoard, you can email it to your tutor, or to `cs3411.hw3@cse.unsw.edu.au`

### Marking Sceme
+ 7 marks for performance against a number of pre-defined opponents.
+ 5 marks for Algorithms, Style, Comments and answer to the Question

You should always adhere to good coding practices and style. In general, a program that attempts a substantial part of the job but does that part correctly will receive more marks than one attempting to do the entire job but with many errors.

### Plagiarism Policy

Your program must be entirely your own work. Plagiarism detection software will be used to compare all submissions pairwise and serious penalties will be applied, particularly in the case of repeat offences.

**DO NOT COPY FROM OTHERS; DO NOT ALLOW ANYONE TO SEE YOUR CODE**

Please refer to the [Yellow Form](http://www.cse.unsw.edu.au/~studentoffice/policies/yellowform.html), or the [CSE Addendum](http://www.cse.unsw.edu.au/~chak/plagiarism) to the [UNSW Plagiarism Policy](https://student.unsw.edu.au/plagiarism) if you require further clarification on this matter.

Good luck! 