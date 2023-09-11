import streamlit as st
import pandas as pd
from xbbg import blp
# Set the display option to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def convert(filename):
    df = pd.read_excel(filename)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
    chs = df.iloc[:, 0].tolist()
    chs = [item for item in chs if ' CH ' in item]
    chs = list(set(chs))
    c2s = [item.replace(' CH ', ' C2 ') for item in chs]
    c1s = [item.replace(' CH ', ' C1 ') for item in chs]
    c1_df = blp.bdp(c1s, 'ID_BB_GLOBAL')
    c1_df = c1_df.reset_index()
    c2_df = blp.bdp(c2s, 'ID_BB_GLOBAL')
    c2_df = c2_df.reset_index()

    results = []

    # Check 'c1_df' dataframe
    for item in chs:
        for index_value in c1_df['index'].values:
            if item.split()[0] == index_value.split()[0]:
                results.append(index_value)
                break  # Move to the next item in 'chs' without executing the subsequent 'for' loop

        else:  # Executed when the 'for' loop completes without encountering a 'break'
            for index_value in c2_df['index'].values:
                if item.split()[0] == index_value.split()[0]:
                    results.append(index_value)
                    break  # Move to the next item in 'chs' without executing the subsequent 'for' loop
            else:  # Executed when the 'for' loop completes without encountering a 'break'
                results.append(item)
    df['converted'] = pd.Series(results)
    df['previous'] = pd.Series(chs)
    df = df[['previous', 'converted']]
    df.to_excel(filename, header=True, index=False)

    st.dataframe(df)

    #st.write("DataFrame saved to", filename)


def browse_file():
    filename = st.file_uploader("Upload xlsx file of input CH tickers", type="xlsx")
    if filename:
        convert(filename)
        #st.write("DataFrame saved to", filename.name)
    #else:
        #st.write("File could not be opened, check if it is in xlsx format")


def main():
    st.title("CH Tickers Conversion")
    browse_file()


if __name__ == "__main__":
    main()