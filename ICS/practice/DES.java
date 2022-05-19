import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Base64;
import java.util.Scanner;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class DES {
    SecretKeySpec secretKey;
    static final int KEY_SIZE = 64;

    public DES(String mKey) {
        try {
            MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
            byte[] key = sha1.digest(mKey.getBytes("UTF-8"));
            key = Arrays.copyOf(key, KEY_SIZE / 8);
            secretKey = new SecretKeySpec(key, "DES");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String encrypt(String msg) {
        try {
            Cipher desEnc = Cipher.getInstance("DES");
            desEnc.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] enc = desEnc.doFinal(msg.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(enc);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public String decrypt(String enc) {
        try {
            Cipher desDec = Cipher.getInstance("DES");
            desDec.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] encBytes = Base64.getDecoder().decode(enc);
            byte[] dec = desDec.doFinal(encBytes);
            return new String(dec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        DES des = new DES(sc.nextLine());

        String plainText = sc.nextLine();
        String encText = des.encrypt(plainText);
        System.out.println("Encrypted Text: " + encText);

        String decText = des.decrypt(encText);
        System.out.println("Decrypted Text: " + decText);
    }

}