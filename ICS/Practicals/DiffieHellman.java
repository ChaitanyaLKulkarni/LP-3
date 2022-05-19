import java.math.BigInteger;
import java.util.Scanner;

/*
    STEPS:
    1) Choose two (p, g) different large prime number
    2) select Alice secrete key (a)
    3) calculate A = g^a mod p
    4) send p, g and A to Bob
    5) Bob selects Bob secrete key (b)
    6) calculate B = g^b mod p
    7) send B to Alice
    8) Bob computes shared key (A^b mod p) = (g^a mod p)^b mod p = g^(ab) mod p
    9) Alice computes shared key (B^a mod p) = (g^b mod p)^a mod p = g^(ab) mod p

    10) Both Alice and Bob can use the shared key to encrypt and decrypt messages
*/

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

        // Send p, g and A to Bob
        System.out.println("Enter Bob's private key (b)");
        int b = sc.nextInt();
        BigInteger B = (BigInteger.valueOf(g).pow(b)).mod(BigInteger.valueOf(p)); // g^b mod p
        System.out.println("B = " + B);

        BigInteger sharedKey = (A.pow(b)).mod(BigInteger.valueOf(p)); // A^b mod p
        System.out.println("Shared key(For Bob) = " + sharedKey);

        // Send B to Alice
        sharedKey = (B.pow(a)).mod(BigInteger.valueOf(p)); // B^a mod p
        System.out.println("Shared key(For Alice) = " + sharedKey);

        sc.close();
    }
}