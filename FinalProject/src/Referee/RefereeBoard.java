package Referee;

import Utilities.StateTree;

/**
 * This is a simple state that just keeps track of the board and whose
 * turn it is. The referee uses this board to keep track of things
 * and check if anybody has won.
 * 
 * @author Ethan Prihar
 *
 */

public class RefereeBoard extends StateTree
{
	public RefereeBoard(int r, int c, int w, int t, boolean p1, boolean p2, StateTree p)
	{
		super(r, c, w, t, p1, p2, p);
	}
	
	public RefereeBoard copy(){
		RefereeBoard newBoard = new RefereeBoard(this.rows, this.columns, this.winNumber, this.turn, false, false, null);
		newBoard.setOut(System.out);
		for (int i = 0; i < newBoard.columns; i++){
			for (int j = 0; j < newBoard.rows; j++){
				newBoard.getBoardMatrix()[j][i] = this.getBoardMatrix()[j][i];
			}
		}
		return newBoard;
	}
}
