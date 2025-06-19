import streamlit as st
import matplotlib.pyplot as plt
import lightkurve as lk
import numpy as np
import time
import re
from lightkurve import LightCurveCollection

st.set_page_config(page_title="Astro App", layout="wide")
st.header("🔭 Astro App")

col1, col2 = st.columns([1, 5])
col3, col4 = st.columns([1, 5])

@st.cache_data(show_spinner=False)
def get_available_data(tic_id):
    return lk.search_lightcurve(tic_id, author="SPOC")

@st.cache_data(show_spinner=True)
def download_with_retries(search_result, max_attempts=10, wait_seconds=1):
    for attempt in range(1, max_attempts + 1):
        try:
            return search_result.download_all()
        except Exception as e:
            if attempt < max_attempts:
                time.sleep(wait_seconds)
            else:
                raise RuntimeError(f"❌ Download failed after {max_attempts} attempts: {e}") from e

with col1:
    st.subheader("Set TIC ID")
    TIC = st.text_input("TIC ID", "TIC 470710327")

selected_sectors = []

with col2:
    if TIC:
        try:
            available_data_all = get_available_data(TIC)
            if len(available_data_all) > 0:
                df = available_data_all.table.to_pandas()

                df["sector"] = df["mission"].str.extract(r"Sector (\d+)", expand=False).astype("Int64")

                desired_columns = [
                    "target_name", "mission", "author", "year", "s_ra", "s_dec", "t_min",
                    "t_max", "t_exptime", "description", "instrument_name", "sector"
                ]
                filtered_columns = [col for col in desired_columns if col in df.columns]
                filtered_df = df[filtered_columns]

                st.subheader("📋 Available SPOC Light Curve Data")
                st.dataframe(filtered_df)

                sectors = sorted(df["sector"].dropna().unique())
                if sectors:
                    min_sec = min(sectors)
                    max_sec = max(sectors)
                    sector_range = st.slider(
                        "Select Sector Range",
                        min_value=min_sec,
                        max_value=max_sec,
                        value=(min_sec, max_sec),
                        step=1
                    )
                    selected_sectors = list(range(sector_range[0], sector_range[1] + 1))
                else:
                    st.warning("⚠️ No valid sectors found.")
            else:
                st.warning("⚠️ No data found for this TIC.")
        except Exception as e:
            st.error(f"❌ Error fetching all-sector data: {e}")

with col3:
    st.subheader("Selected Sectors")
    if TIC and selected_sectors:
        st.write(selected_sectors)
    elif TIC:
        st.info("Select a valid TIC to load available sectors.")

with col4:
    st.subheader("📈 Light Curve Plot")

    if TIC and selected_sectors:
        try:
            search_result = get_available_data(TIC)
            result_df = search_result.table.to_pandas()
            result_df["sector"] = result_df["mission"].str.extract(r"Sector (\d+)", expand=False).astype("Int64")

            target_df = result_df[result_df["sector"].isin(selected_sectors)]

            filtered_result = lk.SearchResult([
                res for res in search_result
                if any(
                    res.table["mission"] == row["mission"] and res.table["t_min"] == row["t_min"]
                    for _, row in target_df.iterrows()
                )
            ])

            if len(filtered_result) > 0:
                downloaded = download_with_retries(filtered_result)

                if isinstance(downloaded, list):
                    valid_curves = [lc for lc in downloaded if hasattr(lc, "flux")]
                    if not valid_curves:
                        raise ValueError("⚠️ No valid light curves were downloaded.")
                    lightcurve = LightCurveCollection(valid_curves).stitch()
                elif hasattr(downloaded, "stitch"):
                    lightcurve = downloaded.stitch()
                elif hasattr(downloaded, "flux"):
                    lightcurve = downloaded
                else:
                    raise ValueError("⚠️ Unexpected download result type.")

                fig, ax = plt.subplots()
                lightcurve.plot(ax=ax, linewidth=0, marker='.', color='midnightblue', alpha=0.5)
                st.pyplot(fig)
            else:
                st.warning("⚠️ No data found for the selected sector range.")
        except Exception as e:
            st.error(f"❌ {str(e)}")