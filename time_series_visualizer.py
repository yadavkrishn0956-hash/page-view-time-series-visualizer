import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load and clean data (GLOBAL, used by all functions)
df = pd.read_csv("fcc-forum-pageviews.csv")

# Step 1: set date as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Step 2: clean data (remove top & bottom 2.5%)
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)

df_copy = df[(df['value'] > lower) & (df['value'] < upper)]


# ---------------- LINE PLOT ----------------
def draw_line_plot():
    df_line = df_copy.copy(deep=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df_line.index, df_line['value'])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.savefig("line_plot.png")
    plt.show()


# ---------------- BAR PLOT ----------------
def draw_bar_plot():
    df_copy2 = df_copy.copy(deep=True)

    # Extract year and month
    df_copy2['year'] = df_copy2.index.year
    df_copy2['month'] = df_copy2.index.month

    # Group and average
    bar_df = df_copy2.groupby(['year', 'month'])['value'].mean().unstack()

    # Rename month numbers to names
    bar_df.columns = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    plt.figure(figsize=(10, 6))
    bar_df.plot(kind="bar")
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    plt.savefig("bar_plot.png")
    plt.show()


# ---------------- BOX PLOT ----------------
def draw_box_plot():
    df_copy3 = df_copy.copy(deep=True)
    df_copy3.reset_index(inplace=True)

    df_copy3['year'] = df_copy3['date'].dt.year
    df_copy3['month'] = df_copy3['date'].dt.strftime('%b')

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Year-wise box plot
    sns.boxplot(
        x='year',
        y='value',
        data=df_copy3,
        ax=axes[0]
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        x='month',
        y='value',
        data=df_copy3,
        order=month_order,
        ax=axes[1]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
