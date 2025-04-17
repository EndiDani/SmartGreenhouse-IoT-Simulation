# Simulazione di una serra agricola smart 🌱
*Readme provvisorio in italiano*

I componenti simulati per la realizzazione della **serra agricola smart** sono principalmente **sensori** e **attuatori**. 
# Sensori

## 1. Temperatura

#### Controllo principale della zona
*Attualmente la politica da adottare:*

- Se > 35°C la **zona** è a rischio **stress termico**. 
- Se < 10°C la **zona** è a rischio **congelamento tubature.**

###### Pseudo-formula: relazione tra luce incidente e temperatura interna

###### `ΔT ≈ (ΔL / 10) * k`

`ΔT` = variazione di temperatura in °C
`ΔL` = variazione di luce in kLux (kilolux)
`k`  = coefficiente di assorbimento termico della zona (es. 0.4 - 0.8)
	*zone chiuse, più scure o con meno ventilazione = **k più alto***
	*zone ben ventilate o ombreggiate = **k più basso***

Esempio pratico: condizione iniziale con 25°C e luce incidente a 18kLux. La luce aumenta a 21.5kLux ->  `ΔL = +3.5`. Supponendo che  `k = 0.5`: 
- `ΔT = (3.5 / 10) * 0.6 = 0.21°C`
La temperatura stimata salirà da 25°C a circa **25.21°C**.

###### Pseudo-formula: efficacia ventilatore sulla temperatura
###### `ΔT_fan = – k_temp × `ΔT`

`k_temp` = coefficiente che simula l'effetto del ventilatore sull'aria.

## 2. Umidità del suolo 
*Suggerito in zona A e B*

- Se < 30% -> **avvio irrigazione** (chiamata all'attuatore pompa).
- *Si iscrive al topic della temperatura*: 
	- troppo caldo -> evapora prima -> irrigazione più frequente

###### Pseudo-formula: Calcolo della perdita di umidità in relazione al calore 
###### `perdita_umidita = 0.1 * temperatura - 1.5   (limitata tra 0 e 5%)`

Questa relazione è credibile in quanto mantiene **range e proporzioni sensate** (il suolo non evapora di 20% in un minuto), ha un comportamento **progressivo** e tiene conto di una fisica semplificata (più caldo = più evaporazione).

**Scomposizione della formula**: 
- **Coefficiente di sensibilità** `(0.1)`: Per **ogni grado in più, perdo il 0.1 di umidità**. 
	*Quindi se da 25°C passo a 30°C, sto dicendo che **in 30°C perdo circa 3.0%**.*
	*È possibile cambiarlo in base anche al tipo di pianta (alcune piante trattengono di più)*
	*Nota bene: possibile modularlo per ogni zona in maniera adatta*
- **Temperatura attuale**: la temperatura misurata nello stesso istante dal sensore termico. 
- **Offset di base**: Serve a **non avere evaporazione a temperature basse**. 
	*Se `T = 15°C` -> `0.1 * 15°C - 1.5 = 0%`*
	È quindi una **soglia minima di attivazione** implicita:  
	*la perdita parte solo **dopo i 15°C circa**.*

| Temperatura | Formula            | Perdita (%) |
| ----------- | ------------------ | ----------- |
| 10°C        | 0.1×10 - 1.5       | 0%          |
| 20°C        | 0.1×20 - 1.5 = 0.5 | 0.5%        |
| 25°C        | 0.1×25 - 1.5 = 1.0 | 1.0%        |
| 35°C        | 0.1×35 - 1.5 = 2.0 | 2.0%        |
###### Pseudo-formula: guadagno umidità in relazione all'irrigazione
###### `guadagno_umidità = irrigazione (5%) - perdita_umidita`

Per comprendere questa formula bisogna distinguere nettamente: 
- **Evaporazione del suolo**: aumenta con la temperatura secondo la formula sopra riportata. 
- **Irrigazione**: costante, pari **al valore altissimi di evaporazione**: in questo modo la pompa può controbilanciare anche i picchi di calore. 

- **Se `perdita_umidita` < 5 %**, `guadagno_umidità` > 0 → **umidità sale**
- **Se `perdita_umidita` ≥ 5 %**,  `guadagno_umidità` = 0 → la pompa bilancia perfettamente la perdita, ma non può fare di più

| Temperatura (°C) | Evaporazione (%) = clamp(0.1×T−1.5,0–5) | pump_gain (%) | net_gain (%) |
| ---------------- | --------------------------------------- | ------------- | ------------ |
| 10               | 0 %                                     | 5 %           | +5.0 %       |
| 20               | 0.5 % = 0.1×20−1.5                      | 5 %           | +4.5 %       |
| 25               | 1.0 % = 0.1×25−1.5                      | 5 %           | +4.0 %       |
| 30               | 1.5 % = 0.1×30−1.5                      | 5 %           | +3.5 %       |
| 35               | 2.0 % = 0.1×35−1.5                      | 5 %           | +3.0 %       |
| 40               | 2.5 % = 0.1×40−1.5                      | 5 %           | +2.5 %       |
| 50               | 3.5 % = 0.1×50−1.5                      | 5 %           | +1.5 %       |
| 60               | 4.5 % = 0.1×60−1.5                      | 5 %           | +0.5 %       |
| 70               | 5.0 % (clamp)                           | 5 %           | 0.0 %        |
| 80               | 5.0 % (clamp)                           | 5 %           | 0.0 %        |


> **Aggiornamenti futuri**: implementare la pioggia. 


## 3. Qualità aria (CO₂)
*Suggerito in zona D*

- Se la CO₂ è alta -> **avvio ventola** (chiamata all'attuatore ventola).
- *Si iscrive al topic finestra e ventilatore*
	 - se è chiusa e CO₂ è alta -> anomalia!

###### Pseudo-formula: generazione CO₂ nell'aria
###### `ΔCO₂ = k * (C_out - C_in)`

**Scomposizione formula**: 
- **Coefficiente naturale** `k`: valore piccolo che fa sì che il sistema tenda lentamente al valore esterno (*nella simulazione, un valore randomico*).
- Se C_in > C_out, ΔCO₂ è negativo (la CO₂ scende), altrimenti positivo.

###### Pseudo-formula: efficacia del ventilatore sul CO₂
###### `ΔCO₂_fan = -k_fan * C_in`

**Scomposizione formula**: 
- **Coefficiente potenza ventilatore** `k_fan`: determina quanto rapidamente la ventola abbassa la CO₂.
- Calcolato sullo stato attuale di CO₂ nell'aria, simula un ricambio continuo.
## 4. Luce
*Suggerito in zona A e B*

- Se c'è troppa luce -> chiusura tende (*opzionale*)
- *Si iscrive alla temperatura*
	- luce alta -> temperatura alta 

## 5. Consumo energetico
*Consigliato in zona E*

- Rileva quanto pompe o ventilatore consumano e se consumano troppo.
- *Si iscrive a tutti gli altri*
	- se pompa consuma ma non c'è irrigazione -> anomalia.

###### Pseudo-formula: Calcolo del consumo di energia degli attuatori
###### `Energia (Wh) = Potenza(W) * Tempo (in ore)`


# Interazioni tra sensori

## 1. Sensore di Luce -> Temperatura

Se entra troppa luce la temperatura nella zona si alza. 
**Effetto**: il sensore di temperatura riceve la luce e si regola con **una variazione positiva**.

## 2. Temperatura -> Umidità del suolo

Se fa più caldo ci sta maggiore **evaporazione**. 
**Effetto**: se il sensore di temperatura segnala valori alti, il sensore di umidità **abbassa più rapidamente** i suoi valori. 

## 3. Umidità del suolo -> Attuatore (Pompa)

Se l'umidità scende troppo è **necessario irrigare**. 
**Effetto**: il sensore attiva un nodo pompa che poi può essere tracciato dal sensore energetico. 
**Esempio**: `humidity < 30%` → attivatore pompa = `True`

## 4. Pompa attiva -> Umidità sale

L'irrigazione cambia lo stato dell'ambiente
**Effetto**: il sensore riceve "*evento pompa attiva*" -> umidità del sensore aumenta.
**Esempio**: `+10%` di umidità dopo attivazione.

## 5. CO₂ -> Ventilazione

Se l'aria è viziata c'è bisogno di un **ricircolo**. 
**Effetto**: sopra la soglia (es. 120 ppm), si attiva un attuatore che simula apertura finestre o ventole. 
*Se è presente la finestra, la mancata apertura può essere considerata anomalia*.

## 6. Attuatori attivi -> Consumo energetico

Le pompe e le ventole consumano energia. 
**Effetto**: se uno o più attuatori sono attivi, il consumo aumenta.
*Una possibile anomalia può essere un attuatore disattivato ma un consumo energetico alto*.
