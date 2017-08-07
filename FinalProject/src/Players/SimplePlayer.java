package Players;

import Utilities.Move;
import Utilities.StateTree;


/**
 * This is an example of how to make a player.
 * This player is extremely simple and does no tree building
 * but its good to test against at first.
 * 
 * @author Ethan Prihar
 *
 */
public class SimplePlayer extends Player
{
	public SimplePlayer(String n, int t, int l, int alg)
	{
		super(n, t, l, alg);
	}

	public Move getMove(StateTree state){
	int bestJ = 0;
	int bestScore = 0;
	
	/*
	int expectedUtility = decision.miniMax_helper(state, 2, 0);
	System.out.println("  Expected utility = " + Integer.toString(expectedUtility));
	*/
	
	//Decisions decision = new Decisions(state, 2, 4);	
	//Move m = decision.miniMax();
	//Move m = decision.Max(state);
	//return m;
	
	for(int j=0; j<state.columns; j++)
	{
		for(int i=0; i<state.rows; i++)
		{
			//System.out.println("Iterations: Column=" + Integer.toString(i) + ", Row= " + Integer.toString(j));
			if(state.getBoardMatrix()[i][j] == 0)
			{
				Heuristic test = new Heuristic(j, i, state, 2);
				if (bestScore < test.offensiveHeuristic()){
					bestJ = j;
					bestScore = test.offensiveHeuristic();
				}
				//System.out.println(test.getValue());
			}
			//Connor is sitting next to me
//			try{Thread.sleep(15000);}
//			catch(InterruptedException ex){Thread.currentThread().interrupt();}
			
//			if(this.turn == 1)
//				return new Move(false, 0);
//			if(this.turn == 2)
//				return new Move(false, 1);	
		}
		
//		if((this.turn == 1 && !state.pop1) || (this.turn == 2 && !state.pop2))
//		{
//			return new Move(true, 0);	
//		}
		
	} 
	return new Move(false, bestJ);
	
}
}