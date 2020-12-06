import io

import aiohttp
import urllib3
from PIL import Image, ImageFont, ImageDraw

urllib3.disable_warnings()
http = urllib3.PoolManager()


def GetBlendColor(Rarity):
    if Rarity.lower() == "frozen":
        return 148, 223, 255
    elif Rarity.lower() == "lava":
        return 234, 141, 35
    elif Rarity.lower() == "legendary":
        return 198, 71, 35
    elif Rarity.lower() == "dark":
        return 251, 34, 223
    elif Rarity.lower() == "starwars":
        return 231, 196, 19
    elif Rarity.lower() == "marvel":
        return 197, 51, 52
    elif Rarity.lower() == "dc":
        return 84, 117, 199
    elif Rarity.lower() == "icon":
        return 54, 183, 183
    elif Rarity.lower() == "shadow":
        return 113, 113, 113
    elif Rarity.lower() == "epic":
        return 177, 91, 226
    elif Rarity.lower() == "rare":
        return 73, 172, 242
    elif Rarity.lower() == "uncommon":
        return 96, 170, 58
    elif Rarity.lower() == "common":
        return 190, 190, 190
    elif Rarity == "slurp":
        return 41, 150, 182
    else:
        return 255, 255, 255


async def GenerateCard(Item):
    card = Image.new("RGB", (300, 545)).convert("RGBA")
    Draw = ImageDraw.Draw(card)
    Name = Item["name"]
    if not Name:
        Name = "Placeholder"
    Rarity = Item["rarity"]["value"].lower()
    if not Rarity:
        Rarity = "common"
    displayRarity = Item["rarity"]["displayValue"]
    if not displayRarity:
        displayRarity = "common"
    blendColor = GetBlendColor(Rarity)
    Category = Item["type"]["value"]
    if not Category:
        Category = "Placeholder"
    displayCategory = Item["type"]["displayValue"]
    if not displayCategory:
        displayCategory = "Placeholder"

    try:
        layer = Image.open(f"assets/Images/card_inside_{Rarity.lower()}.png")
    except:
        layer = Image.open("assets/Images/card_inside_common.png")

    card.paste(layer)

    if Item["images"]["featured"] is not None:
        Icon = Item["images"]["featured"]
    else:
        if Item["images"]["icon"] is not None:
            Icon = Item["images"]["icon"]
        else:
            if Item["images"]["smallIcon"] is not None:
                Icon = Item["images"]["smallIcon"]
            else:
                if Item["images"]["other"] is not None:
                    Icon = Item["images"]["other"]
                else:
                    Icon = "https://i.imgur.com/JPuoAAu.png"
    # Download the Item icon
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(Icon) as data:
                Icon = Image.open(io.BytesIO(await data.read()))
    except Exception as ex:
        print("DOWNLOAD ITEM ICON ERROR", ex)
        pass
    if (Category == "outfit") or (Category == "emote"):
        ratio = max(285 / Icon.width, 365 / Icon.height)
    elif Category == "wrap":
        ratio = max(230 / Icon.width, 310 / Icon.height)
    else:
        ratio = max(310 / Icon.width, 390 / Icon.height)
    Icon = Icon.resize((int(Icon.width * ratio), int(Icon.height * ratio)), Image.ANTIALIAS)
    Icon = Icon.convert("RGBA")
    Middle = int((card.width - Icon.width) / 2)  # Get the middle of card and icon
    # Paste the image
    if (Category == "outfit") or (Category == "emote"):
        card.paste(Icon, (Middle, 0), Icon)
    else:
        card.paste(Icon, (Middle, 15), Icon)

    try:
        layer = Image.open(f"assets/Images/card_faceplate_{Rarity.lower()}.png")
        card.paste(layer, layer)
    except:
        layer = Image.open("assets/Images/card_faceplate_common.png")
        card.paste(layer, layer)

    BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 30)
    textWidth = BurbankBigCondensed.getsize(f"{displayCategory}")[0]

    Middle = int((card.width - textWidth) / 2)
    Draw.text((Middle, 370), f"{displayCategory}", blendColor,
              font=BurbankBigCondensed)

    FontSize = 56
    while ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize).getsize(Name)[0] > 265:
        FontSize -= 1

    BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize)
    textWidth = BurbankBigCondensed.getsize(Name)[0]
    change = 56 - FontSize

    Middle = int((card.width - textWidth) / 2)
    Top = 415 + change / 2

    Draw.text((Middle, Top), Name, (255, 255, 255), font=BurbankBigCondensed)

    try:
        set = Item["set"]["text"]
        FontSize = 56
        while ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize).getsize(set)[0] > 265:
            FontSize -= 1

        BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize)
        textWidth = BurbankBigCondensed.getsize(set)[0]
        change = 56 - FontSize

        Middle = int((card.width - textWidth) / 2)
        Top = 470 + change / 2

        Draw.text((Middle, Top), set, (255, 255, 255), font=BurbankBigCondensed)
    except:
        pass

    return card


def GetMiddle(x, y):
    return (x - y) / 2
