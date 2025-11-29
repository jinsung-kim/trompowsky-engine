<img width="512" alt="chess" src="https://github.com/user-attachments/assets/e59057e5-4eec-47f2-83ac-3b75fd8f2ff9">


The Trompowsky Engine is my rendition of a chess engine built pretty much from scratch, with the exception of the _pygame_ import.

##### Methodology
The AI itself is rather simple. In fact, if you sift through the code, most of it consists of tests to ensure the correctness of the game, and the rest is the code that generates moves. The AI itself is really primitive. Given that chess is generally a zero-sum game, the main algorithm is basically just an implementation of the minimax game theory with some optimizations along the way:

1. Generate all of the valid moves given the current state of the board.
2. Score each move and generate a response move from the opposing side. Each piece is scored by its traditional score, with a positional move bonus given based on where it's located on the board.
3. Repeat this process until depth is 0. Note that I used the alpha-beta pruning technique to eliminate sub-optimal game states.
4. Return the most optimal move and execute it.

Strengthening the AI requires setting the depth to a higher value.
- At zero, the AI will basically make pseudo-random moves.
- At one, the AI will take pieces that are available without thinking about what might come next.
- At two, the AI will aim to take pieces that are available while considering the net cost of the opposing piece that might react based on the move.
- Anything beyond this just tries to create the most optimal position.
  Note: While higher depths are great for strengthening the brainpower of the AI, it also takes exponentially more time to generate moves, given that each move opens up a whole new set of opposing moves to consider.
 
##### Testing
Testing was a critical part of the development cycle. This was one of the first projects where I wrote unit test cases before writing out the functionality. I did this to ensure that I would not waste too much time debugging (it happened anyway). The sanity checking saved a lot of time but still needs work to capture the overall game flow and edge cases. To run the tests, simply run: `python3 tests/run_tests.py`.

##### TODOs
- [ ] Support castling, en passant
- [ ] Support under promotion
- [ ] The ability to undo moves
- [ ] A more comprehensive UI that displays game state and the move log
- [ ] More test cases, particularly the ability to test the actual game state
- [ ] Ability for someone else to play as the black pieces
- [ ] Multithreaded move generation to speed up the AI
- [ ] Ability to input a game log to restore and continue at that state of the game
- [ ] Compare this engine with other engines
- [ ] Rewrite using bitmasks?

