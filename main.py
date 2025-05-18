import discord
from discord.ext import commands
import random
import os
from keep_alive import keep_alive  # Import funkcji keep_alive

# Utrzymaj bota przy życiu
keep_alive()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Prefixy do generatora nitro
nitro_prefixes = [
    "https://discord.gift/xhCGj64ea4pbHOea",
    "https://discord.gift/NIe0UnYmUxsVt55r",
    "https://discord.gift/tNuOR8Wg8hpatxs9",
    "https://discord.gift/yjAGINbcYeG2yMRb"
]

# OPINIA - komenda dla klientów
@bot.command(name="opinia")
async def opinia(ctx):
    if "klient" not in [role.name.lower() for role in ctx.author.roles]:
        return await ctx.send("❌ Nie masz uprawnień do wystawienia opinii.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("🕐 **Czas realizacji (1-5):**")
        czas = await bot.wait_for('message', check=check, timeout=30.0)

        await ctx.send("📦 **Jakość produktu (1-5):**")
        jakosc = await bot.wait_for('message', check=check, timeout=30.0)

        await ctx.send("🛠 **Wykonanie usługi (1-5):**")
        wykonanie = await bot.wait_for('message', check=check, timeout=30.0)

        embed = discord.Embed(title="📝 Nowa Opinia", color=discord.Color.green())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.add_field(name="⏱ Czas realizacji", value=czas.content, inline=True)
        embed.add_field(name="📦 Jakość produktu", value=jakosc.content, inline=True)
        embed.add_field(name="🛠 Wykonanie usługi", value=wykonanie.content, inline=True)
        embed.set_footer(text="Dziękujemy za opinię!")

        await ctx.send(embed=embed)

    except Exception:
        await ctx.send("⏳ Czas na odpowiedź minął lub wystąpił błąd.")

# GEN-NITRO
@bot.command(name="gen-nitro")
async def gen_nitro(ctx):
    kod = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", k=16))
    link = random.choice(nitro_prefixes) + kod

    await ctx.send("✅ Twój kod został wysłany w wiadomości prywatnej.")
    try:
        await ctx.author.send(f"🎁 Twój kod nitro: `{link}`")
    except discord.Forbidden:
        await ctx.send("❌ Nie mogę wysłać wiadomości prywatnej – masz zablokowane DM-y.")

# Uruchomienie bota
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ Brak zmiennej DISCORD_TOKEN")
