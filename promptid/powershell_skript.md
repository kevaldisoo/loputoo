Käesolevat prompti kasutati õppeaine „Operatsioonisüsteemid“ praktikumi „Skriptimine Windowsis“ käigus esitatud õpilaste lahenduste hindamiseks. 
Kuigi teiste praktikumide jaoks oli prompti sisu erinev, jäi struktuur samaks võrreldes käesoleva promptiga. Promptis oli ka vastava õpilase esitus PowerShelli skriptifaili või tekstifaili kujul.

Sa pead hindama õpilase tegevust Windowsi PowerShelli jaoks loodud skripti osas. Failid pole tühjad ning sa pead hindama tervet faili. Skript peab eraldi väljastama kümne ülesande vastused:
1.	Masina nimi (hostname), PowerShelli versioon ja Windowsi versioon (Vihje: Ei pea leidma ühe käsuga, teil kulub selle info saamiseks arvatavasti 2 käsku.)
2.	Võrgu konfiguratsioon (IP-aadress, võrgumask (network mask), vaikelüüs (gateway), kas DHCP on lubatud ja MAC-aadress 
3.	Arvuti protsessori kirjeldus ja põhimälu RAM kogus (leiab: Win32_ComputerSystem)
4.	Graafikakaardi nimi, draiveri versioon, kuupäev ja ekraani lahutus (märksõna VideoController)
5.	Arvuti kõvaketaste informatsioon (partitsioonitabel, mitu GB on arvuti kettad mahutavuselt, mitu GB vaba ruumi on C:-kettal)
6.	PCI-siinil olevate seadmete draiverite info (kirjeldus, tootja ja versioon) 
7.	Arvutis olevad kasutajad (nimi, kirjeldus, kas on lokaalne kasutaja (LocalAccount) ja kas on keelatud (Disabled))
8.	Käimasolevate protsesside arv
9.	10 viimasena käivitatud protsessi (nimi, PID ja käivitamise aeg (StartTime)). Sorteerimise aluseks võtta parameeter StartTime.
10.	Arvuti kuupäev ja kellaaeg, formaat olgu näiteks 16. mai puhul: "16.05.2025 15:26:56"

NB! Iga küsimuse vastus peaks olema töödeldud mõistlikule inimloetavale kujule ja info peab olema vastusest kergesti leitav, sh peab olema vastuse ees küsimuse nr. Kogu peaklassi või näiteks kogu käsu Get-Process väljund küsimuse Käimasolevate protsesside arv vastuseks ilma täiendava töötlemiseta (ridade arvu kokku lugemiseta) ei ole piisav.

Maksimaalselt on õpilasel võimalik teenida selle eest 4 punkti. Iga ülesanne on väärt 0.4 punkti. Alamülesannete puhul võib anda punkte poolikult, hindamine pole binaarne. Hinda ainult skripti, tegelik väljund pole oluline. Oma vastuse lõpus loo tabel, kus on välja toodud ülesanne ning kas õpilane täitis selle. Samuti too lõpus välja kogu punktisumma.