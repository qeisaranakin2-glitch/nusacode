# NusaCode Studio

Mini compiler berbasis web. Frontend menggunakan React + Vite, backend menggunakan Python + Flask.
Bahasa mini yang didukung: `LET`, `PRINT`, angka, string, variabel, operator `+ - * /`, dan tanda kurung.

## Prasyarat
- Python 3.10+
- Node.js 18+
- npm

## Menjalankan backend (terminal 1)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Backend berjalan di http://127.0.0.1:5000

Jika PowerShell memblokir aktivasi venv, gunakan:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

## Menjalankan frontend (terminal 2)
```powershell
cd frontend
npm install
npm run dev
```
Buka URL yang ditampilkan Vite, biasanya http://localhost:5173.

## Contoh program
```text
LET nama = "Qeisar";
LET umur = 21;
PRINT "Halo " + nama;
PRINT umur + 5;
```

## Grammar ringkas
```text
program     -> statement*
statement   -> LET IDENTIFIER = expression ;
             | PRINT expression ;
expression  -> term (("+" | "-") term)*
term        -> unary (("*" | "/") unary)*
unary       -> ("+" | "-") unary | primary
primary     -> NUMBER | STRING | IDENTIFIER | "(" expression ")"
```

## Catatan akademik
Ini adalah interpreter/compiler mini edukatif: lexer menghasilkan token, parser membangun AST, semantic analyzer memeriksa variabel, lalu interpreter menjalankan AST. Versi ini belum menghasilkan machine code/native executable. Jelaskan batasan tersebut saat presentasi.
