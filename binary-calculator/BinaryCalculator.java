import java.util.Scanner;

public class BinaryCalculator {

    public static void main(String[] args) {

        System.out.println("Welcome in binary number calculator!");
        System.out.println("Please enter numbers with the same quantity of digits, so I can work properly!\n");

        Scanner in = new Scanner(System.in);
        System.out.println("Enter your first binary number: ");
        String firstInput = in.next();
        System.out.println("Enter your second binary number: ");
        String secondInput = in.next();
        System.out.println("What should I do? (+, -, *): ");
        String sign = in.next();
        
        if (firstInput.length() != secondInput.length()){
            System.out.println("ERROR: You entered numbers with unequal quantity of digits. Try again!");
        }else {
            switch (sign){
                case "+":
                    // do addition
                    break;
                case "-":
                    //do substraktion
                    break;
                case "*":
                    //do multiplikation
                    break;
                default:
                    System.out.println("ERROR: Invalid sign. Try again!");
                    break;
            }
        }
    }


}


