from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from transliterate import translit
import json

from metro import renderLineLogo, lineColors, renderStationTable, renderStationTableFromJson, renderDirectionTable, \
    renderDirectionSplitTable, stationToEnglish, renderWayOut

s = "Шушары"
#renderDirectionTable(s, translit(s, "ru", reversed=True), lineColors[4]).show()
s = "Спасская"
#renderWayOut(1300, 200).show()
#renderDirectionSplitTable(s, stationToEnglish(s), 4, False).show()
s = "Купчино"
#renderDirectionSplitTable(s, stationToEnglish(s), 2, False).show()
#exit(0)


for i in range(len(lineColors)):
    renderLineLogo(i+1).save("out/lines/line" + str(i + 1) + ".png", format='PNG')

with open("data.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    line_i = 0
    for line in data:
        line_i += 1
        for station in line:
            s = station["name"]
            i = [line_i] + station["interchange"]
            fn = "out/stations/" + s
            for j in i:
                fn += str(j)
            fn += ".png"
            renderStationTableFromJson(station, line_i).save(fn)

with open("data.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    line_i = 0
    for line in data:
        line_i += 1
        margin = 0
        offset = margin
        n = 1300
        m = margin + (200 + margin) * len(line)
        i = Image.new('RGB', (n, m))

        for station in line:
            st = renderStationTableFromJson(station, line_i)
            i.paste(st, (0, offset))
            offset += st.size[1] + margin

        i.save("out/views/line" + str(line_i) + ".png")


with open("data.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    line_i = 0
    for line in data:
        line_i += 1
        margin = 0
        offset = margin
        n = 1300
        m = margin + (200 + margin) * len(line)
        i = Image.new('RGB', (n, m))

        for station in line:
            st = renderStationTableFromJson(station, line_i)
            i.paste(st, (0, offset))
            offset += st.size[1] + margin

        i.save("out/views/line" + str(line_i) + ".png")


listDirections = ""

with open("data.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    line_i = 0
    for line in data:
        line_i += 1
        s = line[0]["name"]
        renderDirectionTable(s, stationToEnglish(s), lineColors[line_i - 1]).save("out/directions/line" + str(line_i) + "north.png")
        renderDirectionSplitTable(s, stationToEnglish(s), line_i, True).save("out/directions/line" + str(line_i) + "northRight.png")
        renderDirectionSplitTable(s, stationToEnglish(s), line_i, False).save("out/directions/line" + str(line_i) + "northLeft.png")
        s = line[-1]["name"]
        renderDirectionTable(s, stationToEnglish(s), lineColors[line_i - 1]).save("out/directions/line" + str(line_i) + "south.png")
        renderDirectionSplitTable(s, stationToEnglish(s), line_i, True).save("out/directions/line" + str(line_i) + "southRight.png")
        renderDirectionSplitTable(s, stationToEnglish(s), line_i, False).save("out/directions/line" + str(line_i) + "southLeft.png")

        listDirections += '<img src="out/directions/line' + str(line_i) + 'north.png" width="240">'
        listDirections += '<img src="out/directions/line' + str(line_i) + 'northRight.png" width="240">'
        listDirections += '<img src="out/directions/line' + str(line_i) + 'northLeft.png" width="240">'
        listDirections += '<img src="out/directions/line' + str(line_i) + 'south.png" width="240">'
        listDirections += '<img src="out/directions/line' + str(line_i) + 'southRight.png" width="240">'
        listDirections += '<img src="out/directions/line' + str(line_i) + 'southLeft.png" width="240">'

print(listDirections)


# s = "Площадь Восстания"
# renderStationTable([1, 3], s, translit(s, "ru", reversed=True)).save("out")

exit(0)