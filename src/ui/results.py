import streamlit as st
import pandas as pd
from file_handler import FileHandler

class Result:
    def __init__(self):
        self.new_df = st.session_state.get('input_excel_new', pd.DataFrame())
        self.res_df = st.session_state.get('results', pd.DataFrame())

    @staticmethod
    def _highlight_row(row):
        if row['Change Type'] == 'New':
            return ['background-color: #FF5733'] * len(row)
        if row['Change Type'] == 'Spring Changed':
            return ['background-color: #B4C6E7'] * len(row)
        return [''] * len(row)


    def display_results(self):
        if self.new_df.empty or self.res_df.empty:
            st.warning('No data to display.')
            return
        st.dataframe(self.new_df)
        st.dataframe(self.res_df)
        # merge new input with metadata and sort
        display_df = self.new_df.copy()
        
        metadata_cols = [
            'Old Reference', 'New Reference',
            'Mass Status', 'Change Type',
            'Cell ID New', 'Cell ID Old'
        ]
        
        for col in metadata_cols:
            display_df[col] = self.res_df[col]
            
        display_df = display_df.sort_values('Cell ID New', ascending=True).reset_index(drop=True)

        # apply styling
        styled = display_df.style.apply(self._highlight_row, axis=1)
        st.dataframe(styled)

        # download section with color legend
        st.subheader('📥 Download Results')
        try:
            data = FileHandler.create_excel_bytes(display_df)
            st.download_button(
                '📄 Download Excel Report',
                data=data,
                file_name='spring_change_analysis.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            st.error(f'Error creating Excel file: {e}')

        # legend explaining colors
        st.markdown('''
        **Color Legend:**
        - 🟥 **New rows**: Cars added in new PTA file
        - 🟦 **Spring Changed**: Reference (spring) changed
        ''')
