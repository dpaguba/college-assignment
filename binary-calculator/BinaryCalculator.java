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
                    display(add(toBinary(firstInput), toBinary(secondInput)));
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
    
    private static int [] toBinary(String str){
        int [] numbers = new int[str.length()];

        for (int position = 0; position < numbers.length; position++) {
            try{
                numbers[position] = Integer.parseInt(String.valueOf(str.charAt(position)));
            }catch (Exception e){
                System.out.println("Invalid Input of number: " + str);
                break;
            }
        }

        return numbers;
    }
    
    private static void display(int [] numbers){
        System.out.print("Result: ");
        for (int num : numbers) {
            System.out.print(num);
        }
    }
    
    private static int [] add(int [] firstNumber, int [] secondNumber){
        int [] result = new int[firstNumber.length + 1];
        int carryBit = 0;

        for (int position = result.length - 1; position > 0; position--) { 
            if ((firstNumber[position - 1] + secondNumber[position - 1]) == 0){
                if (carryBit == 0){
                    result[position] = 0;
                }else {
                    result[position] = 1;
                    carryBit = 0;
                }
            }else if ((firstNumber[position - 1] + secondNumber[position - 1]) == 1){
                if (carryBit == 0){
                    result[position] = 1;
                }else {
                    result[position] = 0;
                    carryBit = 1;
                }
            }else if ((firstNumber[position - 1] + secondNumber[position - 1]) == 2){
                if (carryBit == 0){
                    result[position] = 0;
                }else {
                    result[position] = 1;
                }
                carryBit = 1;
            }
        }

        if (carryBit == 1){
            result[0] = carryBit;
        }

        return result;
    }


}


