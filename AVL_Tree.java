package avl;
/**
 * @author ratneshn
 * @param <K>
 */
public class AVL<K extends Comparable<K>> {
  Node<K> root;
  /* Normally this should be private or protected. But I'm doing whitebox
     testing, I need access from the outside.
  */
    private static <K extends Comparable<K>> boolean search(K T, Node<K> V){
        // Search through V for the values of T
        if(V != null){
            // If T's key is found, returns true
            if((V.key).equals(T)){
                return true;
                // Check if the key of V is smaller than that of T
            } else if((V.key).compareTo(T) > 0){
                // If greater, then search the left tree
                return search(T, V.left);
            } else{
                // If smaller, then search the right tree
                return search(T, V.right);
            }
        } else{
            return false;
        }
    }

    public static <K extends Comparable<K>> boolean subset(Node<K> T, Node<K> V) {
        // Checks if T is a empty tree => subset
        if(T == null){
            return true;
        }
        // If T root exists
        if(search(T.key, V)){
            // check is the children of T is containd in V
            return (subset(T.right, V) && subset(T.left, V));
        } else{
            return false;
        }
    }

    /* Where T is a subset of V. */
    public static <K extends Comparable<K>> boolean subset(AVL<K> T, AVL<K> V) {
         // call on a method subset that takes in the root of V and T
        return subset(T.root, V.root);
    }
}
