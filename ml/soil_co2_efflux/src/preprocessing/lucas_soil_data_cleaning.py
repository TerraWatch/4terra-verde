from preprocessing.transformations import transform_col_to_float


def clean_oc(df):
    values_to_remove = ['<0.0', '< LOD']

    # Filter out rows where 'OC' contains the values to remove
    cleaned_oc_df = df.loc[~df['OC'].isin(values_to_remove)]
    return transform_col_to_float(cleaned_oc_df, 'OC')