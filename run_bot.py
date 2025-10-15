"""
Simple script to run the Telegram bot
"""
import subprocess
import sys
import os

def main():
    """Run the working bot"""
    print("🚀 Starting Telegram Bot...")
    print("=" * 40)
    
    try:
        # Run the working bot
        subprocess.run([sys.executable, "working_bot.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == "__main__":
    main()
