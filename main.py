import discord
from discord.ext import commands
from discord import app_commands
from logic import quiz_questions
from collections import defaultdict
from config import token
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcıların oyun durumu
user_progress = {}
user_inventory = defaultdict(list)

# ===================== ENVANTER KOMUTU =====================
@bot.tree.command(name="envanter", description="Envanterini gösterir.")
async def envanter(interaction: discord.Interaction):
    user_id = interaction.user.id
    inv = user_inventory.get(user_id, [])
    if not inv:
        msg = "Envanterin boş."
    else:
        msg = "Envanterindeki eşyalar:\n" + "\n".join(f"- {item}" for item in inv)
    await interaction.response.send_message(msg, ephemeral=True)


def add_item_to_inventory(user_id, item_name):
    user_inventory[user_id].append(item_name)


# ===================== START KOMUTU =====================
@bot.tree.command(name="start", description="Oyuna başla ve hikayeni yaşa.")
async def start(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_progress:
        await interaction.response.send_message("Zaten oyuna başladın!", ephemeral=True)
        return
    if not quiz_questions:
        await interaction.response.send_message("Hikaye henüz eklenmemiş!", ephemeral=True)
        return
    first_question_id = next(iter(quiz_questions))
    user_progress[user_id] = first_question_id
    await send_question(interaction, user_id)
    
        # 🔥 eklenen kısım
    await interaction.response.defer(ephemeral=False, thinking=True)

    await send_question(interaction, user_id)

# ===================== HARİTA KOMUTU =====================
@bot.tree.command(name="harita", description="Oyunun haritasını gösterir.")
async def harita(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)  # ⏳ beklemeyi bildir

    # Dosya yollarını sırayla dene
    possible_paths = ["assets/harita.png", "harita.png"]
    harita_path = None
    for path in possible_paths:
        if os.path.exists(path):
            harita_path = path
            break

    if not harita_path:
        await interaction.followup.send("❌ Harita dosyası bulunamadı!")
        return

    file = discord.File(harita_path, filename="harita.png")
    await interaction.followup.send("🗺️ İşte yolculuğun haritası:", file=file)

# ===================== SORU GÖNDER =====================
async def send_question(interaction_or_ctx, user_id):
    question_id = user_progress.get(user_id)
    if not question_id or question_id not in quiz_questions:
        await send_end(interaction_or_ctx, user_id)
        return

    question = quiz_questions[question_id]
    buttons = question.gen_buttons()
    view = discord.ui.View()
    for button in buttons:
        view.add_item(button)

    if isinstance(interaction_or_ctx, discord.Interaction):
        if interaction_or_ctx.response.is_done():
            await interaction_or_ctx.followup.send(question.text, view=view)
        else:
            await interaction_or_ctx.response.send_message(question.text, view=view)
    else:
        await interaction_or_ctx.send(question.text, view=view)


# ===================== OYUN BİTİR =====================
async def send_end(interaction_or_ctx, user_id):
    inv = user_inventory.get(user_id, [])
    inv_text = "Envanterin boş." if not inv else "\n".join(f"- {item}" for item in inv)
    msg = f"🏁 Oyun bitti!\n\nEnvanterin:\n{inv_text}"

    if isinstance(interaction_or_ctx, discord.Interaction):
        if interaction_or_ctx.response.is_done():
            await interaction_or_ctx.followup.send(msg)
        else:
            await interaction_or_ctx.response.send_message(msg)
    else:
        await interaction_or_ctx.send(msg)

    # kullanıcıyı temizle
    user_progress.pop(user_id, None)
    user_inventory.pop(user_id, None)


# ===================== BUTON TIKLAMALARI =====================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    user_id = interaction.user.id
    if user_id not in user_progress:
        await interaction.response.send_message("Lütfen önce /start komutunu kullanarak oyuna başla.", ephemeral=True)
        return

    custom_id = interaction.data.get("custom_id", "")
    try:
        question_id, selected_index_str = custom_id.rsplit("_", 1)
        selected_index = int(selected_index_str)
    except Exception:
        await interaction.response.send_message("Geçersiz seçim.", ephemeral=True)
        return

    if question_id not in quiz_questions:
        await interaction.response.send_message("Geçersiz soru.", ephemeral=True)
        return

    question = quiz_questions[question_id]

    # Ödül varsa envantere ekle
    if question.reward:
        add_item_to_inventory(user_id, question.reward)

    # Sonraki soru
    next_question_id = None
    if 0 <= selected_index < len(question.next_questions):
        next_question_id = question.next_questions[selected_index]

    if next_question_id is None:
        await send_end(interaction, user_id)
    else:
        user_progress[user_id] = next_question_id
        await send_question(interaction, user_id)


# ===================== BOT READY =====================
@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} komut senkronize edildi.")
    except Exception as e:
        print(f"Komut senkronizasyon hatası: {e}")


bot.run(token)
