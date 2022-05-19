import java.math.BigInteger;
import java.util.Scanner;

/*
    STEPS:
    1) Choose two (p, q) different large prime number
    2) calculate n = p * q
    3) calculate phi(n) = (p - 1) * (q - 1)
    4) Choose e, 1 < e < phi(n) such that gcd(e, phi(n)) = 1
    5) calculate d = e^-1 mod phi(n)

    e,n = public key
    d,n = private key
*/

public class RSA {

    static long gcd(long phiOfN, long e) {
        long temp;
        while (true) {
            temp = phiOfN % e;
            if (temp == 0)
                return e;
            phiOfN = e;
            e = temp;
        }
    }

    public static long getEncyptionkey(long phiOfN) {
        long e = 2;
        for (e = 2; e < phiOfN; e++) {
            if (gcd(phiOfN, e) == 1) {
                return e;
            }
        }
        return e;
    }

    public static long getDecryptionKey(long phiOfN, long e) {
        double num = 0.0;
        for (int i = 0; i < 100; i++) {
            num = (double) (i * phiOfN + 1) / e;
            if (Math.floor(num) == num)
                break;
        }
        return (long) num;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter two prime number (p & q) ");
        int p = sc.nextInt();
        int q = sc.nextInt();

        long n = p * q;

        long phiOfN = (p - 1) * (q - 1);

        long e = getEncyptionkey(phiOfN);

        long d = getDecryptionKey(phiOfN, e);

        System.out.println("n = " + n);
        System.out.println("e (public key) = " + e);
        System.out.println("d (private key) = " + d);
        while (true) {
            System.out.println("Enter message to be encrypted ");
            long message = sc.nextLong();
            if (message == 0)
                break;
            BigInteger encryptedMessage = (BigInteger.valueOf(message).pow((int) e).mod(BigInteger.valueOf(n))); // msg
                                                                                                                 // ^ e
                                                                                                                 // mod
                                                                                                                 // n
            System.out.println("Encrypted message = " + encryptedMessage.intValue());

            BigInteger decryptedMessage = (BigInteger.valueOf(encryptedMessage.intValue()).pow((int) d)
                    .mod(BigInteger.valueOf(n))); // enc ^ d mod n
            System.out.println("Decrypted message = " + decryptedMessage.intValue());
        }
        sc.close();
    }
}
