import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure bot intents (needed for reading messages and members)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Forbidden words list for auto-moderation
FORBIDDEN_WORDS = ['spam', 'scam', 'free nitro', 'crypto giveaway']

@bot.event
async def on_ready():
    print(f'🤖 {bot.user.name} has connected to Discord!')
    print('Bot is ready to manage the community.')

@bot.event
async def on_member_join(member):
    """Greets new members automatically."""
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! 🎉 Please read the rules.")

@bot.event
async def on_message(message):
    """Auto-moderation: Deletes messages with forbidden words."""
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Check for forbidden words
    content_lower = message.content.lower()
    for word in FORBIDDEN_WORDS:
        if word in content_lower:
            try:
                await message.delete()
                warning = await message.channel.send(f"⚠️ {message.author.mention}, that word is not allowed here!")
                # Delete warning after 5 seconds
                await warning.delete(delay=5)
                print(f"Deleted message from {message.author}: {message.content}")
                return # Stop processing this message
            except discord.Forbidden:
                print("Error: Bot doesn't have permission to delete messages.")

    # Important: Process commands if any
    await bot.process_commands(message)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Admin command: Clears the last X messages in the channel."""
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ Cleared {amount} messages.")
    await msg.delete(delay=3)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file.")
    else:
        bot.run(TOKEN)