package Players;

import java.util.ArrayList;
import java.util.List;

import Utilities.*;


public class Decisions {

  private StateTree board;
  public int turn;
  public int opponent;
  public int depth;
  
  public Decisions(StateTree board, int turn, int depth){
    this.board = board;
    this.turn = turn;
    this.opponent = getOpponent();
    this.depth = depth;
  }
  
  //TODO Iterative deepening
  
  // Minimax intelligent game playing
  public Move alphaBeta(){
    int bestUtility = Integer.MIN_VALUE;
    int alpha = Integer.MIN_VALUE;
    int beta = Integer.MAX_VALUE;
    int thisUtility = 0;
    int row;
    Move move;
    Move bestMove = null;
    StateTree newBoard;
    Heuristic heuristic;   
    int myDepth;
    
    // Create list of Moves
    List<Move> moves = new ArrayList<Move>();
	Move newMove;
    int col;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false,col);
      if (board.validMove(newMove)){
       moves.add(newMove);
      }
    }
    
    System.out.println("Created " + Integer.toString(moves.size()) + " moves.");
    
    // Run the moves over min/max
    for(int i=0; i < moves.size(); i++){
      move = (Move) moves.get(i);
      newBoard = board.copy();
      row = newBoard.getRow(move);
      heuristic = new Heuristic(move.getColumn(),row, newBoard, this.turn);
    
      //System.out.println("Player: " + Integer.toString(turn) + "Heuristic of " + move + " = " + Integer.toString(heuristic.getValue()));

      newBoard.makeMove(move);
      myDepth = this.depth;
      thisUtility = ab_max_value(newBoard, myDepth, heuristic.offensiveHeuristic(), alpha, beta);
      System.out.println("Heuristic of " + move + " = " + Integer.toString(thisUtility));
      if(thisUtility > bestUtility){
      	bestUtility = thisUtility;
        bestMove = move;	
      }
    }
      return bestMove;   
  }
  
  // minimax helper: min function | Opponent
  private int ab_min_value(StateTree newBoard, int depth, int utility, int alpha, int beta){    
		// If terminal
    if(depth == 0){
      return utility;
    }
    // Create list of Moves
    Heuristic heuristic;
    List<Move> moves = new ArrayList<Move>();
    Move newMove;
    StateTree newNewBoard;
    int col, row;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false, col);
      if (newBoard.validMove(newMove)){
       moves.add(newMove);
      }
    }    
   // Run the moves over max
    int minUtility = Integer.MAX_VALUE;
    int thisUtility = 0;
    Move move;
    for(int i=0; i < moves.size(); i++){
        move = (Move) moves.get(i);
        newNewBoard = newBoard.copy();
      row = newBoard.getRow(move);
      heuristic = new Heuristic( move.getColumn(),row, newBoard, this.opponent);
      newNewBoard.makeMove(move);
      
      thisUtility = ab_max_value(newNewBoard, depth-1, heuristic.offensiveHeuristic(), alpha, beta);
      if(thisUtility < minUtility){
      	minUtility = thisUtility;
      }
      if(thisUtility <= alpha){
          return thisUtility;
        }
        beta = Math.min(beta, thisUtility);
    }
    //System.out.println("  minUtility = " + Integer.toString(minUtility));           
    return minUtility;
  }
  
  // minimax helper: max function
  private int ab_max_value(StateTree newBoard, int depth, int utility, int alpha, int beta){ 
    // If terminal
    if(depth == 0){
      return utility;
    }
    // Create list of Moves
    Heuristic heuristic;
    List<Move> moves = new ArrayList<Move>();
    Move newMove;
    int col;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false, col);
      if (newBoard.validMove(newMove)){
       moves.add(newMove);
      }
    }
   // Run the moves over max | Turn
    int maxUtility = Integer.MIN_VALUE;
    int thisUtility = 0;
    int row;
    Move move;
    StateTree newNewBoard;
    for(int i=0; i < moves.size(); i++){
        move = (Move) moves.get(i);
        newNewBoard = newBoard.copy();
      row = newBoard.getRow(move);
      heuristic = new Heuristic( move.getColumn(),row, newBoard, this.turn);
      newNewBoard.makeMove(move);
      
      thisUtility = ab_min_value(newNewBoard, depth-1, heuristic.offensiveHeuristic(), alpha, beta);
      if(thisUtility > maxUtility){
      	maxUtility = thisUtility;
      }
      if(thisUtility >= beta){
          return thisUtility;
        }
        alpha = Math.max(alpha, thisUtility);
    }
    //System.out.println("  maxUtility = " + Integer.toString(maxUtility));     
    return maxUtility;
  }
  
/* Minimax and related parts */
  public int miniMax_helper(StateTree board, int player, int depth){
	  // Terminal state
	  if(depth == 0 || board.isFull()){
		  return new Heuristic(board.lastColumn, board.lastRow, board, player).offensiveHeuristic();
	  }
	  // Maximizing player
	  if(player == this.turn){
		  List<Move> moves = new ArrayList<Move>();
		  int max_bestValue = Integer.MIN_VALUE;
		  // Build the children
		    for (int i = 0; i < board.columns; i++) {
		        Move newMove = new Move(false,i);
		        if (board.validMove(newMove)){
		         moves.add(newMove);
		        }
		      }
		    
		    // For each child of the node
		    int value;
		    for(int k=0; k < moves.size(); k++){
		    	StateTree newBoard = board.copy();
		    	newBoard.makeMove(moves.get(k));
		    	value = miniMax_helper(newBoard, this.opponent, depth-1);
		    	max_bestValue = Math.max(value, max_bestValue);
		    }
		    return max_bestValue;
	  }
	  
	  // Minimizing player
	  else{
		  int min_bestValue = Integer.MAX_VALUE;
		  List<Move> moves = new ArrayList<Move>();
		  // Build the children
		    for (int i = 0; i < board.columns; i++) {
		        Move newMove = new Move(false,i);
		        if (board.validMove(newMove)){
		         moves.add(newMove);
		        }
		      }
		    
		    // For each child of the node
		    int value;
		    for(int h =0 ; h < moves.size(); h++){
		    	StateTree newBoard = board.copy();
		    	newBoard.makeMove(moves.get(h));
		    	value = miniMax_helper(newBoard, this.turn, depth-1);
		    	min_bestValue = Math.min(value, min_bestValue);
		    }
		    return min_bestValue;
	  }		
  }
  
  
  
/*  // Minimax intelligent game playing */
  public Move miniMax(){
    int bestUtility = Integer.MIN_VALUE;
    int thisUtility = 0;
    int row;
    Move move = null;
    Move bestMove = null;
    StateTree newBoard;
    Heuristic heuristic;
    
    // Create list of Moves
    List<Move> moves = new ArrayList<Move>();
	Move newMove;
    int col;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false,col);
      if (board.validMove(newMove)){
       moves.add(newMove);
      } else{
    	  System.out.println("This move is not valid");
      }
    }

    //System.out.println("Created " + Integer.toString(moves.size()) + " moves.");
    
    // Run the moves over min/max
    for(int i=0; i < moves.size(); i++){
      move = (Move) moves.get(i);
      newBoard = board.copy();   // Make a board at this state 
      newBoard.makeMove(move);   // Make the move on the new board
      col = newBoard.lastColumn; // Record the column of the last move
      row = newBoard.lastRow;    // Record the row of the last move
      System.out.println("Column: " + Integer.toString(col) + " Row: " + Integer.toString(row));

      //heuristic = new Heuristic(move.getColumn(), row, newBoard, this.opponent);
      //System.out.println("Player: " + Integer.toString(turn) + "Heuristic of " + move + " = " + Integer.toString(heuristic.getValue()));

      thisUtility = miniMax_helper(newBoard, this.turn, this.depth);
      System.out.println("Utility of " + move + " = " + Integer.toString(thisUtility));
      if(thisUtility > bestUtility){
      	bestUtility = thisUtility;
        bestMove = move;	
      }
    }
      return bestMove;   
  }
  
  // minimax helper: min function | Opponent
  private int min_value(StateTree newBoard, int depth, int utility){    
		// If terminal
    if(depth == 0){
      return utility;
    }
    // Create list of Moves
    Heuristic heuristic;
    List<Move> moves = new ArrayList<Move>();
    Move newMove;
    StateTree newNewBoard;
    int col, row;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false, col);
      if (newBoard.validMove(newMove)){
       moves.add(newMove);
      }
    }    
   // Run the moves over max
    int minUtility = Integer.MAX_VALUE;
    int thisUtility = 0;
    Move move;
    for(int i=0; i < moves.size(); i++){
        move = (Move) moves.get(i);
        newNewBoard = newBoard.copy();
      row = newBoard.getRow(move);
      newNewBoard.makeMove(move);

      heuristic = new Heuristic(move.getColumn(), row, newBoard, this.turn);
      
      thisUtility = max_value(newNewBoard, depth, heuristic.offensiveHeuristic());
      if(thisUtility < minUtility){
      	minUtility = thisUtility;
      }
    }
    //System.out.println("  minUtility = " + Integer.toString(minUtility));           
    return minUtility;
  }
  
  // minimax helper: max function
  private int max_value(StateTree newBoard, int depth, int utility){ 
//    // If terminal
//    if(depth == 0){
//      return utility;
//    }
    // Create list of Moves
    Heuristic heuristic;
    List<Move> moves = new ArrayList<Move>();
    Move newMove;
    int col;
    for (col = 0; col < board.columns; col++) {
      newMove = new Move(false, col);
      if (newBoard.validMove(newMove)){
       moves.add(newMove);
      }
    }
   // Run the moves over max | Turn
    int maxUtility = Integer.MIN_VALUE;
    int thisUtility = 0;
    int row;
    Move move;
    StateTree newNewBoard;
    for(int i=0; i < moves.size(); i++){
        move = (Move) moves.get(i);
        newNewBoard = newBoard.copy();
      row = newBoard.getRow(move);
      newNewBoard.makeMove(move);

      heuristic = new Heuristic(move.getColumn(), row, newBoard, this.opponent);
      
      thisUtility = min_value(newNewBoard, depth-1, heuristic.offensiveHeuristic());
      if(thisUtility > maxUtility){
      	maxUtility = thisUtility;
      }
    }
    //System.out.println("  maxUtility = " + Integer.toString(maxUtility));     
    return maxUtility;
  }
  
  // Returns the best move on this board (unintelligently)
  public Move Max(StateTree newBoard){
    int bestJ = 0;
		int bestScore = 0;
		for(int j=0; j<newBoard.columns; j++){
			for(int i=0; i<newBoard.rows; i++){
				if(newBoard.getBoardMatrix()[i][j] == 0){
					Heuristic test = new Heuristic(j, i, newBoard, turn);
					if (bestScore < test.offensiveHeuristic()){
						bestJ = j;
						bestScore = test.offensiveHeuristic();
					}
					//System.out.println(test.getValue());
				}			
		}
	}
    return new Move(false, bestJ);
  }
  
  // Returns the worst move on this board (unintelligently)
  public int Min(StateTree newBoard){
  	int worstJ = 0;
		int worstScore = 0;
		for(int j=0; j<newBoard.columns; j++)
		{
			for(int i=0; i<newBoard.rows; i++)
			{
				if(newBoard.getBoardMatrix()[i][j] == 0)
				{
					Heuristic test = new Heuristic(j, i, newBoard, turn);
					if (worstScore > test.offensiveHeuristic()){
						worstJ = j;
						worstScore = test.offensiveHeuristic();
					}
					System.out.println(test.offensiveHeuristic());
				}			
		}
	}
	return worstJ;
  }
  
  // Returns the opponent's turn number
  private int getOpponent(){
    if(this.turn == 1)
      return 2;
    return 1;
  }
}