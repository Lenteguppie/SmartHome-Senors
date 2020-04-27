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
- Minimaal 3 female - female jumper wires

## Benodigde software:
- [Arduino IDE](https://www.arduino.cc/en/Main/Software)
- [Thingspeak](https://thingspeak.com/)
- [Hassio operating system](https://www.home-assistant.io/hassio/)
- [Appdeamon plugin in HomeAssistant](https://www.home-assistant.io/docs/ecosystem/appdaemon/)
- Code editor naar keuze voor python

## Dataflow
Voor dit project heb ik gekozen voor een master - slave constructie. Deze constructie houdt in dat de slaves de sensor data verwerken en daarnaa doorsturen naar de benodigde service. De master die haalt de data van die service af. De master verwerkt daarna de data en laat een ander apparaat er op reageren als dat nodig is. In dit project ziet dat er zo uit:

1. De esp8266 leest de sensor data uit.
2. De esp8266 stuurt de data naar een Thingspeak kanaal.
3. AppDeamon haalt elke minuut de laastst verstuurde data van het Thingspeak kanaal.
4. AppDeamon verwerkt de data.
5. AppDeamon communiceert met HASSIO om het licht aan of uit te zetten. 


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


## Slave
Om data binnen te krijgen op de app die we hebben gemaakt moeten we eerst een apparaat maken dat de sensoren uit leest. Je kan met verschillende microcontrollers en/of microprocessors sensoren uitlezen op een of andere manier. Het apparaat wat je gebruikt moet wel met WiFi kunnen verbinden en het *[HTTP(S)](https://nl.wikipedia.org/wiki/Hypertext_Transfer_Protocol "Theorie achter het HTTP protocol")* protocol ondersteunen o m de data door te kunnen sturen naar Thingsspeak.

Het apparaat moet een HTTP GET request kunnen sturen naar de links die in de Thingsspeak dashboard staan onder het tabblad *API Keys*! zoals op het plaatje hieronder!

 ![alt text](https://github.com/Lenteguppie/SmartHome-Senors/blob/master/Media/thingsspeakdashboard.PNG "Thingsspeak dashboard")


### Apparaat keuze
Voor dit project heb ik gekozen voor een NodeMCU ESP8266, dit is een microcontroller die kan verbinden met WiFi. Vooral omdat deze niet veel rekenkracht heeft en niet veel stroom gebruikt waardoor die langer mee kan gaan op een batterij dan bijvoorbeeld een Raspberry Pi. De ESP kan nog minder stroom verbruiken als je die in de deep sleep modus zet. Dit heb ik niet voor dit project gedaan omdat ik het voor nu even met de usb kabel aan mijn computer verbonden laat. Dit staat nog wel op mijn TODO lijst om het onafhankelijk te maken van de computer. De ESP8266 kan verbinden met WiFi en sensoren uitlezen wat het daarom uitstekend maakt om te gebruiken om compact die data uit te lezen.

### Sensor keuze
Voor deze demo heb ik gekozen voor een DHT11, het was in eerste instantie de bedoeling dat ik een LDR ging gebruiken, aangezien die onbedoeld in een ander project zat moest ik inproviseren. In dit geval maakt het niet heel veel uit aangezien je elke sensor kan gebruiken die je wilt. Zolang je maar een waarde in je apps.yaml in stelt waarmee je de lichten aan en uit kan laten doen bij de variabele *"toggle"*. Het is alleen even uitzoeken op welke waarde je de lampen aan en uit wil laten gaan met elke sensor. Het idee blijft hetzelfde verder.

### Slave programmeren
Om de sensordata te kunnen uitlezen moet je de microcontroller / microprocessor programeren. Voor dit voorbeeld gebruik ik een esp8266. U kunt de esp8266 programmeren in de Arduino IDE. Als u [dit bestand (.ino file)](https://github.com/Lenteguppie/SmartHome-Senors/tree/master/Slave/RoomSensor) in de Arduino IDE opent kunt u het daarmee programeren op de esp8266. Deze bestand kunt u anders vinden onder *Slave -> RoomSensor -> RoomSensor.ino*. Vergeet dit bestand niet in een gelijknamige map te zetten en de Secrets.h er in te zetten. In de Secrets.h staan alle gevoelige gegevens die u naar uw wens moet aanpassen.

De enige keer dat u de code moet aanpassen is als een een andere sensor gebruikt of als u de sensor op een andere pin aangesloten heeft.

### Sensor aansluiten
Op de meeste digitale sensoren als de DHT11 zitten 3 pinnen die je kan verbinden met een microcontroller. Hieronder kunt u zien hoe ik de DHT11 heb aangesloten op de esp.

| ESP8266       | SENSORPin     | 
|:------------- |:-------------:| 
| +3.3          | VCC           | 
| D5            | Data          | 
| GND           | GND           | 

Als de sensor aangesloten zit moet het er ongeveer zo uitzien:

 ![alt text](https://github.com/Lenteguppie/SmartHome-Senors/blob/master/Media/dhtesp.jpeg "esp8266 with dht11")