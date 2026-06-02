#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFFER 256

// Safe input handling with bounds checking
void process_input_safe(const char *input) {
    if (input == NULL) {
        fprintf(stderr, "Error: input is NULL\n");
        return;
    }
    
    char buffer[MAX_BUFFER];
    strncpy(buffer, input, MAX_BUFFER - 1);
    buffer[MAX_BUFFER - 1] = '\0';
    printf("Buffer: %s\n", buffer);
}

// Safe command execution with validation
int execute_command_safe(const char *cmd) {
    if (cmd == NULL || strlen(cmd) == 0) {
        fprintf(stderr, "Error: invalid command\n");
        return -1;
    }
    
    // Use execve instead of system for better control
    // (Conceptual - actual implementation would be more complex)
    return 0;
}

// Initialize variables properly
int safe_math() {
    int result = 0;  // Properly initialized
    result = result + 5;
    return result;
}

// Constants defined securely
const char *get_config(const char *key) {
    if (strcmp(key, "timeout") == 0) {
        return "30";
    }
    return NULL;
}