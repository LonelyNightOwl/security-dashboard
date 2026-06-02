import java.sql.*;

public class VulnerableJava {
    
    // SQL Injection vulnerability
    public static ResultSet getUserData(String username) throws SQLException {
        String query = "SELECT * FROM users WHERE username = '" + username + "'";
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db");
        Statement stmt = conn.createStatement();
        return stmt.executeQuery(query);
    }
    
    // Hardcoded credentials
    private static final String DB_PASSWORD = "admin123";
    private static final String API_KEY = "sk-1234567890abcdef";
    
    // Weak random number generation
    public static String generateToken() {
        java.util.Random rand = new java.util.Random();
        return String.valueOf(rand.nextInt(100000));
    }
    
    // Command injection
    public static void executeCommand(String cmd) throws Exception {
        Runtime.getRuntime().exec(cmd);
    }
    
    // Insecure deserialization
    public static Object deserialize(byte[] data) throws Exception {
        java.io.ObjectInputStream ois = new java.io.ObjectInputStream(
            new java.io.ByteArrayInputStream(data)
        );
        return ois.readObject();
    }
}