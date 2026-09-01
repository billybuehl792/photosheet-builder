#!/usr/bin/env python3

import argparse
import math
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def get_images(folder: Path):
    return sorted(
        [
            p
            for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )


def draw_image(c, image_path, x, y, width, height):
    """Fit an image inside a box without stretching it."""
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img)
        img_width, img_height = img.size

    image_ratio = img_width / img_height
    box_ratio = width / height

    if image_ratio > box_ratio:
        draw_width = width
        draw_height = width / image_ratio
    else:
        draw_height = height
        draw_width = height * image_ratio

    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2

    c.drawImage(
        str(image_path),
        draw_x,
        draw_y,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        anchor="c",
    )


def draw_header(c, title, subtitle, description, page_width, page_height, margin):
    """Draw the optional page header and return the amount of space used."""
    current_y = page_height - margin

    if title:
        c.setFont("Helvetica-Bold", 18)
        c.drawString(margin, current_y, title)
        current_y -= 24

    if subtitle:
        c.setFont("Helvetica", 11)
        c.drawString(margin, current_y, subtitle)
        current_y -= 18

    if description:
        c.setFont("Helvetica", 9)

        # Wrap description to the available width.
        max_width = page_width - (2 * margin)
        words = description.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = (
                f"{current_line} {word}".strip()
            )

            if stringWidth(test_line, "Helvetica", 9) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        for line in lines:
            c.drawString(margin, current_y, line)
            current_y -= 13

        current_y -= 5

    # Divider line if anything was added.
    if title or subtitle or description:
        c.line(
            margin,
            current_y,
            page_width - margin,
            current_y,
        )
        current_y -= 15

    return current_y


def create_photosheet(
    input_folder: Path,
    output_file: Path,
    columns: int = 3,
    rows: int = 3,
    margin: float = 36,
    gap: float = 10,
    title: str | None = None,
    subtitle: str | None = None,
    description: str | None = None,
):
    images = get_images(input_folder)

    if not images:
        raise ValueError(f"No images found in {input_folder}")

    page_width, page_height = letter
    photos_per_page = columns * rows

    c = canvas.Canvas(str(output_file), pagesize=letter)

    cell_width = 0
    cell_height = 0
    photo_top = 0

    for index, image_path in enumerate(images):
        position = index % photos_per_page

        if position == 0:
            if index != 0:
                c.showPage()

            # Draw header on each page.
            photo_top = draw_header(
                c,
                title,
                subtitle,
                description,
                page_width,
                page_height,
                margin,
            )

            # Available space for photos.
            photo_bottom = margin

            available_height = photo_top - photo_bottom

            cell_width = (page_width - (2 * margin) -
                          ((columns - 1) * gap)) / columns

            cell_height = (available_height - ((rows - 1) * gap)) / rows

        col = position % columns
        row = position // columns

        x = margin + col * (cell_width + gap)

        y = (photo_top - cell_height - row * (cell_height + gap))

        draw_image(
            c,
            image_path,
            x,
            y,
            cell_width,
            cell_height,
        )

    c.save()

    print(f"Created: {output_file}")
    print(f"Photos:  {len(images)}")
    print(f"Pages:   {math.ceil(len(images) / photos_per_page)}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a grid PDF from a folder of photos."
    )

    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing photos",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/photosheet.pdf"),
        help="Output PDF filename (default: output/photosheet.pdf)",
    )

    parser.add_argument(
        "--columns",
        type=int,
        default=2,
        help="Number of photo columns (default: 2)",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=3,
        help="Number of photo rows (default: 3)",
    )

    parser.add_argument(
        "--title",
        help="Optional title",
    )

    parser.add_argument(
        "--subtitle",
        help="Optional subtitle",
    )

    parser.add_argument(
        "--description",
        help="Optional description",
    )

    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Folder not found: {args.folder}")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.columns < 1 or args.rows < 1:
        raise SystemExit("Columns and rows must be at least 1.")

    create_photosheet(
        args.folder,
        args.output,
        columns=args.columns,
        rows=args.rows,
        title=args.title,
        subtitle=args.subtitle,
        description=args.description,
    )


if __name__ == "__main__":
    main()
