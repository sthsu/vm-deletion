#!/bin/bash

# Update vscode
wget 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64' -O /tmp/code_latest_amd64.deb
sudo dpkg -i /tmp/code_latest_amd64.deb

# Check if Python 3.11 is already installed
if command -v python3.11 &>/dev/null; then
    echo "Python 3.11 is already installed."
else
    # Install Python 3.11 using apt
    echo "Python 3.11 not found. Installing Python 3.9 using apt..."
    sudo apt update
    sudo apt install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.11 -y
    sudo apt install python3.11-venv -y
fi

# Verify installation
if command -v python3.11 &>/dev/null; then
    echo "Python 3.11 installation successful."
    python3.9 --version
else
    echo "Python 3.11 installation failed. Please install manually."
fi

# Install Azure CLI
if command -v az &>/dev/null; then
    echo "Azure CLI is already installed."
else
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# List of extensions to install 
extensions=(
    "ms-python.python"
    "ms-azuretools.vscode-azurefunctions"
    "Azurite.azurite"
)

# Loop through each extension and install it
for extension in "${extensions[@]}"
do
    code --install-extension "$extension"
done

echo "Extensions installation complete."


# Install Core Tools
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4

echo "Azure Functions Core Tools installation complete."


python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt