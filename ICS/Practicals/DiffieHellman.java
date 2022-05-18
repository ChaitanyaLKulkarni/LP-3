import java.math.BigInteger;
import java.util.Scanner;

public class DiffieHellman {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter two prime number (p & g) ");
        int p = sc.nextInt();
        int g = sc.nextInt();

        System.out.println("Enter Alice's private key (a) ");
        int a = sc.nextInt();
        BigInteger A = (BigInteger.valueOf(g).pow(a)).mod(BigInteger.valueOf(p)); // g^a mod p
        System.out.println("A = " + A);

        System.out.println("Enter Bob's private key (b)");
        int b = sc.nextInt();
        BigInteger B = (BigInteger.valueOf(g).pow(b)).mod(BigInteger.valueOf(p)); // g^b mod p
        System.out.println("B = " + B);

        BigInteger sharedKey = (A.pow(b)).mod(BigInteger.valueOf(p));
        System.out.println("Shared key(For Bob) = " + sharedKey);

        sharedKey = (B.pow(a)).mod(BigInteger.valueOf(p));
        System.out.println("Shared key(For Alice) = " + sharedKey);
    }
}