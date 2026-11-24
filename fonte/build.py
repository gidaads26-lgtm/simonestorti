"""Gera ../site/index.html a partir de template.html.

Uso: python3 build.py
Edite os DADOS abaixo e rode de novo. Fotos ficam em fotos/ e entram no HTML em base64.
Para refazer a imagem de compartilhamento e os ícones: python3 gerar_imagens.py
"""
import base64
import html
import io
import json
from pathlib import Path
from urllib.parse import quote

from PIL import Image

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "site"

# ------------------------------------------------------------------ DADOS
NOME = "Simone V. Storti"
PRIMEIRO_NOME = "Simone"
PROFISSAO = "Psicóloga e Hipnoterapeuta"
CRP = ""  # ex.: "12345". Enquanto vazio, o CRP não aparece no site (o CFP exige que apareça).
CIDADE = "Campo Grande/MS"
ENDERECO_RUA = "R. Antônio Maria Coelho, 3595"
BAIRRO = "Jardim dos Estados"
CIDADE_NOME, UF = "Campo Grande", "MS"
CEP = "79020-210"
WHATSAPP = "556799252306"  # DDI + DDD + número, só dígitos
INSTAGRAM = "https://www.instagram.com/simonestorti_psicologa/"
# Link do perfil no Google Meu Negócio. Enquanto vazio, abre uma busca no Google Maps.
GOOGLE_NEGOCIO = ""
DOMINIO = ""  # ex.: "https://www.simonestorti.com.br/" (com barra no fim)

# Nota do passo 1 do "Como funciona". Deixe vazio se não houver.
NOTA_PRIMEIRA = ""

# Depoimentos (deixe a lista vazia para esconder a seção).
# Atenção: o CFP restringe o uso de depoimentos de pacientes por psicólogos.
# Formato: {"nome": "...", "tema": "...", "texto": "...", "foto": "fotos/arquivo.jpg" ou ""}
DEPOIMENTOS = []

DESCRICAO = (
    "Psicóloga e hipnoterapeuta em Campo Grande/MS, com atendimento online. "
    "Psicologia, hipnose clínica e regressão para ansiedade, pânico, TOC, "
    "depressão, insônia e esgotamento."
)
# ------------------------------------------------------------------------

ICON_WA = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.7-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>'
)
ICON_IG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>'
)


def img64(caminho, largura_max=1000, qualidade=80):
    im = Image.open(AQUI / caminho).convert("RGB")
    if im.width > largura_max:
        im = im.resize((largura_max, round(im.height * largura_max / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def link_wa(msg):
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


def depoimentos_html():
    if not DEPOIMENTOS:
        return ""
    cards = []
    for i, d in enumerate(DEPOIMENTOS[:3]):
        if d.get("foto"):
            av = f'<img class="avatar" src="{img64(d["foto"], 160)}" alt="" width="45" height="45">'
        else:
            av = f'<span class="avatar" aria-hidden="true">{html.escape(d["nome"][:1])}</span>'
        cards.append(
            f'<figure class="depo" data-revelar style="--i:{i};margin:0"><blockquote>'
            f'<p>{html.escape(d["texto"])}</p></blockquote><footer>{av}<span>'
            f'{html.escape(d["nome"])}<small>{html.escape(d["tema"])}</small></span></footer></figure>'
        )
    return (
        '<section class="secao" id="depoimentos"><div class="wrap"><div class="cab-secao">'
        '<h2 data-revelar>Quem já passou por aqui</h2></div>'
        f'<div class="depo-grid">{"".join(cards)}</div></div></section>'
    )


def main():
    url = DOMINIO or ""
    crp_texto = f"CRP 14/{CRP}" if CRP else ""
    endereco1 = ENDERECO_RUA
    endereco2 = f"{BAIRRO}, {CIDADE}"
    mapa = "https://www.google.com/maps/search/?api=1&query=" + quote(
        f"{ENDERECO_RUA}, {BAIRRO}, {CIDADE_NOME} - {UF}, {CEP}"
    )
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"{NOME} | {PROFISSAO}",
        "description": DESCRICAO,
        "telephone": "+" + WHATSAPP,
        "image": (url + "og-image.jpg") if url else "og-image.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ENDERECO_RUA,
            "addressLocality": CIDADE_NOME,
            "addressRegion": UF,
            "postalCode": CEP,
            "addressCountry": "BR",
        },
        "areaServed": [CIDADE, "Online"],
        "sameAs": [INSTAGRAM] + ([GOOGLE_NEGOCIO] if GOOGLE_NEGOCIO else []),
    }
    if url:
        jsonld["url"] = url

    nota = f'<p class="nota-primeira">{html.escape(NOTA_PRIMEIRA)}</p>' if NOTA_PRIMEIRA else ""

    valores = {
        "NOME": NOME,
        "PRIMEIRO_NOME": PRIMEIRO_NOME,
        "PROFISSAO": PROFISSAO,
        "PROFISSAO_MIN": PROFISSAO.lower(),
        "CIDADE": CIDADE,
        "DESCRICAO": DESCRICAO,
        "URL": url,
        "CANONICAL": f'<link rel="canonical" href="{url}">' if url else "",
        "JSONLD": json.dumps(jsonld, ensure_ascii=False),
        "WHATSAPP": WHATSAPP,
        "WA_AGENDAR": link_wa(f"Olá, {PRIMEIRO_NOME}! Vim pelo site e gostaria de agendar uma consulta de avaliação."),
        "WA_DUVIDA": link_wa(f"Olá, {PRIMEIRO_NOME}! Vim pelo site e tenho uma dúvida antes de agendar."),
        "INSTAGRAM": INSTAGRAM,
        "ENDERECO_LINHA1": endereco1,
        "ENDERECO_LINHA2": endereco2,
        "CEP": CEP,
        "MAPA": mapa,
        "GOOGLE_NEGOCIO": GOOGLE_NEGOCIO or "https://www.google.com/maps/search/?api=1&query=" + quote(f"{NOME} psicóloga, {ENDERECO_RUA}, {CIDADE_NOME} - {UF}"),
        "CRP_TEXTO": crp_texto,
        "CRP_RODAPE": f", {crp_texto}" if crp_texto else "",
        "CRP_SOBRE": f'<p class="crp" data-revelar>{NOME}, psicóloga, {crp_texto}</p>' if crp_texto else "",
        "NOTA_PRIMEIRA": nota,
        "DEPOIMENTOS": depoimentos_html(),
        "ICON_WA": ICON_WA,
        "ICON_IG": ICON_IG,
        "IMG_HERO": img64("fotos/hero.jpg", 800, 82),
        "IMG_SOBRE": img64("fotos/sobre.jpg", 800, 80),
        "IMG_CONSULTORIO": img64("fotos/consultorio.jpg", 1000, 78),
    }
    s = (AQUI / "template.html").read_text(encoding="utf-8")
    for k, v in valores.items():
        s = s.replace("{{" + k + "}}", v)
    restos = [p for p in s.split("{{")[1:]]
    if restos:
        raise SystemExit("Marcadores sem valor: " + ", ".join(r.split("}}")[0] for r in restos))
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "index.html").write_text(s, encoding="utf-8")
    print(f"index.html gerado ({len(s) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
