"""
This script will validate the excel file uploaded by the user then validate the crucial columns
after that creating the excel output when the user press on download button
"""

#__TODO: import libraries_______________________________________________
import io
from typing import Any, Tuple, Optional

import pandas as pd
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

from src.config import UPLOAD_CONFIG, REQUIRED_COLUMNS

class FileHandler:
    """Handles validation and export of Excel files."""

    #__TODO: Validate the uploaded excel buffer_______________________________________________
    @staticmethod
    def validate_excel_file(
        file: Any, file_label: str
    ) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Args:
            file: Uploaded file.
            file_label: A label for the file (e.g., "old", "new").

        Returns:
            Tuple containing:
              - validity (bool)
              - message (str)
              - DataFrame if valid, else None
        """
        if not file:
            return False, f"No '{file_label}' file uploaded.", None

        try:
            df = (
                pd.read_excel(
                    file,
                    engine="openpyxl",
                    sheet_name=UPLOAD_CONFIG["sheet_name"],
                    skiprows=UPLOAD_CONFIG["skip_rows"],
                )
                .reset_index(drop=True)
            )
        except Exception as e:
            return False, f"Error reading '{file_label}' file: {e}", None

        if df.empty:
            return False, f"'{file_label}' file is empty.", None

        is_valid, msg = FileHandler._validate_columns(df)
        if not is_valid:
            return False, msg, None

        return True, "File uploaded successfully.", df
    
    #__TODO: Validate the crucial columns_______________________________________________
    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Check for required columns

        Args:
            df: DataFrame to validate.

        Returns:
            validity and error message if invalid.
        """
        required_cols = [
            REQUIRED_COLUMNS["mass"],
            REQUIRED_COLUMNS["reference"],
        ]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return False, f"Missing columns: {', '.join(missing)}."
        return True, ""
    
    #__TODO: Create the excel output _______________________________________________
    @staticmethod
    def create_excel_bytes(
        results: pd.DataFrame
    ) -> bytes:
        """
        Generate a styled Excel report as bytes.

        Args:
            results: Analysis results with metadata.

        Returns:
            Byte content of the Excel file.
        """
        if results is None:
            raise ValueError("'results' fataframe is required.")

        export_df = results
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            export_df.to_excel(writer, sheet_name="PTA Analysis", index=False)
            wb = writer.book
            ws = writer.sheets["PTA Analysis"]

            # Header styling
            header_fill = PatternFill("solid", fgColor="4F81BD")
            header_font = Font(bold=True, color="FFFFFF", size=12)
            header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
            header_border = Border(*(Side("thin"),) * 4)

            for idx in range(1, len(export_df.columns) + 1):
                cell = ws.cell(row=1, column=idx)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_align
                cell.border = header_border

        return output.getvalue()