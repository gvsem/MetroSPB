from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from transliterate import translit

lineColors = [(216, 26, 54, 255),
              (10, 47, 146, 255),
              (25, 154, 91, 255),
              (220, 113, 15, 255),
              (105, 12, 115, 255)]

colorInfo = (27, 22, 151, 255)
white = (255, 255, 255)
black = (0, 0, 0)

def renderLineLogo(number):
    i = Image.new('RGB', (180, 120))
    i.paste(lineColors[number - 1], [0,0,i.size[0],i.size[1]])
    draw = ImageDraw.Draw(i)
    fontLine = ImageFont.truetype("Arial_Greek_Bold.ttf", 98)
    draw.text((115, 7), str(number), (255, 255, 255), font=fontLine)
    metroLogo = Image.open("logo_white.png").resize((90, 70))
    i.paste(metroLogo, (18,26), metroLogo)
    return i

def renderStationTable(lines, title, subtitle):

    n = 1300 # 1100
    m = 200
    zoneOffset = 35 # 10
    metroLogoSize = (135, 110)
    metroLogoOffsetH = int((m - metroLogoSize[1]) / 2)
    linesLogoSize = (145, 100)
    linesLogoOffsetH = int((m - linesLogoSize[1]) / 2)
    backgroundColor = (240, 240, 240)

    offset = -1
    lessFont = 1.0
    while offset < 20:

        fontH1 = ImageFont.truetype("FreeSet Bold.ttf", int(65 * lessFont))
        fontH2 = ImageFont.truetype("FreeSet Bold.ttf", int(60 * lessFont))

        titleWidth = fontH1.getsize(title)[0]
        subtitleWidth = fontH2.getsize(subtitle)[0]
        textWidth = max(titleWidth, subtitleWidth)
        textOffset = int((titleWidth - subtitleWidth) / 2)
        width = metroLogoSize[1] + zoneOffset + textWidth

        for line in lines:
            width += linesLogoSize[0] + zoneOffset

        offset = int((n - width) / 2)
        lessFont -= 0.1



    i = Image.new('RGB', (n, m))
    i.paste(backgroundColor, [0,0,i.size[0],i.size[1]])
    metroLogo = Image.open("logo_dark.png").resize(metroLogoSize)
    i.paste(metroLogo, (offset, metroLogoOffsetH), metroLogo)
    draw = ImageDraw.Draw(i)

    offset += metroLogoSize[0] + zoneOffset

    draw.text((offset, 27), title, black, font=fontH1)
    draw.text((offset + textOffset, 93), subtitle, black, font=fontH2)

    offset += textWidth + zoneOffset

    for line in lines:
        lineLogo = renderLineLogo(line).resize(linesLogoSize)
        i.paste(lineLogo, (offset, linesLogoOffsetH))
        offset += linesLogoSize[0] + zoneOffset

    return i

def renderStationTableFromJson(station, line_i):
    s = station["name"]
    i = [line_i] + station["interchange"]
    return renderStationTable(i, s, translit(s, "ru", reversed=True))
