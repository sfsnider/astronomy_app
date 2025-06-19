import streamlit as st
import matplotlib.pyplot as plt
import lightkurve as lk

st.set_page_config(page_title="Astro App", layout="wide")
st.header("🔭 Astro App")

col1, col2 = st.columns([1, 4])
col3, col4 = st.columns([1, 4])


with col1:
    st.subheader("Set TIC ID")
    TIC = st.text_input("TIC ID", "TIC 470710327")
    

with col2:
    # 🔎 Show all-sector metadata
    if TIC:
        try:
            available_data_all = lk.search_lightcurve(TIC, author='SPOC')
            if len(available_data_all) > 0:
                df = available_data_all.table.to_pandas()

                # ✅ Keep only the existing desired columns
                desired_columns = [
                    "target_name", "mission", "author", "year", "s_ra", "s_dec", "t_min",
                    "t_max", "t_exptime", "description", "instrument_name"
                ]
                filtered_columns = [col for col in desired_columns if col in df.columns]
                filtered_df = df[filtered_columns]

                st.subheader("📋 Available SPOC Light Curve Data")
                st.dataframe(filtered_df)
            else:
                st.warning("⚠️ No data found for this TIC.")
        except Exception as e:
            st.error(f"❌ Error fetching all-sector data: {e}")


with col3:
    secNum = st.number_input("Sector Number", min_value=1, max_value=99, step=1)

with col4:
    # 📈 Sector-specific plot
    with st.container():
        st.subheader("📈 Light Curve Plot")

        if TIC and secNum:
            try:
                sector_data = lk.search_lightcurve(TIC, author='SPOC', sector=secNum)
                if len(sector_data) > 0:
                    lightcurve = sector_data.download()

                    fig, ax = plt.subplots()
                    lightcurve.plot(ax=ax, linewidth=0, marker='.', color='midnightblue', alpha=0.5)
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ No data found for that TIC/sector.")
            except Exception as e:
                st.error(f"❌ Error loading light curve: {e}")