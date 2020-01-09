/**
 * Name: Nagarjun Ratnesh
 * Student#1002280195
 * Utorid:ratneshn
 * Title: Assignment 2 Question 4(CSCB63)
 * 8-Puzzle Solver - Dijktra Algorithm
 */
package sbp;

import java.util.*;

class Sliding {
	// Initiation of constants and static global variables
	private static boolean SOLVABLE;
	// Queue to Implemented using LinkedList for Storing All the Nodes in BPS.
	Queue<String> q = new LinkedList<String>(); 
	private static String puzzleTarget = "ABCDEFGH ";	// Target puzzle
	private static String puzzleStart;	// Starting puzzle
	static Sliding puzzle; 
	static Sliding.DirectedGraph<String> graph; // The solution of the puzzle in graph form
	static HashMap<String, ArrayList<String>> movesTree; // A tree in a form of hashmap with solution
	
	/**
	 * Takes in value and returns the key that contains the value
	 * @param value
	 * @return
	 */
	public static String getKeyByValue(String value) {
		String toReturn = null;
		for (String key : movesTree.keySet()) {
		    if (movesTree.get(key).contains(value)){
		    	toReturn = key;
		    }
		}
		return toReturn;
	}

	/**
	 * The main method of the class
	 * @param start
	 * @return
	 */
	public static Iterator<String> solve(String start) {
		// Declaration of Variables
		puzzle = new Sliding(); 
		graph = puzzle.new DirectedGraph<String>();
		movesTree = new HashMap<String, ArrayList<String>>();
		SOLVABLE = false;
		puzzleStart = start;
		solution(start);

		// returns true is the puzzle is solvable
		if(!SOLVABLE){
			return null;

		}else{
			ArrayList<String> finished = new ArrayList<String>(); //A final arrayList containing the shortest path.
			String firstOne = puzzleTarget;
			while(firstOne.compareTo(puzzleStart)!=0){
				finished.add(0, firstOne);
				firstOne=getKeyByValue(firstOne);
			}
			return finished.iterator(); // returns the iterator of the shortest path
		}
	}

	/**
	 * Tries to solve the puzzle 
	 * @param start
	 */
	public static void solution(String start){
		puzzle.add(start, "start"); // Simply adding the begin state

		while(puzzle.q.peek()!=null){
			puzzle.moveUp(puzzle.q.peek()); 
			puzzle.moveDown(puzzle.q.peek()); 
			puzzle.moveLeft(puzzle.q.peek());
			puzzle.moveRight(puzzle.q.remove()); 
		}
	}

	// A class representation of a directed Graph
	public class DirectedGraph<V> {
		// HashMap that represents and adjacency list
		private Map<V,LinkedList<V>> moves = new HashMap<V,LinkedList<V>>();

		/**
		 * Adds vertex
		 * @param move
		 */
		public void add (V move) {
			if (moves.containsKey(move)) return;
			moves.put(move, new LinkedList<V>());  
			}

		/**
		 * Checks if the graph contains the vertex
		 * @param move
		 * @return
		 */
		public boolean contains(V move){
			if(moves.containsKey(move)){
				return true;
			}else{
				return false;
				}
		  }

		/**
		 * Adds edge
		 * @param from
		 * @param to
		 */
		public void add (V from, V to) {
			this.add(from); 
			this.add(to);
		    moves.get(from).add(to);
		    }

		 // prints BFS traversal from a given source "starting"
		public void BFS(String starting){ 
			// Keeps track of visited nodes
			Map<String, Boolean> visited = new HashMap<String, Boolean>();
			// Create a queue for BFS
			LinkedList<String> queue = new LinkedList<String>();
		 
			// Mark the current node as visited and enqueue it
			visited.put(starting, true);
			queue.add(starting);
		 
			// While the queue is not empty
			while (queue.size() != 0){
				starting = queue.poll();
				Iterator<String> i = (Iterator<String>) this.moves.get(starting).listIterator();
				while (i.hasNext()){	
					String n = i.next();
					// If a adjacent has not been visited, then mark it
					if (!visited.containsKey(n)){ 
						if (movesTree.containsKey(starting)){
							movesTree.get(starting).add(n);
						}else{
							ArrayList<String> m = new ArrayList<String>();
		                	movesTree.put(starting, m);
		                	movesTree.get(starting).add(n);
		                }
						// visited and enqueue it
		                visited.put(starting, true);
		                queue.add(n);
		                }
		            }
		        }
		    }
		}

	/**
	 * Add to the graph and the queue
	 * @param curr
	 * @param from
	 */
	public void add(String to, String from){
		if(!graph.contains(to)){
			graph.add(from, to);
			q.add(to);
		}
	}
	
	/**
	 * Move left
	 * @param curr
	 */
	public void moveLeft(String curr){
	int positionBlank = curr.indexOf(" ");
	String from = curr;
	if(positionBlank!=0 && positionBlank!=3 && positionBlank!=6){

		String moved = curr.substring(0, positionBlank-1)+" "+curr.charAt(positionBlank-1)+curr.substring(positionBlank+1);
		add(moved, from);
		if(moved.equals(puzzleTarget)) {
			SOLVABLE = true;
			graph.BFS(puzzleStart);
		}
	}
}

	/**
	 * Move right and remove the current node from Queue
	 * @param curr
	 */
	public void moveRight(String curr){
	int positionBlank = curr.indexOf(" ");
	String from = curr;
	if(positionBlank!=2 && positionBlank!=5 && positionBlank!=8){
		String moved = curr.substring(0, positionBlank)+curr.charAt(positionBlank+1)+" "+curr.substring(positionBlank+2);
		add(moved, from);
		if(moved.equals(puzzleTarget)) {
			SOLVABLE = true;
			graph.BFS(puzzleStart);
		}
	}
}

	/**
	 * Move the blank space up and add new state to queue
	 * @param curr
	 */
	public void moveUp(String curr){
		int positionBlank = curr.indexOf(" ");
		String from = curr;
		if(positionBlank>2){
			String moved = curr.substring(0, positionBlank-3)+" "+curr.substring(positionBlank-2, positionBlank)+curr.charAt(positionBlank-3)+curr.substring(positionBlank+1);
			add(moved, from);
			if(moved.equals(puzzleTarget)) {
				SOLVABLE = true;
				graph.BFS(puzzleStart);
				}
			}
		}

	/**
	 * Move the blank space down
	 * @param curr
	 */
	public void moveDown(String curr){
		int positionBlank = curr.indexOf(" ");
		String from = curr;
		if(positionBlank<6){
			String moved = curr.substring(0, positionBlank)+curr.substring(positionBlank+3, positionBlank+4)+curr.substring(positionBlank+1, positionBlank+3)+" "+curr.substring(positionBlank+4);
			add(moved, from);
			if(moved.equals(puzzleTarget)) {
				SOLVABLE = true;
				graph.BFS(puzzleStart);
				}
			}
		}
}
