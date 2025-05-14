#!/bin/bash

# Input parameters
PEM_FILE="$1"
PASSWORD="$2"

# Check if input file and password are provided
if [ -z "$PEM_FILE" ] || [ -z "$PASSWORD" ]; then
    echo "Usage: $0 <pem_file> <password>"
    exit 1
fi

# Check if PEM file exists
if [ ! -f "$PEM_FILE" ]; then
    echo "Error: PEM file '$PEM_FILE' not found."
    exit 1
fi

# Temporary files for processing
TEMP_DECRYPTED_KEY=$(mktemp)
TEMP_PUBLIC_KEY=$(mktemp)
TRAP="rm -f $TEMP_DECRYPTED_KEY $TEMP_PUBLIC_KEY; exit"
trap "$TRAP" EXIT INT TERM

# Step 1: Extract the encrypted private key (original PEM content)
# Check if the PEM file contains an encrypted private key
if ! grep -q "BEGIN ENCRYPTED PRIVATE KEY" "$PEM_FILE"; then
    echo "Error: PEM file does not contain an encrypted private key."
    exit 1
fi

# Replace header with custom Sigstore header
ENCRYPTED_PRIVATE_KEY=$(cat "$PEM_FILE" | sed 's/BEGIN ENCRYPTED PRIVATE KEY/BEGIN ENCRYPTED SIGSTORE PRIVATE KEY/' | sed 's/END ENCRYPTED PRIVATE KEY/END ENCRYPTED SIGSTORE PRIVATE KEY/')
echo "Encrypted Sigstore Private Key:"
echo "$ENCRYPTED_PRIVATE_KEY"
echo

# Step 2: Decrypt the private key
if ! openssl pkey -in "$PEM_FILE" -out "$TEMP_DECRYPTED_KEY" -passin pass:"$PASSWORD" 2>/dev/null; then
    echo "Error: Failed to decrypt private key. Incorrect password or invalid PEM file."
    exit 1
fi

# Step 3: Derive the public key
if ! openssl ec -in "$TEMP_DECRYPTED_KEY" -pubout -out "$TEMP_PUBLIC_KEY" 2>/dev/null; then
    echo "Error: Failed to derive public key. Ensure the private key is ECDSA."
    exit 1
fi

# Step 4: Format the public key with custom Sigstore header
PUBLIC_KEY=$(cat "$TEMP_PUBLIC_KEY" | sed 's/BEGIN PUBLIC KEY/BEGIN SIGSTORE PUBLIC KEY/' | sed 's/END PUBLIC KEY/END SIGSTORE PUBLIC KEY/')
echo "Sigstore Public Key:"
echo "$PUBLIC_KEY"

# Clean up temporary files (handled by trap)
