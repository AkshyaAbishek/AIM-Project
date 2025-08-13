# AI Toolkit Setup and Installation Guide
# Run this script to set up the AI-enhanced AIM environment

"""
AI Toolkit Setup for AIM Project

This script helps set up the AI development environment for the AIM project.
It provides step-by-step installation and configuration of all AI toolkits.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


class AIToolkitSetup:
    """Automated setup for AI toolkit development environment."""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.project_root = Path(__file__).parent
        
    def setup_environment(self):
        """Complete AI toolkit environment setup."""
        
        print("🤖 AI Toolkit Setup for AIM Project")
        print("=" * 50)
        print(f"Platform: {self.platform}")
        print(f"Python: {self.python_version}")
        print(f"Project: {self.project_root}")
        print()
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Create virtual environment
        if not self.create_virtual_environment():
            return False
        
        # Step 3: Install AI packages
        if not self.install_ai_packages():
            return False
        
        # Step 4: Download AI models
        if not self.download_ai_models():
            return False
        
        # Step 5: Verify installation
        if not self.verify_installation():
            return False
        
        print("\n🎉 AI Toolkit Setup Complete!")
        print("\nNext steps:")
        print("1. Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print("2. Run the AI demo: python tutorials/project_examples/AI_ENHANCED_IMPLEMENTATION.py")
        print("3. Explore the documentation: documentation/AI_TOOLKIT_IMPLEMENTATION_PLAN.md")
        
        return True
    
    def check_python_version(self):
        """Check if Python version is compatible with AI toolkits."""
        print("🔍 Checking Python version...")
        
        if sys.version_info < (3, 8):
            print("❌ Python 3.8 or higher required for AI toolkits")
            print(f"   Current version: {self.python_version}")
            return False
        
        print(f"✅ Python {self.python_version} is compatible")
        return True
    
    def create_virtual_environment(self):
        """Create a virtual environment for AI development."""
        print("📦 Creating virtual environment...")
        
        venv_path = self.project_root / "venv-ai"
        
        if venv_path.exists():
            print("✅ Virtual environment already exists")
            return True
        
        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(venv_path)
            ], check=True)
            print("✅ Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def install_ai_packages(self):
        """Install all AI/ML packages from requirements."""
        print("📚 Installing AI packages...")
        
        # Determine pip path based on platform
        venv_path = self.project_root / "venv-ai"
        if self.platform == "windows":
            pip_path = venv_path / "Scripts" / "pip"
        else:
            pip_path = venv_path / "bin" / "pip"
        
        # Install base requirements first
        requirements_files = [
            "requirements.txt",  # Base AIM requirements
            "requirements-ai.txt"  # AI toolkit requirements
        ]
        
        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                try:
                    print(f"  Installing from {req_file}...")
                    subprocess.run([
                        str(pip_path), "install", "-r", str(req_path)
                    ], check=True)
                    print(f"  ✅ {req_file} installed successfully")
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ Failed to install {req_file}: {e}")
                    return False
        
        return True
    
    def download_ai_models(self):
        """Download required AI models."""
        print("🧠 Downloading AI models...")
        
        models_to_download = [
            {
                "name": "spaCy English model",
                "command": ["python", "-m", "spacy", "download", "en_core_web_sm"],
                "description": "English language model for NLP"
            },
            {
                "name": "NLTK Data",
                "python_code": """
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
""",
                "description": "NLTK data packages for text processing"
            }
        ]
        
        for model in models_to_download:
            try:
                print(f"  Downloading {model['name']}...")
                
                if "command" in model:
                    subprocess.run(model["command"], check=True)
                elif "python_code" in model:
                    exec(model["python_code"])
                
                print(f"  ✅ {model['name']} downloaded")
                
            except Exception as e:
                print(f"  ⚠️ Warning: Could not download {model['name']}: {e}")
                print(f"     You may need to download this manually later")
        
        return True
    
    def verify_installation(self):
        """Verify that all AI packages are installed correctly."""
        print("🔧 Verifying AI toolkit installation...")
        
        # Key packages to verify
        key_packages = [
            ("numpy", "NumPy"),
            ("pandas", "Pandas"),
            ("sklearn", "scikit-learn"),
            ("transformers", "Transformers"),
            ("spacy", "spaCy"),
            ("xgboost", "XGBoost")
        ]
        
        failed_imports = []
        
        for package, name in key_packages:
            try:
                __import__(package)
                print(f"  ✅ {name}")
            except ImportError:
                print(f"  ❌ {name} - Import failed")
                failed_imports.append(name)
        
        if failed_imports:
            print(f"\n⚠️ Some packages failed to import: {', '.join(failed_imports)}")
            print("You may need to install these manually or check for compatibility issues")
            return False
        
        print("✅ All key AI packages verified successfully")
        return True
    
    def create_example_config(self):
        """Create example configuration files for AI features."""
        config_dir = self.project_root / "config" / "ai"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # AI configuration template
        ai_config = {
            "models": {
                "field_mapping": {
                    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                    "confidence_threshold": 0.8
                },
                "risk_assessment": {
                    "model_type": "xgboost",
                    "features": ["age", "income", "coverage_amount"],
                    "risk_threshold": 0.7
                },
                "document_processing": {
                    "spacy_model": "en_core_web_sm",
                    "ner_model": "dbmdz/bert-large-cased-finetuned-conll03-english"
                }
            },
            "api_keys": {
                "openai": "your-openai-api-key-here",
                "huggingface": "your-huggingface-token-here"
            },
            "performance": {
                "use_gpu": False,
                "batch_size": 32,
                "max_sequence_length": 512
            }
        }
        
        config_file = config_dir / "ai_config.json"
        with open(config_file, 'w') as f:
            json.dump(ai_config, f, indent=2)
        
        print(f"📝 Created AI configuration template: {config_file}")


def main():
    """Main setup function."""
    setup = AIToolkitSetup()
    
    print("Would you like to:")
    print("1. Full AI toolkit setup (recommended)")
    print("2. Install packages only")
    print("3. Verify existing installation")
    print("4. Create configuration templates")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        success = setup.setup_environment()
        if success:
            setup.create_example_config()
    elif choice == "2":
        setup.install_ai_packages()
    elif choice == "3":
        setup.verify_installation()
    elif choice == "4":
        setup.create_example_config()
    else:
        print("Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()
