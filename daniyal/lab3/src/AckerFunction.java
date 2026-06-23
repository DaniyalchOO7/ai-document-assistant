package lab3;
import java.util.Scanner;

public class AckerFunction {

    private static int spaces = 0;
    private static int numberOfInvocations = 0;

 
    public static int countOfInvocations(){
        return numberOfInvocations;
    }

    public static int acker(int m, int n){
        numberOfInvocations++;

        // print Enter line
        printSpaces();
        System.out.println("Enter method acker: m = " + m + ", n = " + n);

        spaces++;

        int result;
        if (m == 0) {
            result = n + 1;
        } else if (n == 0) {
            result = acker(m - 1, 1);
        } else {
            result = acker(m - 1, acker(m, n - 1));
        }

        spaces--;

        // print Leave line
        printSpaces();
        System.out.println("Leave method acker: acker(" + m + ", " + n + ") = " + result);

        return result;
    }

   
    private static void printSpaces(){
        for (int i = 0; i < spaces; i++)
            System.out.print("    "); // 4 spaces per level (matches lab output)
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Input two integers separated by a space character (enter \"q\" to quit):");

        while (true) {
            System.out.print("> ");
            String input = scanner.nextLine().trim();

            if (input.equalsIgnoreCase("q")) {
                System.out.println("Quitting.");
                break;
            }

            String[] parts = input.split("\\s+");
            if (parts.length != 2) {
                System.out.println("Invalid input. Please enter two nonnegative integers separated by a space, or 'q' to quit.");
                continue;
            }

            try {
                int m = Integer.parseInt(parts[0]);
                int n = Integer.parseInt(parts[1]);

                if (m < 0 || n < 0) {
                    System.out.println("Please enter nonnegative integers only.");
                    continue;
                }

               
                if (m > 3) {
                    System.out.println("Input rejected: try a n =< 4");
                    continue;
                }
                if (m == 3 && n > 10) {
                    System.out.println("Input rejected: A(3," + n + ") is very large. Try n =< 10 for m = 3.");
                    continue;
                }

                // reset counters
                spaces = 0;
                numberOfInvocations = 0;

                int result = acker(m, n);

                System.out.println();
                System.out.println("Total number of invocations = " + countOfInvocations() + ", result = " + result);

            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please make sure both values are integers.");
            } catch (StackOverflowError soe) {
                System.out.println("Computation failed: recursion depth exceeded. Try smaller inputs.");
            } catch (OutOfMemoryError oome) {
                System.out.println("Computation failed: out of memory. Try smaller inputs.");
            }

            System.out.println();
        }

        scanner.close();
    }
}

//TODO: read two nonnegtive intergers from stardard input and

// call the recursive method acker(int, int).

// Output the total number of method invocations.



               

 