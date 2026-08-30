import argparse
from pathlib import Path
import tempfile
from urllib.request import urlopen

from wildfire_analysis.paths import BMEL_DIR


URL_TEMPLATE = "https://www.bmel-statistik.de/fileadmin/daten/0302250-{year}.pdf"


def download_bmel_pdfs(
    output_dir: Path = BMEL_DIR,
    start_year: int = 1992,
    end_year: int = 2022,
    force: bool = False,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for year in range(start_year, end_year + 1):
        destination = output_dir / f"0302250-{year}.pdf"
        if destination.exists() and not force:
            continue
        with urlopen(URL_TEMPLATE.format(year=year), timeout=60) as response:
            with tempfile.NamedTemporaryFile(dir=output_dir, delete=False) as temporary:
                temporary.write(response.read())
                temporary_path = Path(temporary.name)
        temporary_path.replace(destination)
        downloaded.append(destination)
    return downloaded


def main() -> None:
    parser = argparse.ArgumentParser(description="Download annual BMEL wildfire PDFs")
    parser.add_argument("--output-dir", type=Path, default=BMEL_DIR)
    parser.add_argument("--start-year", type=int, default=1992)
    parser.add_argument("--end-year", type=int, default=2022)
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()
    download_bmel_pdfs(
        arguments.output_dir,
        arguments.start_year,
        arguments.end_year,
        arguments.force,
    )


if __name__ == "__main__":
    main()
