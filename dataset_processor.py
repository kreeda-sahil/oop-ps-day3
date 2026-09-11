import pandas as pd
import numpy as np

class DatasetProcessor:
    def __init__(self, path=None, df=None):

        if df is not None:
            self.df = df.copy()
        elif path is not None:
            self.df = pd.read_csv(path)
        else:
            self.df = pd.DataFrame()

    # Loading
    @classmethod
    def from_csv(cls, path):

        df = pd.read_csv(path)
        return cls(df=df)

    # Validation
    def validate_schema(self, expected_columns):

        actual_columns = set(self.df.columns)
        expected_set = set(expected_columns)
        missing = expected_set - actual_columns
        extra = actual_columns - expected_set

        result = {
            "valid": len(missing) == 0,
            "missing": list(missing),
            "extra": list(extra),
        }

        if result["valid"]:
            print("Schema validation passed. All expected columns are present.")
        else:
            print(f"Schema validation failed. Missing columns: {result['missing']}")

        if result["extra"]:
            print(f"Extra columns found: {result['extra']}")

        return result

    def validate_dtypes(self, expected_dtypes):

        mismatches = {}
        for col, expected_dtype in expected_dtypes.items():
            if col not in self.df.columns:
                mismatches[col] = {"expected": expected_dtype, "actual": "COLUMN_MISSING"}
            else:
                actual_dtype = str(self.df[col].dtype)
                if actual_dtype != expected_dtype:
                    mismatches[col] = {"expected": expected_dtype, "actual": actual_dtype}

        result = {
            "valid": len(mismatches) == 0,
            "mismatches": mismatches,
        }

        if result["valid"]:
            print("Dtype validation passed.")
        else:
            print(f"Dtype validation failed. Mismatches: {mismatches}")

        return result

    # Cleaning
    def drop_missing(self, subset=None, how="any"):

        cleaned_df = self.df.dropna(subset=subset, how=how)
        print(f"Dropped {len(self.df) - len(cleaned_df)} rows with missing values.")
        return DatasetProcessor(df=cleaned_df)

    def fill_missing(self, strategy="mean", columns=None):

        filled_df = self.df.copy()
        target_cols = columns if columns else filled_df.columns.tolist()

        for col in target_cols:
            if col not in filled_df.columns:
                continue

            if strategy == "mean":
                if pd.api.types.is_numeric_dtype(filled_df[col]):
                    filled_df[col] = filled_df[col].fillna(filled_df[col].mean())
            elif strategy == "median":
                if pd.api.types.is_numeric_dtype(filled_df[col]):
                    filled_df[col] = filled_df[col].fillna(filled_df[col].median())
            elif strategy == "mode":
                mode_val = filled_df[col].mode()
                if not mode_val.empty:
                    filled_df[col] = filled_df[col].fillna(mode_val[0])
            else:
                filled_df[col] = filled_df[col].fillna(strategy)

        print(f"Filled missing values using strategy='{strategy}' on {len(target_cols)} columns.")
        return DatasetProcessor(df=filled_df)

    def drop_duplicates(self, subset=None):

        cleaned_df = self.df.drop_duplicates(subset=subset)
        print(f"Dropped {len(self.df) - len(cleaned_df)} duplicate rows.")
        return DatasetProcessor(df=cleaned_df)

    # Transformation
    def add_column(self, name, func):

        new_df = self.df.copy()
        new_df[name] = func(new_df)
        print(f"Added column '{name}'.")
        return DatasetProcessor(df=new_df)


    # Utility
    def summary(self):

        print("DATASET SUMMARY")
        print(f"\nShape: {self.df.shape[0]} rows x {self.df.shape[1]} columns\n")

        print("Column Info")
        info_df = pd.DataFrame({
            "Dtype": self.df.dtypes,
            "Non-Null": self.df.count(),
            "Null": self.df.isnull().sum(),
            "Null%": (self.df.isnull().sum() / len(self.df) * 100).round(2),
            "Unique": self.df.nunique(),
        })
        print(info_df.to_string())

        numeric_cols = self.df.select_dtypes(include=np.number).columns
        if len(numeric_cols) > 0:
            print("\nStats ")
            print(self.df[numeric_cols].describe().to_string())


