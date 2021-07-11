from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]start$"))
async def stsrt(event):
    await event.reply(
            "**Ei, eu sou um Whisper Bot!**",
            buttons=[
                [Button.switch_inline("Conversar", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="É um robô de sussurro!",
            description="É um bot sussurro!\n(c) Morty",
            text=f"**É um sussurro bot**\n`@{me} wspr UserID|Message`\n**(c) morty**",
            buttons=[
                [Button.switch_inline(" conversar ", query="wspr ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Dê uma mensagem também!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="ID de usuário / nome de usuário inválido",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
Um sussurro foi enviado
To [{ui.user.first_name}](tg://user?id={ui.user.id})!
Clique no botão abaixo para ver a mensagem!
**Observação:** __Apenas {ui.user.first_name} pode abrir isto!__
    """
    dn = event.builder.article(
            title="Its a secret message! Sssh",
            description="É uma mensagem secreta! Sssh!",
            text=text,
            buttons=[
                [Button.inline(" Mostrar mensagem! ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="É uma mensagem secreta! Sssh",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 Esta mensagem não é para você!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Ops!\nParece que a mensagem foi excluída do meu servidor!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Bot iniciado com sucesso!")
bot.run_until_disconnected()
