"""Dashboard Shiny for Python: Old Faithful Geyser.

Jalankan dengan:
    shiny run --reload app.py
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from shiny import App, reactive, render, req, ui

from data_loader import load_faithful

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df = load_faithful()

W_MIN, W_MAX = float(df["waiting"].min()), float(df["waiting"].max())
E_MIN, E_MAX = float(df["eruptions"].min()), float(df["eruptions"].max())

LABEL = {
    "eruptions": "Durasi semburan (menit)",
    "waiting": "Waktu tunggu (menit)",
}

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Filter data"),
        ui.input_slider(
            "rentang_tunggu",
            "Rentang waktu tunggu (menit):",
            min=W_MIN,
            max=W_MAX,
            value=(W_MIN, W_MAX),
        ),
        ui.input_slider(
            "rentang_durasi",
            "Rentang durasi semburan (menit):",
            min=E_MIN,
            max=E_MAX,
            value=(E_MIN, E_MAX),
            step=0.1,
        ),
        ui.output_text("jumlah_data"),
        ui.hr(),
        ui.h4("Opsi histogram"),
        ui.input_select(
            "var",
            "Variabel:",
            {"eruptions": "Durasi semburan", "waiting": "Waktu tunggu"},
        ),
        ui.input_slider("bins", "Jumlah bin:", min=5, max=50, value=20),
        ui.input_radio_buttons(
            "warna",
            "Warna:",
            {"steelblue": "Biru", "seagreen": "Hijau", "darkorange": "Oranye"},
            inline=True,
        ),
        ui.input_checkbox("density", "Tampilkan kurva density", True),
        ui.input_checkbox("mean", "Tampilkan garis rata-rata", False),
        ui.hr(),
        ui.h4("Opsi scatter plot"),
        ui.input_checkbox("regresi", "Tampilkan garis regresi", True),
        width=330,
    ),
    ui.navset_tab(
        ui.nav_panel(
            "Histogram",
            ui.output_plot("hist_plot"),
            ui.h5("Ringkasan statistik"),
            ui.output_text_verbatim("ringkasan"),
        ),
        ui.nav_panel(
            "Scatter Plot",
            ui.output_plot("scatter_plot"),
            ui.h5("Korelasi dan regresi linear"),
            ui.output_text_verbatim("regresi_info"),
        ),
        ui.nav_panel(
            "Data",
            ui.output_data_frame("tabel"),
        ),
        ui.nav_panel(
            "Prediksi",
            ui.input_numeric(
                "waktu_baru", "Waktu tunggu (menit):", value=70, min=30, max=120
            ),
            ui.h5("Prediksi durasi semburan"),
            ui.output_text("hasil_prediksi"),
        ),
    ),
    title="Dashboard Old Faithful Geyser",
)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
def server(input, output, session):
    @reactive.calc
    def data_filter():
        w_lo, w_hi = input.rentang_tunggu()
        e_lo, e_hi = input.rentang_durasi()
        return df[
            df["waiting"].between(w_lo, w_hi) & df["eruptions"].between(e_lo, e_hi)
        ]

    @reactive.calc
    def model():
        d = data_filter()
        req(len(d) > 2, d["waiting"].nunique() > 1)
        return stats.linregress(d["waiting"], d["eruptions"])

    # ---- Sidebar ----------------------------------------------------------
    @render.text
    def jumlah_data():
        return f"Observasi terpilih: {len(data_filter())} dari {len(df)}"

    # ---- Tab Histogram ----------------------------------------------------
    @render.plot
    def hist_plot():
        x = data_filter()[input.var()]
        req(len(x) > 2)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(
            x,
            bins=input.bins(),
            density=True,
            color=input.warna(),
            edgecolor="white",
            alpha=0.85,
        )

        if input.density() and x.nunique() > 1:
            grid = np.linspace(x.min(), x.max(), 300)
            ax.plot(grid, stats.gaussian_kde(x)(grid), color="black", linewidth=2)

        if input.mean():
            ax.axvline(x.mean(), color="red", linestyle="--", linewidth=2)

        ax.set_xlabel(LABEL[input.var()])
        ax.set_ylabel("Density")
        ax.set_title(f"Distribusi {LABEL[input.var()]}")
        ax.spines[["top", "right"]].set_visible(False)
        return fig

    @render.text
    def ringkasan():
        x = data_filter()[input.var()]
        req(len(x) > 0)
        return x.describe().round(3).to_string()

    # ---- Tab Scatter ------------------------------------------------------
    @render.plot
    def scatter_plot():
        d = data_filter()
        req(len(d) > 0)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.scatter(d["waiting"], d["eruptions"], color="steelblue", alpha=0.7, s=25)

        if input.regresi() and len(d) > 2 and d["waiting"].nunique() > 1:
            m = model()
            xs = np.linspace(d["waiting"].min(), d["waiting"].max(), 100)
            ax.plot(xs, m.intercept + m.slope * xs, color="firebrick", linewidth=2)

        ax.set_xlabel(LABEL["waiting"])
        ax.set_ylabel(LABEL["eruptions"])
        ax.set_title("Hubungan Waktu Tunggu dan Durasi Semburan")
        ax.spines[["top", "right"]].set_visible(False)
        return fig

    @render.text
    def regresi_info():
        m = model()
        return (
            f"Korelasi Pearson (r) : {m.rvalue:.4f}\n"
            f"R-squared            : {m.rvalue ** 2:.4f}\n"
            f"p-value              : {m.pvalue:.3e}\n"
            f"Persamaan            : durasi = {m.intercept:.4f} + {m.slope:.4f} x waktu_tunggu"
        )

    # ---- Tab Data ---------------------------------------------------------
    @render.data_frame
    def tabel():
        d = data_filter().rename(
            columns={"eruptions": "Durasi semburan", "waiting": "Waktu tunggu"}
        )
        return render.DataGrid(d, filters=False)

    # ---- Tab Prediksi -----------------------------------------------------
    @render.text
    def hasil_prediksi():
        req(input.waktu_baru() is not None)
        m = model()
        pred = m.intercept + m.slope * input.waktu_baru()
        return (
            f"Untuk waktu tunggu {input.waktu_baru():.0f} menit, "
            f"durasi semburan diperkirakan {pred:.2f} menit."
        )


app = App(app_ui, server)
