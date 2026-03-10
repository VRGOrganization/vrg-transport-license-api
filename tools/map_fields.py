"""Ferramenta visual para mapear posicoes dos campos no template da carteirinha.

Abre a imagem do template e permite desenhar retangulos com o mouse para
demarcar as areas dos campos. Cada area recebe um overlay vermelho e um nome
digitado via popup. Ao finalizar, gera um arquivo txt com as coordenadas
no formato usado em config.py.

Uso:
    python3 tools/map_fields.py
    python3 tools/map_fields.py caminho/do/template.jpg
    python3 tools/map_fields.py caminho/do/template.jpg -o saida.txt

Controles:
    Arrastar (botao esquerdo) — desenha o retangulo do campo
    Soltar o botao            — abre popup para nomear o campo
    Clique direito            — remove a ultima marcacao
    Tecla S                   — salva e sai
    Tecla Q / ESC             — sai sem salvar

Requisitos:
    - Python 3.10+ com tkinter (incluso na maioria das instalacoes)
    - Pillow
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog

from PIL import Image, ImageTk

ASSETS_DIR = Path(__file__).resolve().parent.parent / "app" / "assets"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "tmp" / "field_positions.txt"

OVERLAY_COLOR = "#ff0000"
OVERLAY_STIPPLE = "gray25"
LABEL_COLOR = "yellow"
LABEL_OUTLINE = "black"
LABEL_FONT = ("monospace", 12, "bold")


class FieldMapper:
    def __init__(self, image_path: Path, output_path: Path) -> None:
        self.image_path = image_path
        self.output_path = output_path
        # Cada field: (name, x1, y1, x2, y2)
        self.fields: list[tuple[str, int, int, int, int]] = []
        # Cada marker: (rect_id, label_id)
        self.markers: list[tuple[int, int]] = []

        self._drag_start: tuple[int, int] | None = None
        self._drag_rect: int | None = None

        self.root = tk.Tk()
        self.root.title(f"Map Fields — {image_path.name}")

        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(
            self.root,
            width=self.image.width,
            height=self.image.height,
        )
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.status = tk.Label(
            self.root,
            text="Arraste para marcar area | Clique direito: desfazer | S: salvar | Q: sair",
            anchor=tk.W,
            padx=5,
        )
        self.status.pack(fill=tk.X)

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Button-3>", self._on_undo)
        self.root.bind("<Key-s>", self._on_save)
        self.root.bind("<Key-S>", self._on_save)
        self.root.bind("<Key-q>", self._on_quit)
        self.root.bind("<Key-Q>", self._on_quit)
        self.root.bind("<Escape>", self._on_quit)

    def run(self) -> None:
        self.root.mainloop()

    def _on_press(self, event: tk.Event) -> None:
        self._drag_start = (event.x, event.y)
        self._drag_rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline=OVERLAY_COLOR, width=2, dash=(4, 2),
        )

    def _on_drag(self, event: tk.Event) -> None:
        if self._drag_start and self._drag_rect:
            x0, y0 = self._drag_start
            self.canvas.coords(self._drag_rect, x0, y0, event.x, event.y)

    def _on_release(self, event: tk.Event) -> None:
        if not self._drag_start or not self._drag_rect:
            return

        x0, y0 = self._drag_start
        x1, y1 = event.x, event.y

        # Remove o retangulo temporario de arraste
        self.canvas.delete(self._drag_rect)
        self._drag_rect = None
        self._drag_start = None

        # Normaliza coordenadas (canto superior esquerdo -> inferior direito)
        left, right = min(x0, x1), max(x0, x1)
        top, bottom = min(y0, y1), max(y0, y1)

        # Ignora areas muito pequenas (clique acidental)
        if abs(right - left) < 5 or abs(bottom - top) < 5:
            return

        name = simpledialog.askstring(
            "Nome do campo",
            f"Area: ({left}, {top}) -> ({right}, {bottom})\n\nNome do campo:",
            parent=self.root,
        )
        if not name:
            return

        name = name.strip()
        if not name:
            return

        # Overlay vermelho semitransparente
        rect = self.canvas.create_rectangle(
            left, top, right, bottom,
            fill=OVERLAY_COLOR, stipple=OVERLAY_STIPPLE,
            outline=OVERLAY_COLOR, width=2,
        )
        # Label com nome do campo (outline + texto)
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        outline_ids = []
        for dx, dy in offsets:
            oid = self.canvas.create_text(
                left + 4 + dx, top + 2 + dy,
                text=name, anchor=tk.NW, fill=LABEL_OUTLINE,
                font=LABEL_FONT,
            )
            outline_ids.append(oid)
        label = self.canvas.create_text(
            left + 4, top + 2,
            text=name, anchor=tk.NW, fill=LABEL_COLOR,
            font=LABEL_FONT,
        )

        self.fields.append((name, left, top, right, bottom))
        self.markers.append((rect, outline_ids, label))
        self._update_status()

    def _on_undo(self, event: tk.Event) -> None:
        if not self.fields:
            return
        removed = self.fields.pop()
        rect, outline_ids, label = self.markers.pop()
        self.canvas.delete(rect)
        for oid in outline_ids:
            self.canvas.delete(oid)
        self.canvas.delete(label)
        self._update_status()

    def _on_save(self, event: tk.Event) -> None:
        if not self.fields:
            messagebox.showinfo("Aviso", "Nenhum campo marcado.")
            return

        filename = simpledialog.askstring(
            "Nome do arquivo",
            "Nome do arquivo de saida (sem extensao):",
            initialvalue=self.output_path.stem,
            parent=self.root,
        )
        if not filename:
            return

        filename = filename.strip()
        if not filename:
            return

        if not filename.endswith(".txt"):
            filename += ".txt"
        self.output_path = self.output_path.parent / filename

        self._write_output()
        self.root.destroy()

    def _on_quit(self, event: tk.Event) -> None:
        self.root.destroy()

    def _update_status(self) -> None:
        count = len(self.fields)
        names = ", ".join(f[0] for f in self.fields)
        self.status.config(text=f"Campos: {count} [{names}] | S: salvar | Q: sair")

    def _write_output(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        max_name_len = max(len(f[0]) for f in self.fields)

        lines = ["FIELD_POSITIONS = {"]
        for name, x1, y1, x2, y2 in self.fields:
            padded = f'"{name}"'.ljust(max_name_len + 2)
            lines.append(f"    {padded}: ({x1:>3}, {y1:>3}),  # area: ({x1}, {y1}) -> ({x2}, {y2})")
        lines.append("}")
        lines.append("")

        content = "\n".join(lines)
        self.output_path.write_text(content)

        print(f"\n{'=' * 50}")
        print(content)
        print(f"{'=' * 50}")
        print(f"Salvo em: {self.output_path}")


def _choose_image() -> Path:
    """Lista imagens em assets/ e pede para o usuario escolher."""
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    images = sorted(
        f for f in ASSETS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    )

    if not images:
        print(f"Nenhuma imagem encontrada em: {ASSETS_DIR}")
        sys.exit(1)

    print("Imagens disponiveis em assets/:\n")
    for i, img in enumerate(images, 1):
        print(f"  [{i}] {img.name}")
    print()

    while True:
        choice = input("Escolha a imagem (numero): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(images):
            return images[int(choice) - 1]
        print("  Opcao invalida.")


def main() -> None:
    output_path = DEFAULT_OUTPUT

    args = sys.argv[1:]

    if "-o" in args:
        idx = args.index("-o")
        output_path = Path(args[idx + 1])
        args = args[:idx] + args[idx + 2:]

    if args:
        image_path = Path(args[0])
        if not image_path.exists():
            print(f"Arquivo nao encontrado: {image_path}")
            sys.exit(1)
    else:
        image_path = _choose_image()

    print(f"\nTemplate: {image_path}")
    print(f"Output:   {output_path}")
    print(f"Arraste na imagem para marcar as areas dos campos.\n")

    mapper = FieldMapper(image_path, output_path)
    mapper.run()


if __name__ == "__main__":
    main()
