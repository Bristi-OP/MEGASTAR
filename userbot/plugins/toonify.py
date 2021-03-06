# salute the creator/creators

import os

import requests

from userbot import CMD_HELP
from userbot.utils import admin_cmd

Mega = config.DEEP_AI if config.DEEP_AI else "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"


@borg.on(admin_cmd(pattern="toonify", outgoing=True))
async def _(event):

    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("Reply to any image or non animated sticker !")
    devent = await event.edit("Lemme download the file 😉..")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await event.edit("Reply to any image or non animated sticker !")
    devent = await event.edit("Toonifying image 😝...")
    r = requests.post(
        "https://api.deepai.org/api/toonify",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": Mega},
    )
    os.remove(media)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        await devent.edit(str(r.json()))
        return
    if "status" in r.json():
        return await devent.edit(r.json()["status"])
    try:
        output_url = r.json()["output_url"]
    except ValueError:
        await devent.edit("Server could not complete your request")
        return

    await devent.delete()
    await borg.send_message(event.chat_id, file=output_url)


CMD_HELP.update(
    {
        "toonify": ".toonify <reply to any media where a good face is there> "
        "\nIt Toonifies the face 🤣😂   (Note :-if its not working then go to deepai.org then get api and set var DEEP_AI nd key.)"
    }
)
