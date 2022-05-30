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
            switch (sign) {
                case "+" -> {
                    int sum = Integer.parseInt(firstInput, 2) + Integer.parseInt(secondInput, 2);
                    System.out.println(Integer.toBinaryString(sum));
                }
                case "-" -> {
                    int difference = Integer.parseInt(firstInput, 2) - Integer.parseInt(secondInput, 2);
                    System.out.println(Integer.toBinaryString(difference));
                }
                case "*" -> {
                    int product = Integer.parseInt(firstInput, 2) * Integer.parseInt(secondInput, 2);
                    System.out.println(Integer.toBinaryString(product));
                }
                default -> System.out.println("ERROR: Invalid sign. Try again!");
            }
        }
    }
}

# Modified 2025-08-11 10:24:29