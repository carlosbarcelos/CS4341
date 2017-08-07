package Players;

import java.util.Scanner;

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
public class Human extends Player
{
	public Human(String n, int t, int l, int alg)
	{
		super(n, t, l, alg);
	}

	public Move getMove(StateTree state)
	{
		
		int column = getColumn();
		
		return new Move(false, column);
		
	}
	
	public int getColumn(){
		
		Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("Enter the column you'd like to place your piece in: ");
            String input = sc.next();
            int intInputValue = 0;
            try {
                intInputValue = Integer.parseInt(input);
                if(intInputValue < 0 || intInputValue > 8){
                	System.out.println("You must enter a number between from 0 to 8.");
                } else {
                	System.out.println("Attempting to place piece...");
                	return intInputValue;
                }
            } catch (NumberFormatException ne) {
                System.out.println("Input is not a number, try again.");
            }
        }
		
	}
}