#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Buffer overflow vulnerability
void process_input(char *input) {
    char buffer[10];
    strcpy(buffer, input);  // Unsafe - no bounds checking
    printf("Buffer: %s\n", buffer);
}

// Command injection vulnerability
void execute_command(char *cmd) {
    system(cmd);  // Unsafe - user input passed directly
}

// Use of uninitialized variable
int unsafe_math() {
    int result;
    result = result + 5;  // result not initialized
    return result;
}

// Hardcoded credentials
const char *PASSWORD = "admin123";
const char *API_KEY = "sk-1234567890abcdef";