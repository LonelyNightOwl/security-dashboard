import java.sql.*;
import java.security.SecureRandom;

public class SafeJava {
    
    // Safe parameterized query
    public static ResultSet getUserDataSafe(String username) throws SQLException {
        String query = "SELECT * FROM users WHERE username = ?";
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db");
        PreparedStatement stmt = conn.prepareStatement(query);
        stmt.setString(1, username);
        return stmt.executeQuery();
    }
    
    // Secure random token generation
    public static String generateTokenSafe() {
        SecureRandom random = new SecureRandom();
        byte[] tokenBytes = new byte[32];
        random.nextBytes(tokenBytes);
        return javax.xml.bind.DatatypeConverter.printHexBinary(tokenBytes);
    }
    
    // Safe command execution with whitelist
    public static boolean executeCommandSafe(String cmd) throws Exception {
        String[] allowedCommands = {"ls", "pwd", "echo"};
        boolean isAllowed = false;
        
        for (String allowed : allowedCommands) {
            if (cmd.equals(allowed)) {
                isAllowed = true;
                break;
            }
        }
        
        if (!isAllowed) {
            throw new IllegalArgumentException("Command not allowed");
        }
        
        Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
        return true;
    }
    
    // Input validation
    public static boolean validateUsername(String username) {
        return username != null && username.matches("[a-zA-Z0-9_]{3,20}");
    }
}