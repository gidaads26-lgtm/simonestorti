"""Gera og-image.jpg (1200x630), apple-touch-icon.png (180) e favicon-32.png.

Uso: python3 gerar_imagens.py
Lê fotos/hero.jpg e grava os arquivos em ../site/ (pasta de publicação).
Ajuste NOME, FRASE e CIDADE abaixo se mudarem no build.py.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "site"
SAIDA.mkdir(exist_ok=True)

NOME = ["Simone", "V. Storti"]
PROFISSAO = "Psicóloga e Hipnoterapeuta"
FRASE = ["Psicologia e hipnose", "clínica, no mesmo", "cuidado."]
CIDADE = "Campo Grande/MS e online"

PORCELANA = (244, 245, 248)
MARINHO = (13, 35, 82)
NOITE = (8, 22, 52)
CHAMPANHE = (217, 192, 138)
GRAFITE = (42, 47, 58)

FONTES = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONTES_REG = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def fonte(lista, tam):
    for f in lista:
        if Path(f).exists():
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def og():
    W, H, LINHA = 1200, 630, 400
    im = Image.new("RGB", (W, H), PORCELANA)
    d = ImageDraw.Draw(im)
    d.rectangle([0, LINHA, W, H], fill=MARINHO)

    # foto centralizada, atravessando a linha (a miniatura do WhatsApp corta o centro)
    foto = Image.open(AQUI / "fotos" / "hero.jpg").convert("RGB")
    fw, fh = 330, 520
    # recorte com o rosto no terço superior
    cx, cy = 375, 540
    esc = fw / 520
    box = (cx - 260, cy - 250, cx + 260, cy - 250 + int(fh / esc))
    foto = foto.crop(box).resize((fw, fh), Image.LANCZOS)
    x0, y0 = (W - fw) // 2, 50
    im.paste(foto, (x0, y0))
    d = ImageDraw.Draw(im)
    # linha dourada (limiar) cruzando tudo, por cima da foto
    d.rectangle([0, LINHA - 2, W, LINHA + 1], fill=CHAMPANHE)

    f_nome = fonte(FONTES, 54)
    f_prof = fonte(FONTES_REG, 22)
    f_frase = fonte(FONTES, 30)
    f_cid = fonte(FONTES_REG, 22)
    f_selo = fonte(FONTES, 22)

    y = 120
    for linha in NOME:
        d.text((64, y), linha, font=f_nome, fill=MARINHO)
        y += 62
    d.text((64, y + 14), PROFISSAO, font=f_prof, fill=GRAFITE)

    y = 440
    for linha in FRASE:
        d.text((64, y), linha, font=f_frase, fill=(240, 242, 247))
        y += 40

    d.text((800, 130), CIDADE, font=f_cid, fill=GRAFITE)
    # selo
    sx, sy, sw, sh = 800, 456, 340, 64
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=32, fill=CHAMPANHE)
    txt = "Agende pelo WhatsApp"
    tw = d.textlength(txt, font=f_selo)
    d.text((sx + (sw - tw) / 2, sy + 17), txt, font=f_selo, fill=NOITE)

    im.save(SAIDA / "og-image.jpg", "JPEG", quality=86, optimize=True)


FONTE_S = [
    "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def icone(tam, nome):
    """Só a letra S, em marinho, sobre porcelana (lê bem em abas claras e escuras)."""
    esc = 8
    S = tam * esc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    raio = 0 if tam >= 120 else int(S * 0.22)  # o iPhone arredonda o ícone grande sozinho
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=raio, fill=(244, 245, 248, 255))
    f = fonte(FONTE_S, int(S * 0.86))
    txt = "S"
    bb = d.textbbox((0, 0), txt, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((S - tw) / 2 - bb[0], (S - th) / 2 - bb[1]), txt, font=f, fill=MARINHO)
    im = im.resize((tam, tam), Image.LANCZOS)
    if tam >= 120:
        im = im.convert("RGB")
    im.save(SAIDA / nome, "PNG", optimize=True)


if __name__ == "__main__":
    import sys
    if "--so-icones" not in sys.argv:
        og()
    icone(180, "apple-touch-icon.png")
    icone(32, "favicon-32.png")
    print("Imagens geradas em", SAIDA)
