package Referee;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import Players.*;

public class RunReferee {

	public static void main(String[] args) {
		
		// Match parameter
		// You can modify them
		int timeLimit = 10000;
		int boardRows = 8;
		int boardColumns = 9;
		int winNumber = 5;
		int battleDurationLimit = 3600;
		// End of modifications
		
		
		
		//Player player1 = (Player) new Human("Human", 1, timeLimit, 1);
		Player player1 = (Player) new SimplePlayer("CPU 1", 1, timeLimit, 1);
		Player player2 = (Player) new SimplePlayer2("CPU 2", 2, timeLimit, 1);

		Referee referee = new Referee();
		referee.setOut(System.out);
		referee.initMatch(boardRows, boardColumns, winNumber, timeLimit, player1, player2);
		Callable<Object> judge1 = new Callable<Object>() {
		 	public Object call() {
			  return referee.judge();
		 	}
		};			
		ExecutorService service = Executors.newSingleThreadExecutor();
		
		final Future<Object> future1 = service.submit(judge1);
		int result = -1;
		try {
			result = (int) future1.get(battleDurationLimit, TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		} catch (TimeoutException e) {
			e.printStackTrace();
		}
		System.out.println(result);
	}
}
