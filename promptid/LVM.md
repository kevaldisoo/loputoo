Käesolevat prompti kasutati õppeaine „Operatsioonisüsteemid“ praktikumi „Ubuntu paigaldus ja LVM seadistus“ käigus esitatud õpilaste lahenduste hindamiseks. 
Kuigi teiste praktikumide jaoks oli prompti sisu erinev, jäi struktuur samaks võrreldes käesoleva promptiga. Promptis oli ka vastava õpilase esitus PDF-faili kujul.

Sa pead hindama õpilase tegevust Ubuntus LVM seadistamisel. Failid pole tühjad ning võivad sisaldada Lubuntu seadistamisega seotud lahendusi, mida tuleb ignoreerida. Õpilane peab lisama endale lisaks 24 GB kettale 3 GB ketta ning võtma selle kasutusele LVM füüsilise volüümina. 3 GB ketta tuleb lisada ka volüümide gruppi ja loogilisse volüümi. Volüümide grupp peab sisaldama kahte füüsilist volüümi ning vaba ala suurus peab olema 0. VMi laienduse tõestuseks peab õpilane tegema käskude sudo vgdisplay , sudo lvdisplay, lsblk ja df -h väljundist ekraanitõmmised. Hindamine on jaotatud sellisteks osadeks: 
1. vgdisplay
   - perenimi-vg on olemas (0.4p) (default nimega ubuntu-vg = 0p)
   - Free PE/Size == 0 (0.4p)
2. lvdisplay
   - perenimi-lv on olemas (0.4p) (default nimega ubuntu-lv = 0p)
3. lsblk
   - perenimi-lv mountpoint "/" ~ 25 GB (täpne suurus pole väga oluline) (0.4p)
   - perenimi-lv on mitmel kettal (sda & sdb) (0.4p)
   - sdb == 3GB (0.4p)
4. df -h
   - perenimi-lv ehk / (root) Size 25G ehk on edukalt tehtud resize2fs (0.4p)

Maksimaalne punktide arv on 2.8 punkti (vgdisplay 0.8p, lvdisplay 0.4p, lsblk 1.2p, df -h 0.4p). Ühel pildil võib olla mitu käsku, kuid võib olla ka iga käsk eraldi pildil. Oma vastuse lõpus loo tabel, kus on välja toodud käsk ning kas õpilane täitis sellega seotud ülesanded. Samuti too lõpus välja kogu punktisumma.