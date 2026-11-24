"""Monta template.html a partir de template_parte1.html (head e CSS),
template_parte2.html (corpo) e template_parte3.html (JavaScript),
trocando os marcadores [[icone]] pelos SVGs abaixo.

Uso: python3 montar_template.py && python3 build.py
"""
from pathlib import Path

AQUI = Path(__file__).parent

def svg(d):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')

ICONES = {
    "folha": svg('<path d="M5 19c0-8 6-14 14-14 0 8-6 14-14 14z"/><path d="M5 19l7-7"/>'),
    "coracao": svg('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'),
    "pin": svg('<path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>'),
    "pessoa": svg('<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>'),
    "balao": svg('<path d="M4 5.5h16v10.5H10l-6 4z"/><path d="M8 9.5h8M8 12.5h5"/>'),
    "memoria": svg('<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M4.5 4.5v3.2h3.2"/><path d="M12 8.5V12l2.8 1.8"/>'),
    "broto": svg('<path d="M12 21v-9"/><path d="M12 12c0-4 3-6.5 7.5-6.5 0 4-3 6.5-7.5 6.5z"/><path d="M12 14.5c0-3-2.5-5.5-6.5-5.5 0 3 2.5 5.5 6.5 5.5z"/>'),
    "pulso": svg('<path d="M3 12h4l2-5 4 10 2-5h6"/>'),
    "lua": svg('<path d="M19.5 14.5A8 8 0 1 1 9.5 4.5a6.3 6.3 0 0 0 10 10z"/>'),
    "corpo": svg('<circle cx="12" cy="4.8" r="2"/><path d="M12 8v7M7.5 10.5h9M12 15l-3 6M12 15l3 6"/>'),
    "premio": svg('<circle cx="12" cy="9" r="5"/><path d="M9 13.4L7.5 21l4.5-2.4 4.5 2.4-1.5-7.6"/>'),
    "relogio": svg('<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>'),
    "tela": svg('<rect x="3" y="5" width="18" height="12" rx="1.5"/><path d="M9 21h6M12 17v4"/>'),
    "ondas": svg('<path d="M3 12c2-4 3.5-4 5 0s3 4 5 0 3-4 5 0 2 2.5 3 1.5"/>'),
    "ciclo": svg('<path d="M5 12a7 7 0 0 1 12-4.9"/><path d="M19 12a7 7 0 0 1-12 4.9"/><path d="M17.5 3.5v3.8h-3.8"/><path d="M6.5 20.5v-3.8h3.8"/>'),
    "sol": svg('<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4"/>'),
    "google": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 10.2H12v3.9h5.5c-.5 2.5-2.7 4.2-5.5 4.2a6.3 6.3 0 1 1 4.1-11.1l2.8-2.8A10.2 10.2 0 1 0 22 12c0-.6-.1-1.2-.4-1.8z"/></svg>',
    "seta": '<svg class="seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

partes = [(AQUI / f"template_parte{i}.html").read_text(encoding="utf-8") for i in (1, 2, 3)]
s = "".join(partes)
for nome, codigo in ICONES.items():
    s = s.replace(f"[[{nome}]]", codigo)
if "[[" in s.split("<body>")[1]:
    raise SystemExit("Ícone sem definição: " + s.split("[[")[1].split("]]")[0])
(AQUI / "template.html").write_text(s, encoding="utf-8")
print("template.html montado")
