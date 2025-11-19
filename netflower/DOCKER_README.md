# Netflower Backend - Docker Setup

## Struktura projektu
```
netflower/
├── backend/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── src/
├── cicflowmeter/
│   └── Dockerfile
└── shared-files/
    ├── PCAPs/      # Wspólny folder dla plików PCAP
    └── Netflows/   # Wspólny folder dla przekonwertowanych plików
```

## Uruchomienie z docker-compose

### Budowanie obrazów
```bash
cd backend
docker-compose build
```

### Uruchomienie
```bash
docker-compose up -d
```

### Sprawdzenie statusu
```bash
docker-compose ps
```

### Logi
```bash
# Wszystkie serwisy
docker-compose logs -f

# Tylko backend
docker-compose logs -f backend

# Tylko cicflowmeter
docker-compose logs -f cicflowmeter
```

### Zatrzymanie
```bash
docker-compose down
```

## Uruchomienie z podman-compose

### Instalacja podman-compose
```bash
pip install podman-compose
```

### Uruchomienie
```bash
cd backend
podman-compose up -d
```

## Serwisy

- **Backend**: `http://localhost:5000` - Flask API
- **CICFlowMeter**: `http://localhost:6000` - Serwis konwersji PCAP

## Wolumeny

Folder `shared-files` jest współdzielony między kontenerami:
- Backend: `/app/shared-files`
- CICFlowMeter: `/files`

## Zmienne środowiskowe

Backend akceptuje następujące zmienne:
- `UPLOAD_FOLDER` - folder dla plików PCAP (domyślnie: `/app/shared-files/PCAPs`)
- `CONVERT_FOLDER` - folder dla przekonwertowanych plików (domyślnie: `/app/shared-files/Netflows`)
- `CICFLOWMETER_URL` - URL serwisu CICFlowMeter (domyślnie: `http://cicflowmeter:6000`)
