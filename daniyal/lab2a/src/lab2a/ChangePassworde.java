package lab2a;

	import java.util.Scanner;
	//import java.util.Arrays;
	import java.io.PrintWriter;
	public class ChangePassworde {
	static boolean validateLogin(String username, String password) {
	return true;
	}
	static boolean resetPassword(String username, String password) {
	return true;
	}
	public static void main(String[] args) {
	Scanner scanner = new Scanner(System.in);
	System.out.println("Update your password:");
	boolean foundError = false;
	do {
	System.out.print("Enter New Password: ");
	String pwd = scanner.nextLine();
	System.out.print("Verify your New Password: ");
	String pwd2 = scanner.nextLine();
	foundError = false;
	// 2. Must be at least 6 characters
	if (pwd.length() < 6) {
	System.out.println("Error: Your password must be at least 6 characters long.");
	foundError = true;
	}
	// 1. Must match
	if (!pwd.equals(pwd2)) {
	System.out.println("Error: Your passwords do not match.");
	foundError = true;
	}
	boolean hasNonLetter = false;
	for (int i = 0; i < pwd.length(); i++) {
	char c = pwd.charAt(i);
	if (!Character.isLetter(c)) {
	hasNonLetter = true;
	break;
	}
	}
	if (!hasNonLetter) {
	System.out.println("Error: Password must contain at least one non-letter character.");
	foundError = true;
	}
	if (!foundError) { System.out.println("Your password is succesfully updated!");
	}
	}
	while (foundError);
	}

}
