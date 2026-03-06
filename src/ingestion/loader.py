import pandas as pd
from pathlib import Path


class DataLoaderError(Exception):
    """Custom exception for data loading errors."""
    pass


class DataLoader:

    SUPPORTED_FORMATS = (".csv", ".xlsx")

    @staticmethod
    def load(file_path: str) -> pd.DataFrame:

        path = Path(file_path)

        if not path.exists():
            raise DataLoaderError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix not in DataLoader.SUPPORTED_FORMATS:
            raise DataLoaderError(
                f"Unsupported file format {suffix}. "
                f"Supported formats: {DataLoader.SUPPORTED_FORMATS}"
            )

        try:

            if suffix == ".csv":

                try:
                    df = pd.read_csv(path, low_memory=False)

                except UnicodeDecodeError:
                    df = pd.read_csv(path, encoding="latin1", low_memory=False)

            elif suffix == ".xlsx":
                df = pd.read_excel(path)

        except Exception as e:
            raise DataLoaderError(f"Failed to load file: {e}")

        if df.empty:
            raise DataLoaderError("Loaded dataset is empty.")

        return df