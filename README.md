# Photosheet

A simple Python CLI for compiling a folder of photos into a grid-based PDF photosheet.

## Features

- Compile multiple photos into a single PDF
- Automatically arrange photos into a grid
- Preserve photo aspect ratios
- Optional title, subtitle, and description
- Configurable rows and columns
- Custom output filename
- Automatically creates the output directory

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Setup

Clone the project and install the dependencies:

```bash
uv sync
```

## Usage

The basic command is:

```bash
uv run photosheet ./photos
```

By default, this creates:

```text
output/photosheet.pdf
```

### Custom output

```bash
uv run photosheet ./photos -o output/photosheet.pdf
```

### Add a title

```bash
uv run photosheet ./photos \
    --title "Photos"
```

### Add a title, subtitle, and description

```bash
uv run photosheet ./photos \
    --title "Photo Sheet" \
    --subtitle "123 Main Street, Cleveland, OH" \
    --description "Photos documenting something."
```

### Change the grid size

The default layout is **3 columns × 3 rows**.

For 4 rows:

```bash
uv run photosheet ./photos --columns 3 --rows 4
```

For 6 larger photos per page:

```bash
uv run photosheet ./photos --columns 2 --rows 3
```

## Project Structure

```text
photosheet/
├── src/
│   └── photosheet/
│       ├── __init__.py
│       └── main.py
├── photos/
├── output/
├── pyproject.toml
└── README.md
```

## Supported Images

The following image formats are currently supported:

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`
- `.heic`

Photos are automatically rotated according to their EXIF orientation and resized to fit their grid cell without stretching.

## License

Private project.
