"""
Setup and Installation Script
Run this script to set up the project
"""

import os
import sys
from pathlib import Path


def main():
    """Main setup function"""
    print("=" * 60)
    print("Research Paper Assistant - Setup Script")
    print("=" * 60)
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("\n📝 Creating .env file...")
        env_content = """# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Vector Database Configuration
VECTOR_DB_PATH=./data/vector_store

# PDF Storage
PDF_UPLOAD_DIR=./data/uploads

# Application Settings
DEBUG=False
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created. Please add your Groq API key!")
    else:
        print("\n✅ .env file already exists")
    
    # Create data directories
    print("\n📁 Creating data directories...")
    Path("data/uploads").mkdir(parents=True, exist_ok=True)
    Path("data/vector_store").mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    
    print("\n" + "=" * 60)
    print("Setup complete! Next steps:")
    print("=" * 60)
    print("\n1. Edit .env file and add your Groq API key:")
    print("   - Get it from: https://console.groq.com/keys")
    print("   - Replace 'your_groq_api_key_here' with your actual key\n")
    print("2. Install dependencies:")
    print("   python -m pip install --upgrade pip")
    print("   pip install -r requirements.txt\n")
    print("3. Run the application:")
    print("   python main.py\n")
    print("=" * 60)


if __name__ == "__main__":
    main()
