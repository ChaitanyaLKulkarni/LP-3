import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class DES {

    private static SecretKeySpec secretKey;
    private final static int KEY_SIZE = 64;
    private static byte[] key;

    public static void setKey(String myKey) {
        MessageDigest sha = null;
        try {
            key = myKey.getBytes("UTF-8");
            sha = MessageDigest.getInstance("SHA-1");
            key = sha.digest(key);
            key = Arrays.copyOf(key, KEY_SIZE / 8);
            secretKey = new SecretKeySpec(key, "DES");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String encrypt(String msg, String key) {
        setKey(key);
        try {
            Cipher desCipher = Cipher.getInstance("DES");
            desCipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] enc = desCipher.doFinal(msg.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(enc);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String decrypt(String enc, String key) {
        setKey(key);
        try {
            Cipher desCipher = Cipher.getInstance("DES");
            desCipher.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] dec = desCipher.doFinal(Base64.getDecoder().decode(enc));
            return new String(dec);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) {
        try {
            System.out.println("Message Encryption Using DES Algorithm\n-------");
            String mKey = "SecretKey";

            String plainText = "Keep this secret";
            System.out.println("Message : " + plainText);

            String textEncrypted = encrypt(plainText, mKey);
            System.out.println("Encrypted Message : " + textEncrypted);

            String textDecrypted = decrypt(textEncrypted, mKey);
            System.out.println("Decrypted Message : " + textDecrypted);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}