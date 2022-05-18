import java.math.BigInteger;
import java.util.Scanner;

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
            if (num % 1 == 0)
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

        System.out.println("Enter message to be encrypted ");
        long message = sc.nextLong();

        BigInteger encryptedMessage = (BigInteger.valueOf(message).pow((int) e).mod(BigInteger.valueOf(n)));
        System.out.println("Encrypted message = " + encryptedMessage.intValue());

        BigInteger decryptedMessage = (BigInteger.valueOf(encryptedMessage.intValue()).pow((int) d)
                .mod(BigInteger.valueOf(n)));
        System.out.println("Decrypted message = " + decryptedMessage.intValue());

        sc.close();
    }
}
