def pipeline(data, *funcs):
    """Applies a sequence of functions to the input data, in the order they are provided.

    Args:
        data (any): The input data to be processed.
        *funcs (function): A variable number of functions to be applied to the input data.

    Returns:
        data (any): The result of applying all of the functions in the sequence to the input data.
    """
    result = data
    for func in funcs:
        result = func(result)
    return result


def select(*columns):
    """Returns a lambda function that can be used to select the specified columns from a pandas DataFrame.

    Args:
        *columns (str): The names of the columns to select.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame containing only the selected columns.
    """
    return lambda df: df[list(columns)]


def filter(*criteria):
    """
    Filters a Pandas DataFrame based on the specified criteria.

    Args:
        *criteria: A list of lambda functions that specify the filtering criteria.

    Returns:
        A filtered Pandas DataFrame.
    """

    def _filter(df):
        # Combine the filtering criteria using the apply method
        combined_criteria = df.apply(
            lambda row: all(criteria[i](row) for i in range(len(criteria))),
            axis=1,
        )

        # Return the filtered DataFrame
        return df[combined_criteria]

    return _filter


def rename(*mappings):
    """Returns a lambda function that can be used to rename the columns of a pandas DataFrame.

    Args:
        *mappings (str): Strings representing mappings of old column names to new column names.
            Each string should be in the format 'old_name = new_name'.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame
            with the specified column name mappings applied.
    """

    def parse_mapping(
        mapping,
    ):
        (
            old_name,
            new_name,
        ) = mapping.split(" = ")
        return (
            old_name,
            new_name,
        )

    name_map = dict(parse_mapping(mapping) for mapping in mappings)

    return lambda df: df.rename(columns=name_map)


def arrange(*columns):
    """Returns a lambda function that can be used to rearrange the rows of a pandas DataFrame.

    Args:
        *columns (str): The names of the columns to use for sorting the rows, along with the
            desired sort order (ascending or descending). Columns should be specified in the
            format "column_name [desc]".

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame
            with the rows sorted according to the specified columns.
    """

    def parse_column(column):
        if column.endswith(" desc"):
            return (
                column[:-5],
                False,
            )
        else:
            return (
                column,
                True,
            )

    def sort_df(df):
        sorted_columns = [parse_column(c) for c in columns]
        return df.sort_values(
            by=[c[0] for c in sorted_columns],
            ascending=[c[1] for c in sorted_columns],
        )

    return sort_df


def mutate(**transformations):
    """
    Applies transformations to the columns of a Pandas DataFrame.

    The transformation functions operate on the entire DataFrame, which is passed as a single argument to the function. This makes it suitable for transformations that uses pd.Series methods.
    
    If you need individual row-level processing, plese refer to the `mutate_row` function. 

    Args:
        **transformations: A dictionary of new column names and transformation functions.

    Returns:
        A transformed Pandas DataFrame.
    """

    def _mutate(df):
        for new_column, transformation in transformations.items():
            df[new_column] = transformation(df)
        return df

    return _mutate


def mutate_row(**transformations):
    """
    Applies transformations to columns of a Pandas DataFrame at a row-level.

    This means that the transformation functions are applied to each row of the DataFrame, allowing for row-level processing.

    If you need transformations that operate on the entire DataFrame, plese refer to the `mutate` function.
    
    Args:
        **transformations: A dictionary of new column names and transformation functions.

    Returns:
        A transformed Pandas DataFrame.
    """

    def _mutate(df):
        for new_column, transformation in transformations.items():
            df[new_column] = df.apply(transformation, axis=1)
        return df

    return _mutate


def distinct(*columns, keep_all=False):
    """
    Returns a lambda function that can be used to select the unique rows of a pandas DataFrame based on the specified columns.

    Args:
        *columns (str): The names of the columns to use for selecting the unique rows.
        keep_all (bool, optional): Whether or not to keep all columns in the resulting DataFrame. Defaults to False.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame containing only the unique rows based on the specified columns.
    """

    def _distinct(df):
        if keep_all:
            return df.drop_duplicates(subset=columns)
        else:
            return df[list(columns)].drop_duplicates()

    return _distinct


# group_by and summarize ---------
def group_by(*columns):
    """Returns a lambda function that can be used to group the rows of a pandas DataFrame based on the specified columns.

    Args:
        *columns (str): The names of the columns to group the rows by.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame with the rows grouped according to the specified columns."
    """

    def _group_by(df):
        return df.groupby(list(columns))

    return _group_by


def summarize(*aggregations):
    """Returns a lambda function that can be used to apply aggregations to the groups of a pandas DataFrame.

    Args:
        *aggregations (str): A string in the format "column = aggregation_function()" specifying the column to aggregate and the aggregation function to use.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame with the specified aggregations applied to each group.
    """

    def _summarize(df):
        aggregations_dict = {}
        for aggregation in aggregations:
            col, func = aggregation.split(" = ")
            func_name, col_name = func[:-1].split("(")
            aggregations_dict[col] = func_name
        return df.agg(aggregations_dict)

    return _summarize


# Joins -----------
def left_join(right, by):
    """Returns a lambda function that performs a left join of two pandas DataFrames.

    This function allows the user to specify the right DataFrame and the columns to join on. The left DataFrame is passed as input to the returned lambda function.

    Args:
        right (pandas.DataFrame): The DataFrame to join with the left DataFrame.
        by (str or list): The name(s) of the column(s) to use for the merge. Columns must have the same name in both the left and right DataFrames.

    Returns:
        function: A lambda function that takes a left DataFrame as input and returns a new DataFrame containing the left join of the left and right DataFrames.
    """

    def join(left):
        return left.merge(
            right,
            on=by,
            how="left",
        )

    return join


def anti_join(right, by):
    """Returns a lambda function that selects rows from a pandas DataFrame that do not match any rows in another DataFrame.

    This function allows the user to specify the right DataFrame and the columns to compare. The left DataFrame is passed as input to the returned lambda function.

    Args:
        right (pandas.DataFrame): The DataFrame to compare with the left DataFrame.
        by (str or list): The name(s) of the column(s) to use for the comparison. Columns must have the same name in both the left and right DataFrames.

    Returns:
        function: A lambda function that takes a left DataFrame as input and returns a new DataFrame containing the rows from the left DataFrame that do not match any rows in the right DataFrame based on the specified columns.
    """

    def join(left):
        return left[~left[by].isin(right[by])]

    return join


def tail(n=6):
    """
    Returns a lambda function that retrieves the last n rows of a pandas DataFrame.

    Args:
        n (int, optional): The number of rows to return. Defaults to 5.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame containing the last n rows.
    """

    def _tail(df):
        return df.tail(n)

    return _tail


def head(n=5):
    """
    Returns a lambda function that retrieves the first n rows of a pandas DataFrame.

    Args:
        n (int, optional): The number of rows to return. Defaults to 5.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a new DataFrame containing the first n rows.
    """

    def _head(df):
        return df.head(n)

    return _head


def to_csv(filename, index=False, **kwargs):
    """
    Returns a lambda function that saves a pandas DataFrame to a CSV file.

    Args:
        filename (str): The name of the file to save the DataFrame to.
        index (bool, optional): Whether or not to write row names (index). Defaults to False.
        **kwargs: Additional keyword arguments to be passed to pandas.DataFrame.to_csv() function.

    Returns:
        function: A lambda function that takes a DataFrame as input and saves it to a CSV file.
    """

    def _to_csv(df):
        df.to_csv(filename, index=index, **kwargs)
        return df

    return _to_csv


def squeeze():
    """
    Returns a lambda function that squeezes a pandas DataFrame into a pandas Series if it has only one column or one row.

    Returns:
        function: A lambda function that takes a DataFrame as input and returns a pandas Series if the DataFrame has only one column or one row, otherwise returns the original DataFrame.
    """

    def _squeeze(df):
        return df.squeeze()

    return _squeeze
