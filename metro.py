from PIL import Image, ImageOps
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

def stationToEnglish(t):
    # translit(s, "ru", reversed=True)
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
               (*list(u'abvgdee'), 'zh', *list(u'zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
                'y', '', 'e', 'yu','ya', *list(u'ABVGDEE'), 'ZH',
                *list(u'ZIJKLMNOPRSTUF'), 'KH', 'Z', 'CH', 'SH', 'SH', *list(u'_Y_E'), 'YU', 'YA', ' '))

    coding_dict = {source: dest for source, dest in zip(*symbols)}
    translate = lambda x: ''.join([coding_dict[i] for i in x])
    return translate(t)


def renderLineLogo(number, withWhiteBorder=False):
    i = Image.new('RGB', (180, 120))
    i.paste(lineColors[number - 1], [0,0,i.size[0],i.size[1]])
    draw = ImageDraw.Draw(i)
    fontLine = ImageFont.truetype("assets/Arial_Greek_Bold.ttf", 98)
    draw.text((115, 7), str(number), (255, 255, 255), font=fontLine)
    metroLogo = Image.open("assets/logo_white.png").resize((90, 70))
    i.paste(metroLogo, (18,26), metroLogo)
    if withWhiteBorder:
        i = ImageOps.expand(i,border=5,fill='white')
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

        fontH1 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(65 * lessFont))
        fontH2 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(60 * lessFont))

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
    metroLogo = Image.open("assets/logo_dark.png").resize(metroLogoSize)
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



def renderDirectionTable(title, subtitle, color):

    n = 1300 # 1100
    m = 200
    zoneOffset = 35 # 10
    metroLogoSize = (135, 135)
    metroLogoOffsetH = int((m - metroLogoSize[1]) / 2)
    linesLogoSize = (145, 100)
    linesLogoOffsetH = int((m - linesLogoSize[1]) / 2)
    backgroundColor = color

    offset = -1
    lessFont = 1.0
    while offset < 20:

        # fontH1 = ImageFont.truetype("FRS65.ttf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("FRS65.ttf", int(60 * lessFont))
        fontH1 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(65 * lessFont))
        fontH2 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(60 * lessFont))
        # fontH1 = ImageFont.truetype("BarnaulGroteskExtraBold-Reg.ttf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("BarnaulGroteskExtraBold-Reg.ttf", int(60 * lessFont))
        # fontH1 = ImageFont.truetype("HelveticaNeueLTW1GBdCn.otf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("HelveticaNeueLTW1GBdCn.otf", int(60 * lessFont))

        titleWidth = fontH1.getsize(title)[0]
        subtitleWidth = fontH2.getsize(subtitle)[0]
        textWidth = max(titleWidth, subtitleWidth)
        textOffset = int((titleWidth - subtitleWidth) / 2)
        width = metroLogoSize[0] + zoneOffset + textWidth

        offset = int((n - width) / 2)
        lessFont -= 0.1



    i = Image.new('RGBA', (n, m))
    i.paste(backgroundColor, [0,0,i.size[0],i.size[1]])
    metroLogo = Image.open("assets/arrow_white.png").resize(metroLogoSize)
    i.paste(metroLogo, (offset, metroLogoOffsetH), metroLogo)
    draw = ImageDraw.Draw(i)

    offset += metroLogoSize[0] + zoneOffset

    draw.text((offset, 27), title, white, font=fontH1)
    draw.text((offset + textOffset, 93), subtitle, white, font=fontH2)

    return i

def renderStationTableFromJson(station, line_i):
    s = station["name"]
    i = [line_i] + station["interchange"]
    return renderStationTable(i, s, stationToEnglish(s))


def renderWayOut(n, m):

    fontH1 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(65))
    fontH2 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(60))

    title = "Выход"
    subtitle = "Way out"
    zoneOffset = 35 # 10
    wayOutLogoSize = (135, 150)
    wayOutLogoOffsetH = int((m - wayOutLogoSize[1]) / 2)
    backgroundColor = colorInfo

    titleWidth = fontH1.getsize(title)[0]
    subtitleWidth = fontH2.getsize(subtitle)[0]
    textWidth = max(titleWidth, subtitleWidth)
    textOffset = int((titleWidth - subtitleWidth) / 2)
    width = wayOutLogoSize[0] + zoneOffset + textWidth

    offset = int((n - width) / 2)

    i = Image.new('RGBA', (n, m))
    i.paste(backgroundColor, [0,0,i.size[0],i.size[1]])
    draw = ImageDraw.Draw(i)

    draw.text((offset, 27), title, white, font=fontH1)
    draw.text((offset + textOffset, 93), subtitle, white, font=fontH2)
    offset += textWidth + zoneOffset

    wayOutLogo = Image.open("assets/wayout.png").resize(wayOutLogoSize)
    i.paste(wayOutLogo, (offset, wayOutLogoOffsetH), wayOutLogo)
    offset += wayOutLogoSize[0] + zoneOffset

    return i


def renderDirectionSplitTable(title, subtitle, line, outIsRight=True):

    n = 1600 # 1100
    m = 200
    zoneOffset = 35 # 10
    metroLogoSize = (135, 135)
    metroLogoOffsetH = int((m - metroLogoSize[1]) / 2)
    linesLogoSize = (165, 120)
    linesLogoOffsetH = int((m - linesLogoSize[1]) / 2)
    backgroundColor = lineColors[line - 1]

    offset = -1
    lessFont = 1.0
    while offset < 20:

        # fontH1 = ImageFont.truetype("FRS65.ttf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("FRS65.ttf", int(60 * lessFont))
        fontH1 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(65 * lessFont))
        fontH2 = ImageFont.truetype("assets/FreeSet Bold.ttf", int(60 * lessFont))
        # fontH1 = ImageFont.truetype("BarnaulGroteskExtraBold-Reg.ttf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("BarnaulGroteskExtraBold-Reg.ttf", int(60 * lessFont))
        # fontH1 = ImageFont.truetype("HelveticaNeueLTW1GBdCn.otf", int(65 * lessFont))
        # fontH2 = ImageFont.truetype("HelveticaNeueLTW1GBdCn.otf", int(60 * lessFont))

        titleWidth = fontH1.getsize(title)[0]
        subtitleWidth = fontH2.getsize(subtitle)[0]
        textWidth = max(titleWidth, subtitleWidth)
        textOffset = int((titleWidth - subtitleWidth) / 2)
        width = metroLogoSize[1] + zoneOffset + textWidth + linesLogoSize[0] + zoneOffset

        offset = int((n - width) / 2)
        lessFont -= 0.1

    # no center align needed here
    offset = 30

    i = Image.new('RGBA', (n, m))
    i.paste(backgroundColor, [0,0,i.size[0],i.size[1]])
    draw = ImageDraw.Draw(i)

    wayN = max(600, int(0.35 * n))
    wayOut = renderWayOut(wayN, m)

    if outIsRight:

        metroLogo = Image.open("assets/arrow_white.png").resize(metroLogoSize).rotate(90)
        i.paste(metroLogo, (offset, metroLogoOffsetH), metroLogo)

        offset += metroLogoSize[0] + zoneOffset

        lineLogo = renderLineLogo(line, True).resize(linesLogoSize)
        i.paste(lineLogo, (offset, linesLogoOffsetH))
        offset += linesLogoSize[0] + zoneOffset

        draw.text((offset, 27), title, white, font=fontH1)
        draw.text((offset, 93), subtitle, white, font=fontH2)

        i.paste(wayOut, (n - wayN, 0), wayOut)

        draw.line([(n - wayN, 0), (n - wayN, m)], fill="white", width=10)

    else:

        i.paste(wayOut, (0, 0), wayOut)
        draw.line([(wayN, 0), (wayN, m)], fill="white", width=10)

        offset = n - offset - metroLogoSize[0]

        metroLogo = Image.open("assets/arrow_white.png").resize(metroLogoSize).rotate(270)
        i.paste(metroLogo, (offset, metroLogoOffsetH), metroLogo)
        draw = ImageDraw.Draw(i)

        offset -= zoneOffset + linesLogoSize[0]
        lineLogo = renderLineLogo(line, True).resize(linesLogoSize)
        i.paste(lineLogo, (offset, linesLogoOffsetH))

        offset -= zoneOffset + textWidth

        draw.text((offset, 27), title, white, font=fontH1)
        draw.text((offset + textOffset, 93), subtitle, white, font=fontH2)


    return i