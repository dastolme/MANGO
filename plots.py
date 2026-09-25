import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rc

plt.rcParams['axes.grid'] = True
plt.rcParams['savefig.transparent'] = True

# HFO_0_dict = {
#   "VGEM": [370, 380, 390, 400, 410, 420, 430, 440],
#   "Charge_keV": [8.08523166e-13, 1.46132443e-12, 2.49760157e-12, 3.82302562e-12,
#                  5.91143483e-12, 9.34253199e-12, 1.42059941e-11, 1.76780901e-11],
#    "EX": [1, 1, 1, 1, 1, 1, 1, 1],
#    "EY": [1.69009610e-14, 3.00718705e-14, 5.04190541e-14, 7.69504929e-14,
#   1.18603424e-13, 1.87397923e-13, 4.33988951e-13, 3.54121358e-13]
# }
# HFO_0 = pd.DataFrame(HFO_0_dict)

# HFO_1_dict = {
#   "VGEM": [370, 380, 390, 400, 410, 420, 430, 440, 450],
#   "Charge_keV": [4.86489623e-13, 8.95202444e-13, 1.43061962e-12, 2.55827051e-12,
#   4.42926669e-12, 6.56723522e-12, 9.63379394e-12, 1.29554316e-11,
#   1.72063797e-11],
#    "EX": [1, 1, 1, 1, 1, 1, 1, 1, 1],
#    "EY": [1.73297321e-14, 2.89312225e-14, 5.28536317e-14, 8.03618915e-14,
#   1.38917638e-13, 2.05515941e-13, 3.01422007e-13, 4.05512577e-13,
#   6.00948613e-13]
# }
# HFO_1 = pd.DataFrame(HFO_1_dict)

# HFO_2_5_dict = {
#   "VGEM": [380, 390, 400, 410, 420, 430, 440, 450, 460, 470],
#   "Charge_keV": [4.85835769e-13, 8.74625088e-13, 1.47491811e-12, 2.54186123e-12,
#   3.98906208e-12, 6.19917188e-12, 8.79881952e-12, 1.20036689e-11,
#   1.52996546e-11, 1.95298450e-11],
#    "EX": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#    "EY": [2.69043545e-14, 4.67862818e-14, 7.79949905e-14, 1.34093736e-13,
#   2.10174635e-13, 3.26487394e-13, 4.63323316e-13, 6.32607594e-13,
#   8.05508558e-13, 1.02837465e-12]
# }
# HFO_2_5 = pd.DataFrame(HFO_2_5_dict)

# HFO_5_dict = {
#   "VGEM": [430, 440, 450, 460, 470, 480, 490],
#   "Charge_keV": [2.24121550e-12, 3.52928205e-12, 5.55123487e-12, 7.75843073e-12,
#   1.05074204e-11, 1.34153318e-11, 1.72125004e-11],
#    "EX": [1, 1, 1, 1, 1, 1, 1],
#    "EY": [1.18772936e-13, 1.86005619e-13, 2.92370564e-13, 4.08554934e-13,
#   5.54730820e-13, 7.06646818e-13, 9.08519588e-13]
# }
# HFO_5 = pd.DataFrame(HFO_5_dict)

# HFO = pd.concat(
#     [HFO_0, HFO_1, HFO_2_5, HFO_5],
#     keys=["0", "1", "2.5", "5"],
#     names=["Dataset", None]
# ).reset_index(level=0).reset_index(drop=True)
# print(HFO)

# sns.set_theme(style="ticks", context="paper")
# sns.color_palette(palette='gist_rainbow')

# g = sns.relplot(
#     data=HFO,
#     x="VGEM",
#     y="Charge_keV",
#     hue="Dataset",
#     s=300,
#     marker=".",
#     palette=["#F7D002", "#454E9E", "#54C6EB", "#16DB93"],
#     edgecolor="None"
# )

# g.set(yscale="log")
# g.ax.yaxis.grid(True, "minor", linewidth=.25)

# g.map(plt.errorbar, "VGEM", "Charge_keV", "EY","EX", marker="none", color='r', ls='none', elinewidth=1)

# for ax in g.axes.flat:
#     ax.grid(True, axis='both')

#     ax.tick_params(axis='both', which='both', colors='white', labelsize=12)

# for spine in ['top', 'right', 'bottom', 'left']:
#     ax.spines[spine].set_visible(True)
#     ax.spines[spine].set_color('black')
#     ax.spines[spine].set_linewidth(0.7)

# sns.move_legend(
#     g,
#     "upper left",
#     bbox_to_anchor=(0.7, 0.45),
#     title="HFO(%)",
#     frameon=True
# )

# if g._legend:
#     leg = g._legend
#     leg.get_frame().set_facecolor("white")
#     leg.get_frame().set_alpha(0.85)

#     for text in leg.get_texts():
#         text.set_fontsize(12)

# plt.ylabel("Charge/keV [C/keV]", fontsize = 20, color='white')
# plt.xlabel("VGEM [V]", fontsize = 20, color='white')
# plt.tight_layout(rect=[0, 0, 0.9, 1])
# plt.savefig("electron_gain.png", dpi=500, transparent=True)

# #################################
HFO_0_dict = {
    "VGEM": [350, 360, 370, 380, 390, 400, 410, 420, 430],
    "EX": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Peak": [1963.73190641,   4725.78926604,  11514.76699033,  23857.60246052,
        41531.15377315,  64943.40495567,  95116.89885729, 134394.32155147,
       185676.17599549],
    "EY": [7.45963764,  12.60919598,  21.99637395,  31.29725521,
        48.93478198,  80.98394362, 127.66029395, 184.98732682,
       248.24535563]
}

HFO_0 = pd.DataFrame(HFO_0_dict)

HFO_1_dict = {
    "VGEM": [390, 400, 410, 420, 430, 440],
    "EX": [1, 1, 1, 1, 1, 1],
    "Peak": [3130.40735378, 6880.34593405, 12257.45196222, 19433.27043398, 28774.39290661, 40702.76718417],
    "EY": [84.59753889, 62.06156803, 45.13368276, 30.45546012, 21.32610724,
       19.97514249]
}

HFO_1 = pd.DataFrame(HFO_1_dict)

HFO_2_5_dict = {
    "VGEM": [440, 450, 460, 470],
    "EX": [1, 1, 1, 1],
    "Peak": [7750, 13640, 18800, 24400],
    "EY": [20, 30, 50, 70]
}

HFO_2_5 = pd.DataFrame(HFO_2_5_dict)

HFO_5_dict = {
    "VGEM": [450, 460, 480, 490],
    "EX": [1, 1, 1, 1],
    "Peak": [3540, 3620, 5900, 8370],
    "EY": [20, 30, 50, 90]
}

HFO_5 = pd.DataFrame(HFO_5_dict)

HFO_7_5_dict = {
    "VGEM": [460, 470, 480],
    "EX": [1, 1, 1],
    "Peak": [880, 1330, 1910],
    "EY": [10, 10, 10]
}

HFO_7_5 = pd.DataFrame(HFO_7_5_dict)

HFO_10_dict = {
    "VGEM": [470, 480, 490],
    "EX": [1, 1, 1],
    "Peak": [400, 530, 770],
    "EY": [50, 30, 30]
}

HFO_10 = pd.DataFrame(HFO_10_dict)

HFO = pd.concat(
    [HFO_0, HFO_1, HFO_2_5, HFO_5, HFO_7_5, HFO_10],
    keys=["0", "1", "2.5", "5", "7.5", "10"],
    names=["Dataset", None]
).reset_index(level=0).reset_index(drop=True)

sns.set_theme(style="ticks", context="paper")
sns.color_palette(palette='gist_rainbow')

g = sns.relplot(
    data=HFO,
    x="VGEM",
    y="Peak",
    hue="Dataset",
    s=300,
    marker=".",
    palette=["#F7D002", "#454E9E", "#54C6EB", "#16DB93", "#f6b8b8", "#B0A7A7"],
    edgecolor="None"
)

g.set(yscale="log")
g.ax.yaxis.grid(True, "minor", linewidth=.25)

g.map(plt.errorbar, "VGEM", "Peak", "EY", "EX", marker="none", color='r', ls='none', elinewidth=1)

for ax in g.axes.flat:
    ax.grid(True, axis='both')

    ax.tick_params(axis='both', which='both', colors='white', labelsize=12)

for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(0.7)

sns.move_legend(
    g,
    "upper left",
    bbox_to_anchor=(0.7, 0.47),
    title="HFO(%)",
    frameon=True
)

if g._legend:
    leg = g._legend
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_alpha(0.85)

    for text in leg.get_texts():
        text.set_fontsize(12)
    

plt.ylabel("LY [ADC]", fontsize = 20, color='white')
plt.xlabel("VGEM [V]", fontsize = 20, color='white')
plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.savefig("LY.png", dpi=500, transparent=True)

# ####################
# He_CF4_spectrum = pd.read_csv(
#     "/Users/melbadastolfo/Desktop/CYGNO/Analysis/MANGO/Florian/He_CF4/Orig_He_CF4_1000.txt",
#     delim_whitespace=True,
#     header=None,
#     names=["V1", "V2"]
# )

# HFO1_spectrum = pd.read_csv(
#     "/Users/melbadastolfo/Desktop/CYGNO/Analysis/MANGO/Florian/He_CF4_HFO1/Orig_He_CF4_HFO1_1000.txt",
#     delim_whitespace=True,
#     header=None,
#     names=["V1", "V2"]
# )

# # HFO2_5_spectrum = pd.read_csv(
# #     "/Users/melbadastolfo/Desktop/CYGNO/Analysis/MANGO/Florian/He_CF4_HFO2.5/He_CF4_HFO2.5_1000.txt",
# #     delim_whitespace=True,
# #     header=None,
# #     names=["V1", "V2"]
# # )

# # -------------------------------
# # Define wavelength ranges (MUST BE ADDED)
# # -------------------------------
# UV = (200, 400)      # example — change to your real UV range
# VIS = (400, 750)     # example — change to your real VIS range

# # -------------------------------
# # Define integral functions
# # -------------------------------
# def calc_VIS_integral(spectrum, VIS):
#     mask = (
#         (spectrum["V1"] >= VIS[0]) &
#         (spectrum["V1"] <= VIS[1]) &
#         (spectrum["V2"] >= 0)
#     )
#     return spectrum.loc[mask, "V2"].sum()

# def calc_UV_integral(spectrum, UV):
#     mask = (
#         (spectrum["V1"] >= UV[0]) &
#         (spectrum["V1"] < UV[1]) &
#         (spectrum["V2"] >= 0)
#     )
#     return spectrum.loc[mask, "V2"].sum()

# # -------------------------------
# # Build dataframe
# # -------------------------------
# gas_mixture = (
#     ["He:CF4(60:40)"] * 2 +
#     ["He:CF4:HFO(1%)"] * 2 
#     # ["He:CF4:HFO(2.5%)"] * 2
# )

# emission_band = ["UV", "VIS"] * 2

# value = [
#     calc_UV_integral(He_CF4_spectrum, UV),
#     calc_VIS_integral(He_CF4_spectrum, VIS),

#     calc_UV_integral(HFO1_spectrum, UV),
#     calc_VIS_integral(HFO1_spectrum, VIS)

#     # calc_UV_integral(HFO2_5_spectrum, UV),
#     # calc_VIS_integral(HFO2_5_spectrum, VIS)
# ]

# data = pd.DataFrame({
#     "gas_mixture": gas_mixture,
#     "emission_band": emission_band,
#     "value": value
# })

# # -------------------------------
# # Compute percentages
# # -------------------------------
# data_percent = (
#     data
#     .groupby("gas_mixture")
#     .apply(lambda df: df.assign(percentage=df["value"] / df["value"].sum()))
#     .reset_index(drop=True)
# )

# # -------------------------------
# # Plot
# # -------------------------------
# plt.figure(figsize=(6, 6))

# ax = sns.barplot(
#     data=data_percent,
#     x="gas_mixture",
#     y="value",
#     hue="emission_band",
#     dodge=True
# )

# ax.yaxis.grid(True, linestyle='-', alpha=0.7)
# ax.set_axisbelow(True)

# # Add percentage labels
# x_order = data_percent["gas_mixture"].unique()
# hue_order = data_percent["emission_band"].unique()
# n_hues = len(hue_order)
# bar_width = 0.8 / n_hues

# for i, x_val in enumerate(x_order):
#     for j, hue_val in enumerate(hue_order):
#         # Select the correct row
#         row = data_percent[
#             (data_percent["gas_mixture"] == x_val) &
#             (data_percent["emission_band"] == hue_val)
#         ]
#         if not row.empty:
#             y = row["value"].values[0]
#             perc = row["percentage"].values[0] * 100

#             xpos = i - 0.4 + bar_width/2 + j*bar_width

#             # Annotate directly above the bar
#             ax.text(
#                 xpos,  # x-position: adjust dodge width if needed
#                 y + y*0.002,       # small offset above the bar
#                 f"{perc:.1f}%",
#                 ha="center",
#                 va="bottom",
#                 fontsize=12
#             )

# # Labels, legend, theme
# ax.set_xlabel("Gas Mixture", fontsize=14)
# ax.set_ylabel("Intensity (a.u.)", fontsize=14)

# leg = ax.legend(title="Emission band", loc="upper right", bbox_to_anchor=(0.95, 0.85))
# plt.setp(leg.get_title(), fontsize=14)
# plt.setp(leg.get_texts(), fontsize=12)

# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)

# plt.tight_layout()
# plt.savefig("UV_VIS.png", dpi=500)


# # ###################
# HFO_0_dict = {
#     "VGEM": [370, 380, 390, 400, 410, 420, 430],
#     "Gain": [8.08523166e-13, 1.46132443e-12, 2.49760157e-12, 3.82302562e-12,
#              5.91143483e-12, 9.34253199e-12, 1.42059941e-11],
#     "EX": [1.69009610e-14, 3.00718705e-14, 5.04190541e-14, 7.69504929e-14,
#         1.18603424e-13, 1.87397923e-13, 4.33988951e-13],
#     "Peak": [11514.76699033, 23857.60246052, 41531.15377315, 64943.40495567,
#              95116.89885729, 134394.32155147, 185676.17599549],
#     "EY": [21.99637395,  31.29725521,
#             48.93478198,  80.98394362, 127.66029395, 184.98732682,
#             248.24535563],
#     "Dataset": ["0%"]*7
# }

# HFO_1_dict = {
#     "VGEM": [390, 400, 410, 420, 430, 440],
#     "Gain": [1.43061962e-12, 2.55827051e-12, 4.42926669e-12, 6.56723522e-12,
#              9.63379394e-12, 1.29554316e-11],
#     "EX": [5.28536317e-14, 8.03618915e-14,
#         1.38917638e-13, 2.05515941e-13, 3.01422007e-13, 4.05512577e-13],
#     "Peak": [3130.40735378, 6880.34593405, 12257.45196222, 19433.27043398,
#              28774.39290661, 40702.76718417],
#     "EY": [84.59753889, 62.06156803, 45.13368276, 30.45546012, 21.32610724,
#         19.97514249],
#     "Dataset": ["1%"]*6
# }

# HFO_2_5_dict = {
#     "VGEM": [440, 450, 460, 470],
#     "Gain": [8.79881952e-12, 1.20036689e-11, 1.52996546e-11, 1.95298450e-11],
#     "EX": [4.63323316e-13, 6.32607594e-13,
#         8.05508558e-13, 1.02837465e-12],
#     "Peak": [7750, 13640, 18800, 24400],
#     "EY": [20, 30, 50, 70],
#     "Dataset": ["2.5%"]*4
# }

# HFO_5_dict = {
#     "VGEM": [450, 460, 480, 490],
#     "Gain": [5.55123487e-12, 7.75843073e-12, 1.34153318e-11, 1.72125004e-11],
#     "EX": [2.92370564e-13, 4.08554934e-13,
#      7.06646818e-13, 9.08519588e-13],
#     "Peak": [3540, 3620, 5900, 8370],
#     "EY": [20, 30, 50, 90],
#     "Dataset": ["5%"]*4
# }

# # Combine all datasets into one DataFrame
# HFO = pd.concat([
#     pd.DataFrame(HFO_0_dict),
#     pd.DataFrame(HFO_1_dict),
#     pd.DataFrame(HFO_2_5_dict),
#     pd.DataFrame(HFO_5_dict)
# ], ignore_index=True)

# # ---------------------------
# # Set Seaborn theme
# # ---------------------------
# sns.set_theme(style="ticks", context="paper")
# palette = ["#F7D002", "#454E9E", "#54C6EB", "#16DB93"]

# # ---------------------------
# # Create scatter plot with error bars
# # ---------------------------
# g = sns.relplot(
#     data=HFO,
#     x="Gain",
#     y="Peak",
#     hue="Dataset",
#     s=100,
#     marker="o",
#     palette=palette,
#     edgecolor="none"
# )

# # Set y-axis to log scale
# g.set(yscale="log")
# g.ax.yaxis.grid(True, "minor", linewidth=0.25)


# # Add error bars
# for ds in HFO['Dataset'].unique():
#     subset = HFO[HFO['Dataset'] == ds]
#     g.ax.errorbar(subset['Gain'], subset['Peak'], yerr=subset['EY'], xerr=subset['EX'],
#                   fmt='none', color='r', elinewidth=1, capsize=1)

# # Customize axes and spines
# for ax in g.axes.flat:
#     ax.grid(True, axis='both')
#     ax.tick_params(axis='both', which='both', colors='black', labelsize=12)
#     for spine in ['top', 'right', 'bottom', 'left']:
#         ax.spines[spine].set_visible(True)
#         ax.spines[spine].set_color('black')
#         ax.spines[spine].set_linewidth(0.7)

# # Move and customize legend
# sns.move_legend(
#     g,
#     "upper left",
#     bbox_to_anchor=(0.7, 0.4),
#     title="HFO(%)",
#     frameon=True
# )

# if g._legend:
#     leg = g._legend
#     leg.get_frame().set_facecolor("white")
#     leg.get_frame().set_alpha(0.85)
#     for text in leg.get_texts():
#         text.set_fontsize(12)

# # Labels and layout
# plt.ylim(1e3,4e5)
# plt.xlabel(r"Y$_Q$ [C/keV]", fontsize=16)
# plt.ylabel("LY [ADC]", fontsize=16)
# plt.tight_layout(rect=[0, 0, 0.9, 1])
# plt.savefig("peak_vs_gain.png", dpi=500)