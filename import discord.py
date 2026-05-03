import discord
from discord.ext import commands

# --- NASTAVENÍ ---
TOKEN = 'MTUwMDUwNzk1ODQ0MDg5MDQ3OQ.GTvnFb.rmouArVrnsiw_QQMQ7opmICOtYQGibX-PR75cQ'
LOG_CHANNEL_ID = 1493234949904535671  # <--- SEM VLOŽ ID ROOMKY, KAM MÁ BOT PSÁT
# -----------------

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

RANK_STRUCTURE = {
    1493234945718489126: [1493234945773277197, 1493234945773277196, 1493234945773277195, 1493234945773277194],
    1493238561254801408: [1493234945760432177, 1493234945760432176, 1493234945760432175],
    1493238699054600303: [1493234945760432173, 1493234945760432172],
    1493238759515226164: [1493234945760432170, 1493234945760432169, 1493234945752174631],
    1493238825135378504: [1493234945752174630, 1493234945752174629, 1493234945752174626, 1493234945752174625],
    1493238866851795176: [1493234945752174624]
}

@bot.event
async def on_ready():
    print(f'Kvartermester připraven k hlášení!')

@bot.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    current_role_ids = [role.id for role in after.roles]
    
    for category_id, rank_ids in RANK_STRUCTURE.items():
        category_role = after.guild.get_role(category_id)
        if not category_role: continue

        has_rank = any(rid in current_role_ids for rid in rank_ids)

        # PŘIDÁNÍ KATEGORIE
        if has_rank and category_role not in after.roles:
            await after.add_roles(category_role)
            if log_channel:
                await log_channel.send(f"**[PERSONELL]** Voják **{after.display_name}** byl zařazen do sekce **{category_role.name}**.")

        # ODEBRÁNÍ KATEGORIE (pokud už nemá žádnou hodnost z dané sekce)
        elif not has_rank and category_role in after.roles:
            await after.remove_roles(category_role)
            if log_channel:
                await log_channel.send(f"**[PERSONELL]** Voják **{after.display_name}** byl vyřazen ze sekce **{category_role.name}**.")

bot.run(TOKEN)