# Sensori

## 1. Temperatura

#### Controllo principale della zona
_Politica adottata:_
- Se la temperatura supera **`max_temp`°C**, la **zona** è a rischio **stress termico**.
- Se la temperatura scende sotto **`min_temp`°C**, la **zona** è a rischio **congelamento**.
### Pseudo-formula: Relazione tra luce incidente e temperatura interna
###### `ΔT ≈ (ΔL / 10) * k`

#### Scomposizione della formula:
- **ΔT** → variazione della temperatura in °C.
- **ΔL** → variazione della luce incidente in kilolux (kLux).
- **k** → coefficiente di assorbimento termico della zona.
    - Zone chiuse, scure, poco ventilate → **k alto** (es. 0.6 – 0.8).
    - Zone aperte, ventilate, ombreggiate → **k basso** (es. 0.3 – 0.5).
#### Esempio pratico:
- **Condizione iniziale:**
    - Temperatura = 25°C
    - Luce incidente = 18 kLux
- **Evento:**
    - La luce aumenta a 21.5 kLux → quindi `ΔL = +3.5 kLux`.
- **Calcolo ΔT:**  
    Supponendo `k = 0.6`:
`ΔT = (3.5 / 10) × 0.6 = 0.21°C`
**Risultato:**  
La temperatura stimata salirà da **25.00°C a 25.21°C**.
### Pseudo-formula: efficacia ventilatore sulla temperatura
###### `ΔT_temp = ΔT * k_fan`

#### Scomposizione della formula:
- **ΔT_temp** → diminuzione della temperatura grazie al ventilatore.
- **k_fan** → coefficiente di efficacia del ventilatore (es. 0.01 – 0.05).
    - Un `k_fan` più alto simula un ventilatore più potente o condizioni di ventilazione forzata.

## 2. Umidità del suolo 

#### Controllo principale della zona
_Politica adottata:_
- Se minore di **`min_hum`°C** -> **avvio irrigazione** (chiamata all'attuatore pompa).

### Pseudo-formula: Calcolo della perdita di umidità in relazione al calore 
###### `perdita_umidita = clamp(evap_coeff * temperatura - evap_offset, min = 0% max = 5%`

Questa relazione è **credibile** perché:
- Mantiene **range e proporzioni sensate** (il suolo non evapora del 20% in un singolo ciclo),
- Comporta **un'evaporazione progressiva** al crescere della temperatura,
- Introduce **una soglia minima implicita** (niente evaporazione significativa sotto i ~15°C).
#### Scomposizione della formula: 
- **Coefficiente di evaporazione**  
    Ogni grado di aumento **provoca una perdita di umidità dello `evap_coeff`%**.  
    _(Esempio: a 30°C → perdita di circa 1.5% per ciclo)_
- **Temperatura attuale**  
    Rilevata dal sensore di temperatura nello stesso ciclo.
- **Offset (default: -1.5)**  
    Impedisce evaporazione a basse temperature.  
    _(Esempio: a 15°C → 0.1×15 − 1.5 = 0% evaporazione.)_
- **Clamping finale**  
    Si limita la perdita massima al 5%, per evitare effetti estremi sopra i 70°C.

| Temperatura (°C) | Formula calcolata       | Perdita di umidità (%) |
| ---------------- | ----------------------- | ---------------------- |
| 10               | 0.1×10−1.5 = -0.5 → 0%  | 0%                     |
| 20               | 0.1×20−1.5 = 0.5        | 0.5%                   |
| 25               | 0.1×25−1.5 = 1.0        | 1.0%                   |
| 35               | 0.1×35−1.5 = 2.0        | 2.0%                   |
| 50               | 0.1×50−1.5 = 3.5        | 3.5%                   |
| 70               | 0.1×70−1.5 = 5.5 → 5.0% | 5.0%                   |
| 80               | 0.1×80−1.5 = 6.5 → 5.0% | 5.0%                   |
### Pseudo-formula: guadagno umidità in relazione all'irrigazione
###### `guadagno_umidità = pump_gain - perdita_umidita`

#### Principio:
- L'irrigazione **apporta** sempre un valore costante di umidità.
- L'evaporazione **sottrae** umidità, in funzione della temperatura.
- Se il **guadagno netto** è positivo, l'umidità aumenta;  
	se si azzera, l'irrigazione **bilancia esattamente** la perdita.

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

## 3. Qualità aria (CO₂)

#### Controllo principale della zona
_Politica adottata:_

- Se la CO₂ supera il limite massimo → **avvio della ventola** (chiamata all'attuatore ventilatore).

### Pseudo-formula: generazione CO₂ nell'aria
###### `ΔCO₂ = k * (C_out - C_in)`

#### Scomposizione formula: 
- **ΔCO₂** → variazione della concentrazione di CO₂ (in ppm).
- **k** → coefficiente naturale di scambio:
    - **Piccolo valore** che simula l'adattamento lento della CO₂ interna verso quella esterna.
    - Esempio pratico: in ambienti chiusi `k ≈ 0.03–0.05`.
- **C_out** → concentrazione di CO₂ esterna (di riferimento, es. 400 ppm).
- **C_in** → concentrazione di CO₂ interna (attuale).

**Comportamento:**
- Se `C_in > C_out`, **ΔCO₂ è negativo** → la CO₂ interna **diminuisce**.
- Se `C_in < C_out`, **ΔCO₂ è positivo** → la CO₂ interna **aumenta** (caso raro indoor).

### Pseudo-formula: efficacia del ventilatore sul CO₂
###### `ΔCO₂_fan = -k_fan * C_in`

#### Scomposizione formula: 
- **ΔCO₂_fan** → diminuzione di CO₂ dovuta all'azione del ventilatore.
- **k_fan** → coefficiente di efficacia della ventola:
    - Simula quanto velocemente il ventilatore abbassa la concentrazione interna di CO₂.
    - Valori tipici: `k_fan ≈ 0.01–0.05` (maggiore → ventilazione più efficiente).
- **C_in** → concentrazione di CO₂ interna attuale.

**Effetto:**  
La ventola agisce **proporzionalmente** al livello di CO₂ presente: più è alta, più il decremento è rapido.
## 4. Luce

#### Controllo principale della zona
_Politica adottata:_

- **Luce alta** → **temperatura tende ad aumentare**.

## 5. Consumo Energetico

#### Controllo principale della zona
_Politica adottata:_

- Monitoraggio del **consumo energetico** di pompe, ventilatori e altri attuatori.

### Pseudo-formula: Calcolo del consumo di energia degli attuatori

##### `Energia Istantanea (W) = Somma(consumo_W di ogni attuatore attivo)`

