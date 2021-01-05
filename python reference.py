df.loc[df['column name'] condition, 'new column name'] = 'value if condition is met'

def vc_good(df, label="a", digit=2):
  if isinstance(df, pd.DataFrame):
    c = df[label].value_counts(dropna=False)
    p = df[label].value_counts(dropna=False, normalize=True).mul(100).round(digit).astype(str) + '%'
    print(pd.concat([c,p], axis=1, keys=['counts', '%']))
  elif isinstance(df, pd.Series):
    c = df.value_counts(dropna=False)
    p = df.value_counts(dropna=False, normalize=True).mul(100).round(digit).astype(str) + '%'
    print(pd.concat([c,p], axis=1, keys=['counts', '%']))
  else:
    raise ValueError("check input type!")

