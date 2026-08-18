import java.util.Scanner;

public class ScientificCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        double num1, num2, result = 0.0;
        int choice;

        System.out.println("===== Scientific Calculator =====");
        System.out.println("1. Addition");
        System.out.println("2. Subtraction");
        System.out.println("3. Multiplication");
        System.out.println("4. Division");
        System.out.println("5. Power");
        System.out.println("6. Square Root");
        System.out.println("7. Sine");
        System.out.println("8. Cosine");
        System.out.println("9. Tangent");
        System.out.println("10. Logarithm (base e)");
        System.out.print("Choose an operation (1-10): ");
        choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter first number: ");
                num1 = scanner.nextDouble();
                System.out.print("Enter second number: ");
                num2 = scanner.nextDouble();
                result = num1 + num2;
                break;

            case 2:
                System.out.print("Enter first number: ");
                num1 = scanner.nextDouble();
                System.out.print("Enter second number: ");
                num2 = scanner.nextDouble();
                result = num1 - num2;
                break;

            case 3:
                System.out.print("Enter first number: ");
                num1 = scanner.nextDouble();
                System.out.print("Enter second number: ");
                num2 = scanner.nextDouble();
                result = num1 * num2;
                break;

            case 4:
                System.out.print("Enter first number: ");
                num1 = scanner.nextDouble();
                System.out.print("Enter second number: ");
                num2 = scanner.nextDouble();
                if (num2 != 0)
                    result = num1 / num2;
                else {
                    System.out.println("Error: Division by zero.");
                    return;
                }
                break;

            case 5:
                System.out.print("Enter base number: ");
                num1 = scanner.nextDouble();
                System.out.print("Enter exponent: ");
                num2 = scanner.nextDouble();
                result = Math.pow(num1, num2);
                break;

            case 6:
                System.out.print("Enter number: ");
                num1 = scanner.nextDouble();
                if (num1 >= 0)
                    result = Math.sqrt(num1);
                else {
                    System.out.println("Error: Cannot calculate square root of negative number.");
                    return;
                }
                break;

            case 7:
                System.out.print("Enter angle in degrees: ");
                num1 = scanner.nextDouble();
                result = Math.sin(Math.toRadians(num1));
                break;

            case 8:
                System.out.print("Enter angle in degrees: ");
                num1 = scanner.nextDouble();
                result = Math.cos(Math.toRadians(num1));
                break;

            case 9:
                System.out.print("Enter angle in degrees: ");
                num1 = scanner.nextDouble();
                result = Math.tan(Math.toRadians(num1));
                break;

            case 10:
                System.out.print("Enter number: ");
                num1 = scanner.nextDouble();
                if (num1 > 0)
                    result = Math.log(num1);
                else {
                    System.out.println("Error: Logarithm of non-positive number is undefined.");
                    return;
                }
                break;

            default:
                System.out.println("Invalid choice!");
                return;
        }

        System.out.println("Result: " + result);
    }
}
