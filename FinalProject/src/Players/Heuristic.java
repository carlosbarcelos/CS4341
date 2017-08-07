package Players;

import Utilities.StateTree;

public class Heuristic {
	private int col; // The Y position of the desired move
	private int row; // The X position of the desired move
	private StateTree board; // The board on which to make th emove
	private int turn; // The turn number (for asking questions about piece number)

	public Heuristic(int col, int row, StateTree board, int turn){
		this.col = col;
		this.row = row;
		this.board = board;
		this.turn = turn;
	}

	// Returns the heuristic value of a move on a position
	public int offensiveHeuristic(){

		int downScore = 0;
		int leftScore = 0;
		int rightScore = 0;
		int urDiagScore = 0;
		int dlDiagScore = 0;
		int ulDiagScore = 0;
		int drDiagScore = 0;

		// Check for how many in a row we have
		// Check vertical opportunity
		int i = row;
		int j = col;
		while(true){ // Check down
			try{
				if(board.getBoardMatrix()[i][j-1] != turn){
					break;
				} else{
					downScore++;
					j--; // Move down
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}

		i = row;
		j = col;
		while(true){ // Check left
			try{
				if(board.getBoardMatrix()[i-1][j] != turn){
					break;
				} else{
					leftScore++;
					i--; // Move left
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;

			}
		}
		i = row;
		j = col;
		while(true){ // Check right
			try{
				if(board.getBoardMatrix()[i+1][j] != turn){
					break;
				} else{
					rightScore++;
					i++; // Move right
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}
		i = row;
		j = col;
		while(true){ // Check up right diag
			try{
				if(board.getBoardMatrix()[i+1][j+1] != turn){
					break;
				} else{
					urDiagScore++;
					i++; // Move right
					j++; // Move up
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}
		i = row;
		j = col;
		while(true){ // Check down left diag
			try{
				if(board.getBoardMatrix()[i-1][j-1] != turn){
					break;
				} else{
					dlDiagScore++;
					i--; // Move left
					j--; // Move down
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}
		i = row;
		j = col;
		while(true){ // Check up left diag
			try{
				if(board.getBoardMatrix()[i-1][j+1] != turn){
					break;
				} else{
					ulDiagScore++;
					i--; // Move left
					j++; // Move up 
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}
		i = row;
		j = col;
		while(true){ // Check down right diag
			try{
				if(board.getBoardMatrix()[i+1][j-1] != turn){
					break;
				} else{
					drDiagScore++;
					i++; // Move right 
					j--; // Move down
				}
			}catch (IndexOutOfBoundsException e) {
				// Ran out of board to check
				break;
			}
		}

		// Calculate vertical opportunity
		int vertical = downScore + 1;
		//System.out.println("  vertical Opportunity     = " + Integer.toString(vertical));
		// Calculate horizontal opportunity
		int horizontal = leftScore + rightScore + 1;
		//System.out.println("  horizontal Opportunity   = " + Integer.toString(horizontal));
		// Calculate forward diagonal opportunity
		int forwardDiag = dlDiagScore + urDiagScore + 1;
		//System.out.println("  forwardDiag Opportunity  = " + Integer.toString(forwardDiag));
		// Calculate backward diagonal opportunity
		int backwardDiag = ulDiagScore + drDiagScore + 1;
		//System.out.println("  backwardDiag Opportunity = " + Integer.toString(backwardDiag));
		//System.out.println("");


		// Calculates scoring opportunity score
		int opportunityScore = 0;
		int[] scoreArray = {vertical, horizontal, forwardDiag, backwardDiag};
		for (int s: scoreArray) {
			if(s >= board.winNumber){
				opportunityScore += Math.pow(10, board.winNumber);
			} else{
				opportunityScore += 25 * s;
			} // The intersection of these two curves is ~1.6. A board will never be that small
		}

		// Calculates distance from center score
		int midPoint = (board.columns - 1)/2; // The middle column
		int delta = Math.abs(col - midPoint); // How far this column is from the middle
		int columnScore = board.columns - midPoint - delta;


		//return score
		return opportunityScore + columnScore;
	}

	// Defensive heuristic
	public int defensiveHeuristic(){
		//TODO
		return 0;
	}
	// Hybrid heuristic
	public int hybridHeuristic(){
		//TODO
		return 0;
	}
	// Opportunity heuristic - trys to get as many scoring opportunities for the next move
	public int opportunityHeuristic(){
		//TODO
		return 0;
	}
}