# SmartHome Senors
Een systeem dat zelf gemaakte temperatuur en / of LDR (Light dependent resistors) integreert met het appdeamon systeem

In dit project maak ik gebruik vaan een DHT11, dat is een sensor die temperatuur en luchtvochtigheid meet. Ik sluit de DHT11 aan op een NodeMCU ESP8266. De ESP die leest de data en stuurt deze door naar ThingsSpeak.

Thingsspeak is een platform waar je via het HTTP protocol data kan verzenden en af kan halen met behulp van een API. Ook laat Thingspeak de ontvangen data zien met mooie grafieken zodat het ook nog visueel is weergegeven.

*Voor deze repository is het wel een ***vereiste*** dat er een al bestaand smarthome systeem aanwezig is waar de appdeamon plugin op draait. Ik ga hier namelijk niet al te diep op in hoe je dit opzet aangezien er al genoeg bronnen op internet daar voor zijn.*

## Het doel
Het doel van dit project is om het home automation systeem wat ik thuis heb draaien nog meer automatisch te maken. Ik wil er voor zorgen dat de lampen reageren op de input van de sensor die ik ophaal. Dit kan een licht sensor en/of een temperatuur sensor zijn. Het doel voor later is om alles in huis automatisch te laten verlopen. Dus onder andere mijn lampen aan en uit zetten als het systeem een bepaalde waarde van de sensoren ontvangt. 
 
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

## AppDeamon setup
### YAML file
Om dit programma te laten lopen in ons smart home systeem maak ik gebruik van een zo genoemde app van appdeamon. Deze apps die worden ingeladen als je ze hebt gedefiniëert in de *apps.yaml*. Zet het volgende in de apps.yaml (waardes zonder de blokhaken!):

```yaml
sensordata:
  module: sensordata
  class: SensorData
  name: [naam van de ruimte waar de sensor in staat (String)]
  sensor_id: [ID van de sensor die je wil gebruiken (int)]
  toggle: [waarde voor (float)]
  debug: 0
```
[klik hier voor een voorbeeld apps.yaml bestand!](https://github.com/Lenteguppie/SmartHome-Senors/blob/master/Master/apps.yaml)

### App
Als de yaml klaar is dan is het nu tijd om de app in dezelfde map te zetten als het *apps.yaml* bestand. De app zelf kan je in de repository vinden onder: *Master -> sensordata.py* of [klik hier](https://github.com/Lenteguppie/SmartHome-Senors/blob/master/Master/sensordata.py "SensorData.py Source File") om naar het bestand toe te gaan.