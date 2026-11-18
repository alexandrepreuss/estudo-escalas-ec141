"""
Converte relatorio_escalas.md em um documento Word (.docx) formatado,
com orientação paisagem para acomodar as matrizes de até 20 dias.
"""

import re
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor


def set_cell_shading(cell, color_hex: str) -> None:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=60, bottom=60, left=80, right=80) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_formatted_runs(paragraph, text: str, base_size_pt: float = 10.0) -> None:
    """Interpreta **negrito**, `código` e remove sintaxe LaTeX simples."""
    text = text.replace(r"$\le 40\text{h/sem}$", "<= 40h/sem").replace(r"$\ge 2$", ">= 2")
    tokens = re.split(r"(\*\*.*?\*\*|`.*?`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            run = paragraph.add_run(tok[2:-2])
            run.bold = True
            run.font.size = Pt(base_size_pt)
        elif tok.startswith("`") and tok.endswith("`"):
            run = paragraph.add_run(tok[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(max(base_size_pt - 0.5, 8.0))
        else:
            run = paragraph.add_run(tok)
            run.font.size = Pt(base_size_pt)


def parse_markdown_table(lines: list[str], start_idx: int) -> tuple[list[list[str]], int]:
    rows = []
    i = start_idx
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw = lines[i].strip().strip("|")
        cols = [c.strip() for c in raw.split("|")]
        # Pula linha separadora | :--- | :---: |
        if not all(re.fullmatch(r":?-+:?", c) for c in cols):
            rows.append(cols)
        i += 1
    return rows, i


def md_para_docx(md_path: str, docx_path: str) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document()

    # Configura página em Paisagem (A4) para caber tabelas de até 20 dias
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Cm(29.7)
    section.page_height = Cm(21.0)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)

    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Calibri"
    style_normal.font.size = Pt(10.5)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line or line == "---":
            i += 1
            continue

        if line.startswith("# "):
            p = doc.add_heading(level=1)
            run = p.add_run(line[2:].strip())
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue

        if line.startswith("## "):
            p = doc.add_heading(level=2)
            run = p.add_run(line[3:].strip())
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue

        if line.startswith("### "):
            p = doc.add_heading(level=3)
            add_formatted_runs(p, line[4:].strip(), base_size_pt=12.0)
            i += 1
            continue

        if line.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            add_formatted_runs(p, line[2:].strip(), base_size_pt=9.5)
            i += 1
            continue

        if line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_formatted_runs(p, line[2:].strip(), base_size_pt=10.0)
            i += 1
            continue

        if line.startswith("|"):
            rows, next_i = parse_markdown_table(lines, i)
            if rows:
                num_cols = len(rows[0])
                table = doc.add_table(rows=len(rows), cols=num_cols)
                table.style = "Table Grid"
                table.alignment = WD_TABLE_ALIGNMENT.CENTER

                is_matriz_dias = num_cols > 10 or (num_cols >= 4 and rows[0][1] == "D01")
                font_pt = 8.0 if num_cols >= 15 else (8.5 if is_matriz_dias else 9.0)

                for r_idx, row_data in enumerate(rows):
                    for c_idx, val in enumerate(row_data):
                        cell = table.cell(r_idx, c_idx)
                        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                        set_cell_margins(cell, top=40, bottom=40, left=50, right=50)

                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(0)
                        p.paragraph_format.space_after = Pt(0)

                        if r_idx == 0:
                            set_cell_shading(cell, "1B365D")
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            run = p.add_run(val.replace("**", ""))
                            run.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                            run.font.size = Pt(font_pt)
                        else:
                            if is_matriz_dias and c_idx > 0:
                                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            elif not is_matriz_dias and c_idx >= 2:
                                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

                            clean_val = val.replace("**", "")
                            if is_matriz_dias and clean_val == "F":
                                set_cell_shading(cell, "D9E2F3")
                            elif r_idx >= len(rows) - 2 and is_matriz_dias:
                                set_cell_shading(cell, "F2F2F2")

                            add_formatted_runs(p, val, base_size_pt=font_pt)

                spacer = doc.add_paragraph()
                spacer.paragraph_format.space_before = Pt(2)
                spacer.paragraph_format.space_after = Pt(4)

            i = next_i
            continue

        p = doc.add_paragraph()
        add_formatted_runs(p, line, base_size_pt=10.5)
        i += 1

    doc.save(docx_path)
    print(f"Arquivo Word gerado com sucesso em: {docx_path}")


if __name__ == "__main__":
    md_para_docx(
        "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas.md",
        "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_v3.docx",
    )
