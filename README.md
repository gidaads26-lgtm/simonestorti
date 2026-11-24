# Site de Simone V. Storti

Site de uma página: `site/index.html`, com CSS, JavaScript e fotos dentro do próprio arquivo.

## Pastas

- `site/`: o que vai para o servidor (`index.html`, `og-image.jpg`, `apple-touch-icon.png`, `favicon-32.png`).
- `fonte/`: o que gera o site.
  - `build.py`: dados da profissional no topo (nome, CRP, WhatsApp, Instagram, endereço, domínio, depoimentos).
  - `template_parte1.html` (CSS), `template_parte2.html` (textos e estrutura) e `template_parte3.html` (JavaScript): edite estes.
  - `montar_template.py`: junta as três partes e os ícones em `template.html`.
  - `template_limiar_v1.html`: versão anterior do visual, guardada para referência.
  - `gerar_imagens.py`: gera a imagem de compartilhamento e os ícones.
  - `fotos/`: hero.jpg, sobre.jpg, consultorio.jpg.

## Como atualizar

1. Edite os dados no topo de `fonte/build.py`, por exemplo `CRP = "12345"` e `DOMINIO = "https://www.seudominio.com.br/"`.
2. Para trocar uma foto, substitua o arquivo em `fonte/fotos/` mantendo o nome.
3. Rode:

```
cd fonte
python3 gerar_imagens.py   # só se mudou a foto do topo ou o texto da imagem de compartilhamento
python3 montar_template.py   # só se mexeu nas partes do template
python3 build.py
```

4. Suba o conteúdo de `site/` para a hospedagem.

## Pendências

- Número do CRP (`CRP` em `build.py`). Enquanto vazio, o CRP não aparece no site; o CFP exige que apareça.
- Link do Google Meu Negócio (`GOOGLE_NEGOCIO` em `build.py`). Enquanto vazio, o ícone abre uma busca no Google Maps.
- Domínio (`DOMINIO`): sem ele, o link canônico e as URLs absolutas da imagem de compartilhamento ficam vazios.
- Nota da primeira consulta (`NOTA_PRIMEIRA`), se houver.
- Depoimentos: o CFP restringe o uso por psicólogos; a seção fica oculta com a lista vazia.
- Depois de trocar o domínio, aumente `?v=1` no `og:image` do `template.html` para o WhatsApp buscar a imagem nova.
