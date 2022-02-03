import java.util.Iterator;

public class BinarySearchTree<T extends Comparable<T>>
{

  public int mostTwoChildrenNodes()
  {
      if (isEmpty()){
          return 0;
      }else{
          if (isLeaf()){
              return 0;
          }
          if (!rightChild.isEmpty() && !leftChild.isEmpty()){
              return 1+Math.max(rightChild.mostTwoChildrenNodes(), leftChild.mostTwoChildrenNodes());
          }else if (rightChild.isEmpty() && !leftChild.isEmpty()){
              return leftChild.mostTwoChildrenNodes();
          }else {
              return rightChild.mostTwoChildrenNodes();
          }

      }

  }
  
