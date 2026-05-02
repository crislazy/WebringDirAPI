# WebringDirAPI
## A small and simple database of webrings written in Python

---

## Features
- Add a webring
- Get all webrings
- Get a webring details by name
- Report a webring
- Web UI + Docs

## Endpoints

### POST /add
Add a webring

**Body:**
```json
{
  "name": "example",
  "url": "https://example.com",
  "desc": "optional description"
}
```

**Response:**
```json
{
  "message": "added",
  "name": "example"
}
```

### GET /get
Get all webrings

### GET /get/<name>
Get one webring

**Response:**
```json
{
  "url": "https://example.com",
  "desc": "empty"
}
```

### GET /report/<name>
Report a webring

**Response:**
```json
{
  "message": "reported"
}
```

## Run locally

```bash
pip install -r requirements.txt
python main.py
```