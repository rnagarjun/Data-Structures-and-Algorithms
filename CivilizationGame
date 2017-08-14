/**
 * Name: Nagarjun Ratnesh
 * UTorid: ratneshn
 * CSCB63 Assignment Question #4
 */
package tile;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Reach {
	// Global Variable Declaration
	private static TileInfo[] board;
	private static Set<Integer> possibleSpots;
	
	public static List<Integer> reach(int speed, int start, TileInfo[] tileinfo) {
		// Initialization of variables
		board = tileinfo;
		possibleSpots = new HashSet<>();
		int[] units = tileinfo[start].adjlist;
		
		// Call possibleUnit method
		possibleUnit(units, speed+tileinfo[start].cost, start);
		List<Integer> possibleUnits = new ArrayList<Integer>();
		possibleUnits.addAll(possibleSpots);
		return possibleUnits;
	}

	/**
	 * Recursively checks if the possible unit is valid or not
	 * @param units
	 * @param updatedSpeed
	 * @param updatedStart
	 */
	public static void possibleUnit(int[] units, int updatedSpeed, int updatedStart){
		// Base case: if the speed is <=0 or if the given list is empty
		if ((updatedSpeed <= 0)|| units == null){
			// end recursion
		}else {
			int tileSpeed = board[updatedStart].cost;
			//Check after visiting a possible unit if there is more speed left to spent
			if ((updatedSpeed-tileSpeed) >= 0){
				possibleSpots.add(updatedStart);
				// For every other units adjacent to current unit
				for(int i =0; i < units.length; i++){
					// recursively check each unit
					possibleUnit(board[units[i]].adjlist, updatedSpeed-tileSpeed, units[i]);
					}
		     }
		}
	}
}
