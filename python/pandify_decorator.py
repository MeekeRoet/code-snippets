import pandas as pd


def pandify(class_type, suffix=""):
    """Decorator for having a standard scikit-learn transformer output dataframes.

    A standard transformer is a transformer that outputs the same number of columns
    as it receives as input.
    """

    class PandasTransformer(class_type):
        def transform(self, X: pd.DataFrame) -> pd.DataFrame:
            result = super().transform(X)
            return pd.DataFrame(
                result, index=X.index, columns=[c + suffix for c in X.columns]
            )

    PandasTransformer.__name__ = class_type.__name__
    PandasTransformer.__doc__ = class_type.__doc__

    return PandasTransformer