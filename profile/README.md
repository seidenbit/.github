<p align="center">
  <img src="seidenbit-banner.svg" alt="Seidenbit – Software, IT und 3D-Druck, sauber verwoben" width="100%">
</p>

Seidenbit entwickelt quelloffene Werkzeuge für IT-Infrastruktur, Home Assistant und Elektromobilität. Wo es die Aufgabe zulässt, laufen sie lokal: im Browser, auf dem Home-Assistant-Gerät oder auf dem eigenen Server.

### IT-Infrastruktur

| Projekt | Worum es geht |
|---|---|
| **[Exitcheck](https://github.com/seidenbit/exitcheck)** | Wertet RVTools-Exporte für den Umstieg von VMware auf Proxmox VE oder Hyper-V aus: Kosten über einen frei wählbaren Zeitraum, Stolpersteine je VM und eine Aufwandsschätzung. Rechnet vollständig im Browser und sendet nichts. [Ausprobieren](https://seidenbit.github.io/exitcheck/) |

### Home Assistant

| Projekt | Worum es geht |
|---|---|
| **[Automationscheck](https://github.com/uekala/automationscheck)** | Findet Automationen, die sich gegenseitig stören – Gegenspieler, Schleifen, Selbstauslösung – und meldet sie unter *Reparaturen*. Verändert nichts. |
| **[Update-Check mit Grok](https://github.com/uekala/ha-grok-update-check)** | Blueprint: Bevor ein Update installiert wird, sucht Grok auf X, GitHub, Reddit und im Forum nach Problemen mit genau dieser Version. |
| **[Kassensturz](https://github.com/uekala/kassensturz)** | Haushaltsbuch als Home-Assistant-App: Umsätze per Open Banking oder FinTS, Verträge mit Hinweis auf Preiserhöhungen, Budgets und Prognose bis zum nächsten Gehalt. Läuft lokal. |
| **[Filen WebDAV](https://github.com/uekala/filen-webdav)** | Add-on, das Home-Assistant-Backups Ende-zu-Ende-verschlüsselt in Filen.io ablegt. |

### Elektromobilität

| Projekt | Worum es geht |
|---|---|
| **[Ladekrone](https://github.com/uekala/ladekrone)** | Günstige Ad-hoc-Ladepreise in der Umgebung aus den AFIR-Daten der Mobilithek – als Sensor in Home Assistant und als [Web-App](https://uekala.github.io/ladekrone/app/) fürs Handy. |
| **[Ladecockpit](https://github.com/uekala/ladecockpit)** | Holt die echten Tesla-Laderechnungen über die Fleet API und zeigt Kosten, Preis-Radar und nächsten Ladestopp in einer selbst gehosteten Web-App. Home Assistant ist optional. |

### Mitmachen

Fehler und Ideen bitte als Issue im jeweiligen Repository. Alle Projekte stehen unter der MIT-Lizenz.

<sub>Tesla und Supercharger sind Marken der Tesla, Inc.; Ladecockpit ist ein unabhängiges Community-Projekt. Alle genannten Marken gehören ihren Inhabern.</sub>
