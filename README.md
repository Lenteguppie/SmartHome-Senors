# SmartHome Senors
Een systeem dat zelf gemaakte temperatuur en / of LDR (Light dependent resistors) integreert met het appdeamon systeem

In dit project maak ik gebruik vaan een DHT11, dat is een sensor die temperatuur en luchtvochtigheid meet. Ik sluit de DHT11 aan op een NodeMCU ESP8266. De ESP die leest de data en stuurt deze door naar ThingsSpeak.

Thingsspeak is een platform waar je via het HTTP protocol data kan verzenden en af kan halen met behulp van een API. Ook laat Thingspeak de ontvangen data zien met mooie grafieken zodat het ook nog visueel is weergegeven.


Voor deze repository is het wel een vereiste dat er een al bestaand smarthome systeem aanwezig is waar de appdeamon plugin op draait. Ik ga hier namelijk niet al te diep op in hoe je dit opzet aangezien er al genoeg bronnen op internet daar voor zijn.
 
## Benodigde hardware:
- Raspberry Pi 3B+ of Raspberry Pi 4
- SD kaartje 32 of 64 GB is voldoende
- NodeMCU ESP8266
- DHT11 digitale temperatuur sensor

## Benodigde software:
- Arduino IDE
- Code editor naar keuze voor python
- Hassio operating system
- Appdeamon plugin in HomeAssistant

