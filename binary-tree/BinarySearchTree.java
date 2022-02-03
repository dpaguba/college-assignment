import java.util.Iterator;

public class BinarySearchTree<T extends Comparable<T>>
{

  /*
  Excercise 1
  */
    public int countNodes (int top, int bottom){
        if (top<=bottom && !isEmpty()){
            if (top<=0 && bottom>=0){
                return 1
                        + leftChild.countNodes(top-1, bottom-1)
                        + rightChild.countNodes(top-1, bottom-1);
            }
            if(bottom < 0){
                return 0;
            }
            return leftChild.countNodes(top-1, bottom-1)
                    + rightChild.countNodes(top-1, bottom-1);
        }
        else {
            return 0;
        }
    }
    
    /*
    Excercise 2
    */
    public int sortedUpTo(int needToPrint){
        if (needToPrint > 0 && !isEmpty()){
            int leftToPrint = leftChild.sortedUpTo(needToPrint);
            if (leftToPrint!=0) {
                System.out.println(content);
                leftToPrint = rightChild.sortedUpTo(needToPrint-1);
                return leftToPrint;
            }else{
                return 0;
            }
        }else{
            return needToPrint;
        }

    }
    

}
  
