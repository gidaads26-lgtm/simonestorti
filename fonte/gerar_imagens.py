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
FRASE = ["Psicologia, hipnose", "clínica e regressão"]
CRP = "CRP 14/00809-6"
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
    """Cartão 1200x630 no visual do site: porcelana, foto em arco no centro
    (a miniatura quadrada do WhatsApp corta o meio), nome serifado à esquerda,
    chamada e botão marinho à direita."""
    W, H = 1200, 630
    E = 2  # desenha em dobro e reduz no fim, para bordas suaves
    im = Image.new("RGB", (W * E, H * E), PORCELANA)

    # luz diagonal suave, como na hero
    luz = Image.new("L", (W * E, H * E), 0)
    dl = ImageDraw.Draw(luz)
    dl.polygon([(0, 0), (int(W * E * .55), 0), (int(W * E * .2), H * E), (0, H * E)], fill=150)
    luz = luz.filter(ImageFilter.GaussianBlur(120 * E))
    im.paste(Image.new("RGB", im.size, (255, 255, 255)), (0, 0), luz)
    d = ImageDraw.Draw(im)

    # foto em arco, centralizada, saindo pela base
    fw, fh = 360 * E, 560 * E
    fx, fy = (W * E - fw) // 2, 70 * E
    # moldura dourada deslocada atrás do arco
    d.rounded_rectangle([fx + 18 * E, fy - 18 * E, fx + fw + 18 * E, fy + fh + 40 * E], radius=fw // 2, outline=CHAMPANHE, width=2 * E)
    foto = Image.open(AQUI / "fotos" / "hero.jpg").convert("RGB")
    # recorte com o rosto no terço superior (ajuste CX, TOPO e LARG se trocar a foto)
    CX, TOPO, LARG = 500, 110, 700
    box = (CX - LARG // 2, TOPO, CX + LARG // 2, TOPO + int(LARG * fh / fw))
    foto = foto.crop(box).resize((fw, fh), Image.LANCZOS)
    mascara = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, fw, fh + fw], radius=fw // 2, fill=255)
    im.paste(foto, (fx, fy), mascara)

    serif = ["/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    med = ["/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"] + FONTES_REG
    f_nome = fonte(serif, 66 * E)
    f_prof = fonte(FONTES_REG, 21 * E)
    f_crp = fonte(med, 17 * E)
    f_frase = fonte(serif, 31 * E)
    f_cid = fonte(FONTES_REG, 19 * E)
    f_btn = fonte(med, 20 * E)
    OURO_TXT = (122, 94, 38)
    CINZA = (82, 90, 108)

    # esquerda: nome, profissão, CRP
    x = 64 * E
    y = 168 * E
    for linha in NOME:
        d.text((x, y), linha, font=f_nome, fill=MARINHO)
        y += 78 * E
    y += 14 * E
    d.text((x, y), PROFISSAO, font=f_prof, fill=GRAFITE)
    y += 40 * E
    d.line([(x, y), (x + 46 * E, y)], fill=CHAMPANHE, width=2 * E)
    y += 18 * E
    d.text((x, y), CRP, font=f_crp, fill=OURO_TXT)

    # direita: frase, cidade, botão
    x = (W - 64 - 330) * E
    y = 182 * E
    for linha in FRASE:
        d.text((x, y), linha, font=f_frase, fill=MARINHO)
        y += 44 * E
    y += 14 * E
    # ícone de local em círculo
    r = 15 * E
    cx, cy = x + r, y + 13 * E
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=MARINHO, width=max(2, int(1.5 * E)))
    d.ellipse([cx - 4 * E, cy - 6 * E, cx + 4 * E, cy + 2 * E], outline=MARINHO, width=max(2, int(1.5 * E)))
    d.line([(cx, cy + 2 * E), (cx, cy + 8 * E)], fill=MARINHO, width=max(2, int(1.5 * E)))
    d.text((x + 2 * r + 12 * E, y), CIDADE, font=f_cid, fill=CINZA)
    y += 66 * E
    bw, bh = 330 * E, 64 * E
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=6 * E, fill=MARINHO)
    txt = "Agende pelo WhatsApp"
    bb = d.textbbox((0, 0), txt, font=f_btn)
    d.text((x + (bw - (bb[2] - bb[0])) / 2 - bb[0], y + (bh - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f_btn, fill=PORCELANA)

    im = im.resize((W, H), Image.LANCZOS)
    im.save(SAIDA / "og-image.jpg", "JPEG", quality=86, optimize=True, progressive=True)


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
