# zoznam_scrapy

Crawler firem z portálu https://www.zoznam.sk/katalog/

## Popis projektu
Program prochází celý katalog firem na uvedeném portále a stáhne informace o jednotlivých firmách do JSON Line souboru.

Použité knihovny:
- Celý projekt je napsán ve frameworku Scrapy

## Ukázka výstupu

{"created": "2023-03-10 15:16:58.875383", "name": ["Edulka s.r.o., Bratislava"], "zoznam_url": "https://www.zoznam.sk/firma/2801424/Edulka-Bratislava", 
"address": ["Kpt. Rašu 23, 84101 Bratislava"], "label": ["Poradenstvo v oblasti zdravia a krásy. Predaj produktov pre aromaterapiu a masáže. "], 
"company_url": ["www.zoznam.sk/firma/2801424/Edulka-Bratislava"]} <br>
{"created": "2023-03-10 15:16:58.876360", "name": ["ZDRAVIE +, s.r.o., Partizánske"], "zoznam_url": "https://www.zoznam.sk/firma/3619585/ZDRAVIE-Partizanske", 
"address": ["Mostová 381/7, 95804 Partizánske"], "label": ["Terapia razovej vlny. Odstránenie bolestí chrbta, nôh, pätnej kosti, tenisového lakťa a podobne. "], 
"company_url": ["https://www.zdravieplus.eu/"]} <br>
{"created": "2023-03-10 15:16:58.877358", "name": ["Jsme 3pe z. s., Praha"], "zoznam_url": "https://www.zoznam.sk/firma/3554597/Jsme-3pe-z-s-Praha", 
"address": ["Kaprova 42/14, 11000 Praha"], "label": ["Platforma pre tých, ktorí majú alebo sa stretávajú s poruchami príjmu potravy. "], 
"company_url": ["https://www.jsme3pe.cz/"]} <br>
