import matplotlib.pyplot as plt
import json
from matplotlib import font_manager
import argparse

# Add argument parser
parser = argparse.ArgumentParser(description="Render LLM benchmark chart")
parser.add_argument(
    "--render-type",
    choices=["full", "without-fps"],
    default="full",
    help="Rendering type: full or without-fps (default: full)",
)
args = parser.parse_args()

# Add custom font
font_path = "../../assets/fonts/sarasa-mono-sc-regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Sarasa Mono SC"

# JSON data - 修复编码问题
with open("benchmark-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract LLM names and scores (including all LLMs)
scores = data  # Use all data entries

if args.render_type == "without-fps":
    # Remove FPS category and adjust Final-Score
    for entry in scores:
        if "Final-Score" in entry and "point_17" in entry:
            entry["Final-Score"] = entry["Final-Score"] - entry["point_17"]

# Sort scores by Final-Score in descending order
scores.sort(key=lambda x: x["Final-Score"], reverse=True)
llm_names = [entry["LLM"] for entry in scores]

# Prepare data for stacked bar chart
categories = [
    "point_1",
    "point_2",
    "point_3",
    "point_4",
    "point_5",
    "point_6",
    "point_7",
    "point_8",
    "point_9",
    "point_10",
    "point_11",
    "point_12",
    "point_13",
    "point_14",
    "point_15",
    "point_16",
    "point_17",
]

# Category display names for the legend
category_display_names = [
    "1 - 使用 canvas 绘制动画",
    "2 - 全屏展示动画",
    "3 - 所有代码放在同一个HTML文件里面",
    "4 - Mandelbrot Set 图形美观度",
    "5 - Mandelbrot Set 的主要图形大小",
    "6 - Mandelbrot Set 的主要图形每渲染一次每帧放大 0.5%",
    "7 - 总计渲染200次",
    "8 - 总计渲染200次后重置并循环",
    "9 - 李白诗书写正确",
    "10 - 李白诗处理",
    "11 - Mandelbrot Set 的 Main cardioid and period bulbs 部分留空",
    "12 - 动画的中心应使始终为 Main cardioid and period bulbs 的交界处",
    "13 - 动画字体大小8px, 字体渲染排列也是8px，无间距 ",
    "14 - 字符从 mandelbrot set的最外围使用最深的颜色，然后依次变浅",
    "15 - 左上角指示器计算和展示正确",
    "16 - 指示器样式",
    "17 - 平均FPS水平",
]

if args.render_type == "without-fps":
    # Remove FPS category
    categories = categories[:-1]  # Remove the last category (FPS)
    category_display_names = category_display_names[:-1]  # Remove the last display name

# 新增颜色配置
colors = [
    "#192f60",
    "#223a70",
    "#2a4073",
    "#274a78",
    "#4a488e",
    "#4d4398",
    "#5654a2",
    "#706caa",
    "#68699b",
    "#867ba9",
    "#8491c3",
    "#bbbcde",
    "#bbc8e6",
    "#ebf6f7",
    "#e8ecef",
    "#eaedf7",
    "#eaf4fc",
]

if args.render_type == "without-fps":
    colors = colors[:-1]  # Remove the last color

category_scores = {
    category: [entry.get(category, 0) for entry in scores] for category in categories
}

# Plotting
fig, ax = plt.subplots(figsize=(20, 6))

# Customize font size and weight for better readability
plt.rcParams["font.size"] = 10
plt.rcParams["font.weight"] = "normal"

# Initialize bottom for stacking
bottom = [0] * len(llm_names)

# Plot each category with specified colors
for i, category in enumerate(categories):
    bars = ax.bar(
        llm_names,
        [entry.get(category, 0) for entry in scores],
        bottom=bottom,
        label=category_display_names[i],
        color=colors[i],
        edgecolor="black",
        linestyle="--",
        linewidth=0.5,
        width=0.8,
    )
    bottom = [
        i + j for i, j in zip(bottom, [entry.get(category, 0) for entry in scores])
    ]

# Add total score labels on top of bars
for i, score in enumerate(bottom):  # 使用 bottom 作为最终高度
    ax.text(i, score, f"{scores[i]['Final-Score']}", ha="center", va="bottom")

# Add labels and title
ax.set_ylabel("Score")

if args.render_type == "without-fps":
    ax.set_title(
        "KCORES LLM Arena - Mandelbrot Set Meet Libai Benchmark (Without FPS)\nby karminski-牙医\nhttps://github.com/KCORES/kcores-llm-arena"
    )
else:
    ax.set_title(
        "KCORES LLM Arena - Mandelbrot Set Meet Libai Benchmark\nby karminski-牙医\nhttps://github.com/KCORES/kcores-llm-arena"
    )

ax.set_ylim(0, 110)
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Show plot
plt.tight_layout()
# Save the plot as PNG file
if args.render_type == "without-fps":
    plt.savefig(
        "llm_benchmark_results_without_fps.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.5,
    )
else:
    plt.savefig(
        "llm_benchmark_results.png", dpi=300, bbox_inches="tight", pad_inches=0.5
    )
plt.show()
