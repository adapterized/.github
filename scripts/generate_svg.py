import matplotlib.pyplot as plt
import requests


def fetch_arena_models():
    url = "https://api.wulong.dev/arena-ai-leaderboards/v1/leaderboard?name=text"

    try:
        response = requests.get(url).json()
        top_15 = response.get("models", [])[:15]

        models = [
            m["model"][:18] + "..." if len(m["model"]) > 18 else m["model"]
            for m in top_15
        ]
        scores = [m["score"] for m in top_15]

        return models[::-1], scores[::-1]

    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return ["Fallback Model"] * 15, [1000] * 15


def draw_svg(models, scores):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("#0d1117")

    bars = ax.barh(models, scores, color="#7e57c2", height=0.5, alpha=0.85)

    # Clean up the chart
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 10,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            color="#8b949e",
            fontsize=9,
        )

    ax.get_xaxis().set_ticks([])
    ax.tick_params(axis="y", colors="#c9d1d9", length=0, labelsize=10, pad=10)

    plt.savefig("top_models.svg", format="svg", bbox_inches="tight", transparent=True)
    print("Top 15 Open/Closed Source models graphed. Vibes secured.")


if __name__ == "__main__":
    models, scores = fetch_arena_models()
    draw_svg(models, scores)
