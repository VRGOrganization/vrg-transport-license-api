# Mapeador de Campos

Ferramenta visual para mapear as posicoes dos campos no template da carteirinha usando o mouse.

## Requisitos

- Python 3.10+
- Pillow (ja e dependencia do projeto)
- tkinter (incluso na maioria das instalacoes do Python)

## Uso

```bash
# Usa o template padrao (app/assets/modelo.jpg)
python3 tools/map_fields.py

# Usa outro template
python3 tools/map_fields.py caminho/do/template.jpg

# Define o arquivo de saida
python3 tools/map_fields.py caminho/do/template.jpg -o saida.txt
```

## Controles

| Acao                | Controle                      |
|---------------------|-------------------------------|
| Marcar area         | Arrastar com botao esquerdo   |
| Nomear campo        | Popup ao soltar o botao       |
| Desfazer marcacao   | Clique direito                |
| Salvar e sair       | Tecla S                       |
| Sair sem salvar     | Tecla Q ou ESC                |

## Fluxo

1. A imagem do template abre numa janela
2. Arraste o mouse para desenhar um retangulo na area do campo
3. Ao soltar, um popup pede o nome do campo (ex: `name`, `degree`, `blood_type`)
4. A area fica com overlay vermelho e o nome aparece no canto
5. Repita para todos os campos
6. Pressione **S** para salvar

## Saida

O arquivo e salvo em `tmp/field_positions.txt` (padrao) no formato pronto para copiar no `config.py`:

```python
FIELD_POSITIONS = {
    "name"       : (280,  70),
    "institution": (280, 145),
    "degree"     : (280, 210),
    "telephone"  : (280, 285),
    "shift"      : (280, 355),
    "blood_type" : (520, 355),
}
```

Basta copiar o conteudo e substituir em `app/config.py`.
