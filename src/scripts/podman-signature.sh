#!/bin/bash

# Exit on any error
set -e

# Variables
IMAGE="registry.access.redhat.com/ubi9/openjdk-17"
LOCAL_IMAGE="myregistry.example.com/openjdk-17:signed"
SIGSTORE_DIR="/var/tmp/sigstore/myregistry.example.com"
POLICY_FILE="/etc/containers/policy.json"
REGISTRY_CONFIG="/etc/containers/registries.d/myregistry.yaml"
PUBLIC_KEY_FILE="/tmp/cosign.pub"
PRIVATE_KEY_FILE="/tmp/cosign.key"

# Step 1: Pull the Red Hat UBI9 OpenJDK 17 image
echo "Pulling the image: $IMAGE"
podman pull $IMAGE

# Step 2: Generate a private/public key pair if it doesn't exist (for signing)
if [ ! -f "$PRIVATE_KEY_FILE" ] || [ ! -f "$PUBLIC_KEY_FILE" ]; then
    echo "Generating a new private/public key pair for signing..."
    cosign generate-key-pair --output-key-prefix /tmp/cosign
    echo "Generated keys: $PUBLIC_KEY_FILE and $PRIVATE_KEY_FILE"
else
    echo "Using existing key pair: $PUBLIC_KEY_FILE and $PRIVATE_KEY_FILE"
fi

# Step 3: Tag the image for your private registry
echo "Tagging the image for your registry: $LOCAL_IMAGE"
podman tag $IMAGE $LOCAL_IMAGE

# Step 4: Push the image to your registry (login first if needed)
echo "Logging into your registry (provide credentials if prompted)..."
podman login myregistry.example.com || { echo "Login failed"; exit 1; }

echo "Pushing the image to $LOCAL_IMAGE..."
podman push $LOCAL_IMAGE

# Step 5: Sign the image using the private key
echo "Signing the image with Cosign using private key..."
cosign sign --key $PRIVATE_KEY_FILE $LOCAL_IMAGE

# Step 6: Configure Podman to verify signatures
echo "Setting up signature storage location..."
sudo mkdir -p /etc/containers/registries.d
sudo mkdir -p $SIGSTORE_DIR

# Create registry configuration for signature storage
cat <<EOF | sudo tee $REGISTRY_CONFIG
docker:
  myregistry.example.com:
    sigstore: file://$SIGSTORE_DIR
    sigstore-staging: file://$SIGSTORE_DIR
EOF

# Step 7: Set the trust policy to enforce signature verification
echo "Configuring Podman trust policy..."
sudo podman image trust set --type signedBy --pubkeysfile $PUBLIC_KEY_FILE myregistry.example.com

# Ensure the policy file exists and has the correct format
if [ ! -f "$POLICY_FILE" ]; then
    echo "Creating initial policy file..."
    sudo bash -c "cat > $POLICY_FILE <<EOF
{
    \"default\": [
        {
            \"type\": \"insecureAcceptAnything\"
        }
    ],
    \"transports\": {
        \"docker\": {
            \"myregistry.example.com\": [
                {
                    \"type\": \"signedBy\",
                    \"keyType\": \"x509\",
                    \"keyPath\": \"$PUBLIC_KEY_FILE\"
                }
            ]
        }
    }
}
EOF"
else
    echo "Policy file already exists, ensure it includes the correct signedBy entry."
fi

# Step 8: Verify the image by pulling it again
echo "Verifying the image by pulling it..."
podman pull $LOCAL_IMAGE || { echo "Signature verification failed"; exit 1; }

# Step 9: Inspect the image for confirmation
echo "Inspecting the image for metadata..."
podman inspect $LOCAL_IMAGE | grep -E "com.redhat.component|description"

echo "Image successfully pulled, signed, and verified!"