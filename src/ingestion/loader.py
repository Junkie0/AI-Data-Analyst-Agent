import pandas as pd


class DataLoaderError(Exception):
    """Custom exception for data loading errors."""
    pass


class DataLoader:
    SUPPORTED_FORMATS = (".csv", ".xlsx")

    @staticmethod
    def load(file_path: str) -> pd.DataFrame:
        if not file_path.endswith(DataLoader.SUPPORTED_FORMATS):
            raise DataLoaderError(
                f"Unsupported file format. Supported formats: {DataLoader.SUPPORTED_FORMATS}"
            )

        try:
            if file_path.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path)
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding="latin1")
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            raise DataLoaderError(f"Failed to load file: {e}")

        if df.empty:
            raise DataLoaderError("Loaded dataset is empty.")

        return df