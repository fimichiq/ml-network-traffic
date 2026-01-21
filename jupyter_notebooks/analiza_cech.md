# Analiza Cech Datasetów

## Podsumowanie

### Dataset główny (CICIDS2017)
- **Lokalizacja**: `/datasets/CSVs/*.csv`
- **Liczba cech**: 84 kolumny
- **Pliki**: 8 plików CSV z różnymi dniami tygodnia
- **Ostatnia kolumna**: `Label` (typ ataku)

### Dataset RDM-UQ (CIC-ToN-IoT)
- **Lokalizacja**: `/datasets/CSVs/dataset-rdm-uq/data/CIC-ToN-IoT.csv`
- **Liczba cech**: 85 kolumn
- **Dodatkowa kolumna**: `Attack` (oprócz `Label`)

## Porównanie Struktur

### Wspólne cechy (83 kolumny)

Oba datasety mają identyczne 83 pierwsze kolumny:

#### Identyfikatory przepływu (7 cech)
1. **Flow ID** - Unikalny identyfikator przepływu
2. **Src IP** - Źródłowy adres IP
3. **Src Port** - Źródłowy port
4. **Dst IP** - Docelowy adres IP
5. **Dst Port** - Docelowy port
6. **Protocol** - Protokół (TCP/UDP)
7. **Timestamp** - Znacznik czasowy

#### Podstawowe metryki przepływu (5 cech)
8. **Flow Duration** - Czas trwania przepływu
9. **Tot Fwd Pkts** - Liczba pakietów w kierunku forward
10. **Tot Bwd Pkts** - Liczba pakietów w kierunku backward
11. **TotLen Fwd Pkts** - Całkowita długość pakietów forward
12. **TotLen Bwd Pkts** - Całkowita długość pakietów backward

#### Statystyki długości pakietów Forward (4 cechy)
13. **Fwd Pkt Len Max** - Maksymalna długość pakietu forward
14. **Fwd Pkt Len Min** - Minimalna długość pakietu forward
15. **Fwd Pkt Len Mean** - Średnia długość pakietu forward
16. **Fwd Pkt Len Std** - Odchylenie standardowe długości pakietu forward

#### Statystyki długości pakietów Backward (4 cechy)
17. **Bwd Pkt Len Max** - Maksymalna długość pakietu backward
18. **Bwd Pkt Len Min** - Minimalna długość pakietu backward
19. **Bwd Pkt Len Mean** - Średnia długość pakietu backward
20. **Bwd Pkt Len Std** - Odchylenie standardowe długości pakietu backward

#### Metryki przepustowości (2 cechy)
21. **Flow Byts/s** - Bajty przepływu na sekundę
22. **Flow Pkts/s** - Pakiety przepływu na sekundę

#### Statystyki Inter-Arrival Time przepływu (4 cechy)
23. **Flow IAT Mean** - Średni czas między przepływami
24. **Flow IAT Std** - Odchylenie standardowe IAT przepływu
25. **Flow IAT Max** - Maksymalny IAT przepływu
26. **Flow IAT Min** - Minimalny IAT przepływu

#### Statystyki IAT Forward (5 cech)
27. **Fwd IAT Tot** - Całkowity czas IAT forward
28. **Fwd IAT Mean** - Średni IAT forward
29. **Fwd IAT Std** - Odchylenie standardowe IAT forward
30. **Fwd IAT Max** - Maksymalny IAT forward
31. **Fwd IAT Min** - Minimalny IAT forward

#### Statystyki IAT Backward (5 cech)
32. **Bwd IAT Tot** - Całkowity czas IAT backward
33. **Bwd IAT Mean** - Średni IAT backward
34. **Bwd IAT Std** - Odchylenie standardowe IAT backward
35. **Bwd IAT Max** - Maksymalny IAT backward
36. **Bwd IAT Min** - Minimalny IAT backward

#### Flagi TCP (4 cechy)
37. **Fwd PSH Flags** - Liczba flag PSH w kierunku forward
38. **Bwd PSH Flags** - Liczba flag PSH w kierunku backward
39. **Fwd URG Flags** - Liczba flag URG w kierunku forward
40. **Bwd URG Flags** - Liczba flag URG w kierunku backward

#### Nagłówki i pakiety/s (4 cechy)
41. **Fwd Header Len** - Długość nagłówków forward
42. **Bwd Header Len** - Długość nagłówków backward
43. **Fwd Pkts/s** - Pakiety forward na sekundę
44. **Bwd Pkts/s** - Pakiety backward na sekundę

#### Statystyki długości pakietów (5 cech)
45. **Pkt Len Min** - Minimalna długość pakietu
46. **Pkt Len Max** - Maksymalna długość pakietu
47. **Pkt Len Mean** - Średnia długość pakietu
48. **Pkt Len Std** - Odchylenie standardowe długości pakietu
49. **Pkt Len Var** - Wariancja długości pakietu

#### Liczniki flag TCP (7 cech)
50. **FIN Flag Cnt** - Liczba flag FIN
51. **SYN Flag Cnt** - Liczba flag SYN
52. **RST Flag Cnt** - Liczba flag RST
53. **PSH Flag Cnt** - Liczba flag PSH
54. **ACK Flag Cnt** - Liczba flag ACK
55. **URG Flag Cnt** - Liczba flag URG
56. **CWE Flag Count** - Liczba flag CWE
57. **ECE Flag Cnt** - Liczba flag ECE

#### Średnie rozmiary (4 cechy)
58. **Down/Up Ratio** - Stosunek download/upload
59. **Pkt Size Avg** - Średni rozmiar pakietu
60. **Fwd Seg Size Avg** - Średni rozmiar segmentu forward
61. **Bwd Seg Size Avg** - Średni rozmiar segmentu backward

#### Bulk Rate (6 cech)
62. **Fwd Byts/b Avg** - Średnia liczba bajtów bulk forward
63. **Fwd Pkts/b Avg** - Średnia liczba pakietów bulk forward
64. **Fwd Blk Rate Avg** - Średnia bulk rate forward
65. **Bwd Byts/b Avg** - Średnia liczba bajtów bulk backward
66. **Bwd Pkts/b Avg** - Średnia liczba pakietów bulk backward
67. **Bwd Blk Rate Avg** - Średnia bulk rate backward

#### Subflow (4 cechy)
68. **Subflow Fwd Pkts** - Pakiety w subflow forward
69. **Subflow Fwd Byts** - Bajty w subflow forward
70. **Subflow Bwd Pkts** - Pakiety w subflow backward
71. **Subflow Bwd Byts** - Bajty w subflow backward

#### Window Size (2 cechy)
72. **Init Fwd Win Byts** - Początkowy rozmiar okna forward
73. **Init Bwd Win Byts** - Początkowy rozmiar okna backward

#### Dodatkowe metryki (2 cechy)
74. **Fwd Act Data Pkts** - Pakiety z danymi forward
75. **Fwd Seg Size Min** - Minimalny rozmiar segmentu forward

#### Active/Idle Time (8 cech)
76. **Active Mean** - Średni czas aktywności
77. **Active Std** - Odchylenie standardowe czasu aktywności
78. **Active Max** - Maksymalny czas aktywności
79. **Active Min** - Minimalny czas aktywności
80. **Idle Mean** - Średni czas bezczynności
81. **Idle Std** - Odchylenie standardowe czasu bezczynności
82. **Idle Max** - Maksymalny czas bezczynności
83. **Idle Min** - Minimalny czas bezczynności

### Kolumny etykiet

#### Dataset główny (CICIDS2017)
84. **Label** - Szczegółowy typ ataku lub BENIGN
   - Wartości: BENIGN, DDoS, PortScan, Bot, Infiltration, Web Attack (Brute Force/XSS/SQL Injection), FTP-Patator, SSH-Patator, DoS (GoldenEye/Hulk/Slowhttptest/slowloris), Heartbleed

#### Dataset RDM-UQ (CIC-ToN-IoT)
84. **Label** - Klasyfikacja binarna (0 lub 1)
   - `0` = ruch normalny (Benign)
   - `1` = ruch złośliwy (dowolny atak)
85. **Attack** - Szczegółowy typ ataku
   - Wartości: Benign, backdoor, ddos, dos, injection, mitm, password, ransomware, scanning, xss

## Kluczowe różnice

| Aspekt | CICIDS2017 | CIC-ToN-IoT (RDM-UQ) |
|--------|------------|---------------------|
| Liczba kolumn | 84 | 85 |
| Kolumny etykiet | 1 (Label) | 2 (Label, Attack) |
| Typ Label | Multi-class (nazwy ataków) | Binary (0/1) |
| Szczegóły ataków | W kolumnie Label | W kolumnie Attack |
| Liczba plików | 8 (różne dni) | 1 plik zbiorczy |
| Struktura cech | Identyczna dla 83 pierwszych kolumn | Identyczna dla 83 pierwszych kolumn |

## Różnica między Label a Attack w RDM-UQ

Dataset **CIC-ToN-IoT (RDM-UQ)** używa **dwupoziomowego systemu etykietowania**:

### Label (kolumna 84) - Klasyfikacja binarna
- **0** = Ruch normalny (Benign)
- **1** = Ruch złośliwy (atak)
- **Zastosowanie**: Problemy klasyfikacji binarnej (wykrywanie anomalii)

### Attack (kolumna 85) - Klasyfikacja wieloklasowa
- **Benign** = Ruch normalny
- **backdoor** = Atak backdoor
- **ddos** = Distributed Denial of Service
- **dos** = Denial of Service
- **injection** = Ataki injection (SQL, Command)
- **mitm** = Man-in-the-Middle
- **password** = Ataki na hasła
- **ransomware** = Ransomware
- **scanning** = Skanowanie portów/sieci
- **xss** = Cross-Site Scripting
- **Zastosowanie**: Problemy klasyfikacji wieloklasowej (identyfikacja typu ataku)

### Porównanie z CICIDS2017

**CICIDS2017** używa **jednopolowego systemu etykietowania**:
- Tylko kolumna **Label** zawierająca szczegółowe nazwy ataków
- Wartości: BENIGN, DDoS, PortScan, Bot, Infiltration, Web Attack (Brute Force/XSS/SQL Injection), FTP-Patator, SSH-Patator, DoS (GoldenEye/Hulk/Slowhttptest/slowloris), Heartbleed
- Dla klasyfikacji binarnej trzeba ręcznie przekształcić etykiety (BENIGN vs wszystkie inne)

## Kategorie cech (grupowanie funkcjonalne)

### 1. Identyfikacja (7 cech)
- Identyfikatory przepływu i adresy sieciowe

### 2. Metryki czasowe (22 cechy)
- Flow Duration, IAT (Flow, Forward, Backward), Active/Idle time

### 3. Statystyki pakietów (22 cechy)
- Długości pakietów (min, max, mean, std, var)
- Liczba pakietów (forward, backward, total)

### 4. Flagi TCP (11 cech)
- PSH, URG, FIN, SYN, RST, ACK, CWE, ECE

### 5. Metryki przepustowości (8 cech)
- Bytes/s, Packets/s, Bulk rates

### 6. Nagłówki i segmenty (6 cech)
- Header lengths, Segment sizes

### 7. Subflow i Window (6 cech)
- Subflow statistics, Initial window bytes

### 8. Etykiety (1-2 cechy)
- Label (+ Attack dla RDM-UQ)

## Wnioski

1. **Kompatybilność cech**: Oba datasety są w pełni kompatybilne pod względem cech sieciowych (83 kolumny) - różnią się tylko sposobem etykietowania.

2. **Standard CICFlowMeter**: Wszystkie 83 cechy pochodzą z tego samego narzędzia (CICFlowMeter), co zapewnia spójność metryk.

3. **Bogactwo cech**: 83 cechy pokrywają wszystkie aspekty analizy przepływów sieciowych:
   - Charakterystyki czasowe
   - Rozmiary i częstotliwości
   - Flagi protokołu TCP
   - Wzorce komunikacji (bulk, subflow)

4. **Systemy etykietowania**:
   - **CICIDS2017**: Jedna kolumna z nazwami ataków (wymaga przekształcenia dla klasyfikacji binarnej)
   - **RDM-UQ**: Dwie kolumny - gotowa klasyfikacja binarna (Label) + szczegóły (Attack)
   - **Zaleta RDM-UQ**: Łatwiejsze w użyciu dla obu typów problemów (binary i multi-class)

5. **Możliwość łączenia**: Datasety można łatwo połączyć poprzez:
   - Mapowanie nazw ataków CICIDS2017 na kategorie RDM-UQ
   - Dodanie kolumny binarnej do CICIDS2017 (0 dla BENIGN, 1 dla reszty)
   - Usunięcie kolumny Label z RDM-UQ i użycie tylko Attack

## Zastosowania praktyczne

### Klasyfikacja binarna (wykrywanie anomalii)
- **RDM-UQ**: Użyj kolumny `Label` (0/1) bezpośrednio
- **CICIDS2017**: Przekształć `Label` → 0 dla BENIGN, 1 dla pozostałych

### Klasyfikacja wieloklasowa (identyfikacja typu ataku)
- **RDM-UQ**: Użyj kolumny `Attack`
- **CICIDS2017**: Użyj kolumny `Label` bezpośrednio
