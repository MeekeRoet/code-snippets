from pyspark.sql import DataFrame, functions as f
from typing import Iterable


def spark_melt(
    df: DataFrame,
    id_vars: Iterable[str],
    value_vars: Iterable[str],
    var_name: str = "variable",
    value_name: str = "value",
) -> DataFrame:
    """Convert Spark dataframe from wide to long format.
    """

    # Create array<struct<variable: str, value: ...>>.
    _vars_and_vals = f.array(
        *(
            f.struct(f.lit(c).alias(var_name), f.col(c).alias(value_name))
            for c in value_vars
        )
    )

    # Add to the DataFrame and explode.
    _tmp = df.withColumn("_vars_and_vals", f.explode(_vars_and_vals))

    cols = id_vars + [
        f.col("_vars_and_vals")[x].alias(x) for x in [var_name, value_name]
    ]

    return _tmp.select(*cols)