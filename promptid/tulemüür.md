Käesolevat prompti kasutati õppeaine „Andmeturve“ praktikumi „Tulemüür, iptables, nmap & IPv6“ käigus esitatud õpilaste lahenduste hindamiseks. 
Kuigi teiste praktikumide jaoks oli prompti sisu erinev, jäi struktuur samaks võrreldes käesoleva promptiga. Promptis oli ka vastava õpilase esitus PDF-faili kujul.

Sa pead hindama õpilase tegevust tulemüüriga seotud skripti osas. Failis võib olla ka muid ülesandeid, kuid hinda ainult 10-1 või 1. ülesannet. Failid pole tühjad. Skript peab sisaldama naabrite jaoks ühise ahela kasutamist ning vastama nendele nõuetele:
1.	INPUT ahel peab sisaldama lokaalsete ühenduste (-i lo) ning varasemalt juba lubatud ühenduste (-state ESTABLISHED,RELATED) reegleid.
2.	INPUT ahelas peavad olema reeglid naabrite ahelasse IP'de järgi suunamiseks.
3.	Naabrite ahelas peavad olema reeglid ICMP, SSH, HTTP, HTTPS ja SMTP lubamise kohta.
4.	Skriptis peab olema logimise reegel, mis logib kõik naabrite ahelasse saabunud paketid nii, et logimise teade oleks kujul: "Perenimi-NAABRID-ahel", kus siis "Perenimi" on asendatud teie nimega (nime klappimist ei pea kontrollima).
- Kõik teised ühendused/paketid peavad olema keelatud.

Maksimaalselt on õpilasel võimalik teenida selle eest 1 punkti. Hindamine pole binaarne. Oma vastuse lõpus loo tabel, kus on välja toodud nõue ning kas õpilane täitis selle. Samuti too lõpus välja kogu punktisumma.

