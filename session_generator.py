"""
Session String Generator
Run this script to generate a session string for voice chat functionality
"""

import asyncio
from pyrogram import Client

API_ID = input("Enter your API_ID: ")
API_HASH = input("Enter your API_HASH: ")

async def main():
    async with Client(
        name="session_generator",
        api_id=int(API_ID),
        api_hash=API_HASH,
        in_memory=True
    ) as app:
        print("\n✅ Login successful!")
        print("\n📝 Your SESSION_STRING:\n")
        print(await app.export_session_string())
        print("\n💡 Copy this string to your .env file as SESSION_STRING")

if __name__ == "__main__":
    print("="*70)
    print("🔐 Telegram Session String Generator")
    print("="*70)
    print("\nYou'll need to:")
    print("1. Enter your phone number")
    print("2. Enter the verification code sent to Telegram")
    print("3. Enter your 2FA password (if enabled)")
    print("\n⚠️  This will log in with YOUR USER account")
    print("="*70)
    print()
    
    asyncio.run(main())
