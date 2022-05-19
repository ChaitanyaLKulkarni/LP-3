import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Base64;
import java.util.Scanner;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class AES {
    SecretKeySpec secreteKey;
    final static int KEY_SIZE = 256;

    public AES(String mKey) {
        try {
            MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
            byte[] key = sha256.digest(mKey.getBytes("UTF-8"));
            key = Arrays.copyOf(key, KEY_SIZE / 8);
            secreteKey = new SecretKeySpec(key, "AES");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String encrypt(String msg) {
        try {
            Cipher aesEnc = Cipher.getInstance("AES");
            aesEnc.init(Cipher.ENCRYPT_MODE, secreteKey);
            byte[] enc = aesEnc.doFinal(msg.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(enc);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public String decrypt(String enc) {
        try {
            Cipher aesDec = Cipher.getInstance("AES");
            aesDec.init(Cipher.DECRYPT_MODE, secreteKey);
            byte[] encBytes = Base64.getDecoder().decode(enc);
            byte[] dec = aesDec.doFinal(encBytes);
            return new String(dec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter password: ");

        AES aes = new AES(sc.nextLine());

        System.out.println("Enter Plain Text");
        String plainText = sc.nextLine();

        String enc = aes.encrypt(plainText);
        System.out.println("Encrypted: " + enc);

        String dec = aes.decrypt(enc);
        System.out.println("Decrypted: " + dec);
    }
}
