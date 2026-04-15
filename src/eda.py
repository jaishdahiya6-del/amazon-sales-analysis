# =============================================================
# FILE: src/eda.py
# PURPOSE: Exploratory Data Analysis with 10+ Business Charts
# DATASET: Amazon Sales (100K+ rows)
# =============================================================

# ---- IMPORTS ----
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')  # Suppress minor warnings

# ---- STYLING ----
# Set a clean, professional look for all charts
# This affects EVERY chart we draw below
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Amazon brand colors — makes charts look professional
AMAZON_ORANGE = '#FF9900'
AMAZON_DARK   = '#232F3E'
AMAZON_BLUE   = '#146EB4'
PALETTE = [AMAZON_ORANGE, AMAZON_BLUE, AMAZON_DARK,
           '#28A745', '#DC3545', '#6F42C1', '#FFC107']

# =============================================================
# SECTION 0: LOAD CLEANED DATA
# =============================================================

def load_cleaned_data():
    """Load the cleaned CSV we created in data_cleaning.py"""

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "processed", "amazon_sales_cleaned.csv")

    df = pd.read_csv(file_path, encoding='latin1')
    print(f"✅ Cleaned data loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"📋 Columns available: {list(df.columns)}\n")
    return df


# =============================================================
# HELPER: SAVE CHART
# =============================================================

def save_chart(filename):
    """
    Save every chart to the visualizations/ folder automatically.
    Why? So we can use them in README, presentations, and portfolio.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, "visualizations", filename)
    plt.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"   💾 Saved → visualizations/{filename}")


# =============================================================
# CHART 1: Sales by Category — Bar Chart
# BUSINESS QUESTION: Which product categories drive the most orders?
# =============================================================

def chart_1_sales_by_category(df):
    print("\n📊 Chart 1: Sales by Category")

    # Find the correct category column name
    # (our cleaner lowercased all column names)
    cat_col = [c for c in df.columns if 'category' in c.lower()]
    if not cat_col:
        print("   ⚠️  No category column found — skipping")
        return
    cat_col = cat_col[0]

    # Count orders per category and sort descending
    cat_counts = (df[cat_col]
                  .value_counts()
                  .reset_index()
                  .rename(columns={'index': cat_col,
                                   'count': 'order_count',
                                   cat_col: 'order_count'})
                  )
    # Handle both old and new pandas naming
    cat_counts.columns = ['category', 'order_count']
    cat_counts = cat_counts.sort_values('order_count', ascending=False)

    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.bar(cat_counts['category'],
                  cat_counts['order_count'],
                  color=AMAZON_ORANGE,
                  edgecolor='white',
                  linewidth=0.8)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.,
                height + 50,
                f'{int(height):,}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold', color=AMAZON_DARK)

    ax.set_title('📦 Orders by Product Category',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Product Category', fontsize=12)
    ax.set_ylabel('Number of Orders', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f'{int(x):,}'))
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    save_chart("01_sales_by_category.png")
    plt.show()

    # ---- BUSINESS INSIGHT ----
    top_cat = cat_counts.iloc[0]['category']
    top_pct = (cat_counts.iloc[0]['order_count'] /
               cat_counts['order_count'].sum() * 100)
    print(f"\n   🔍 INSIGHT: '{top_cat}' is the top category "
          f"with {top_pct:.1f}% of all orders.")
    print(f"   💼 ACTION: Amazon should prioritize inventory "
          f"& ads for '{top_cat}'.")


# =============================================================
# CHART 2: Order Size Distribution — Bar Chart
# BUSINESS QUESTION: What sizes do customers order the most?
# =============================================================

def chart_2_size_distribution(df):
    print("\n📊 Chart 2: Size Distribution")

    size_col = [c for c in df.columns if 'size' in c.lower()]
    if not size_col:
        print("   ⚠️  No size column found — skipping")
        return
    size_col = size_col[0]

    size_counts = df[size_col].value_counts().reset_index()
    size_counts.columns = ['size', 'count']
    size_counts = size_counts.sort_values('count', ascending=False).head(15)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- Left: Bar Chart ---
    colors = [AMAZON_ORANGE if i == 0 else AMAZON_BLUE
              for i in range(len(size_counts))]
    bars = ax1.bar(size_counts['size'], size_counts['count'],
                   color=colors, edgecolor='white')

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.,
                 h + 30, f'{int(h):,}',
                 ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax1.set_title('👕 Orders by Size', fontsize=14,
                  fontweight='bold', color=AMAZON_DARK)
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Number of Orders')
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # --- Right: Pie Chart ---
    top5 = size_counts.head(5)
    ax2.pie(top5['count'],
            labels=top5['size'],
            autopct='%1.1f%%',
            colors=PALETTE[:5],
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax2.set_title('👕 Top 5 Sizes (Share)', fontsize=14,
                  fontweight='bold', color=AMAZON_DARK)

    plt.suptitle('Size-wise Order Analysis', fontsize=16,
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    save_chart("02_size_distribution.png")
    plt.show()

    top_size = size_counts.iloc[0]['size']
    top_pct  = size_counts.iloc[0]['count'] / size_counts['count'].sum() * 100
    print(f"\n   🔍 INSIGHT: Size '{top_size}' is the most ordered "
          f"({top_pct:.1f}% of orders).")
    print(f"   💼 ACTION: Ensure '{top_size}' stock never runs out "
          f"— it is your highest demand size.")


# =============================================================
# CHART 3: Courier Status Breakdown — Donut + Bar
# BUSINESS QUESTION: What % of orders are delivered vs cancelled?
# =============================================================

def chart_3_courier_status(df):
    print("\n📊 Chart 3: Courier / Delivery Status")

    courier_col = [c for c in df.columns if 'courier' in c.lower()
                   or 'status' in c.lower()]
    if not courier_col:
        print("   ⚠️  No courier/status column found — skipping")
        return
    courier_col = courier_col[0]

    status_counts = df[courier_col].value_counts().reset_index()
    status_counts.columns = ['status', 'count']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- Left: Donut Chart ---
    wedges, texts, autotexts = ax1.pie(
        status_counts['count'],
        labels=status_counts['status'],
        autopct='%1.1f%%',
        colors=PALETTE[:len(status_counts)],
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2,
                    'width': 0.6}   # width < 1 makes it a donut
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax1.set_title('🚚 Order Delivery Status\n(Donut Chart)',
                  fontsize=14, fontweight='bold', color=AMAZON_DARK)

    # --- Right: Horizontal Bar ---
    status_sorted = status_counts.sort_values('count')
    colors_bar = [AMAZON_ORANGE if 'Shipped' in str(s)
                  else '#DC3545' if 'Cancel' in str(s)
                  else AMAZON_BLUE
                  for s in status_sorted['status']]

    bars = ax2.barh(status_sorted['status'],
                    status_sorted['count'],
                    color=colors_bar, edgecolor='white')

    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 100, bar.get_y() + bar.get_height() / 2,
                 f'{int(w):,}', va='center', fontsize=10,
                 fontweight='bold')

    ax2.set_title('🚚 Delivery Status Count',
                  fontsize=14, fontweight='bold', color=AMAZON_DARK)
    ax2.set_xlabel('Number of Orders')
    ax2.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.tight_layout()
    save_chart("03_courier_status.png")
    plt.show()

    # Find cancellation rate
    cancel = status_counts[status_counts['status'].str.contains(
        'Cancel', case=False, na=False)]
    if not cancel.empty:
        cancel_pct = cancel['count'].sum() / status_counts['count'].sum() * 100
        print(f"\n   🔍 INSIGHT: {cancel_pct:.1f}% of orders are cancelled.")
        print(f"   💼 ACTION: Investigate cancellation reasons — "
              f"this directly impacts revenue.")
    else:
        print(f"\n   🔍 INSIGHT: Delivery status breakdown shown above.")


# =============================================================
# CHART 4: Sales Channel Analysis — Bar + Pie
# BUSINESS QUESTION: Which channel (Amazon.in vs Non-Amazon)
#                    generates more orders?
# =============================================================

def chart_4_sales_channel(df):
    print("\n📊 Chart 4: Sales Channel Analysis")

    channel_col = [c for c in df.columns
                   if 'channel' in c.lower() or 'sales' in c.lower()]
    # Avoid picking up 'amount' or numeric cols accidentally
    channel_col = [c for c in channel_col
                   if df[c].dtype == 'object']
    if not channel_col:
        print("   ⚠️  No sales channel column found — skipping")
        return
    channel_col = channel_col[0]

    channel_counts = df[channel_col].value_counts().reset_index()
    channel_counts.columns = ['channel', 'count']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- Left: Bar ---
    bars = ax1.bar(channel_counts['channel'],
                   channel_counts['count'],
                   color=[AMAZON_ORANGE, AMAZON_BLUE,
                          AMAZON_DARK][:len(channel_counts)],
                   edgecolor='white', linewidth=0.8, width=0.5)

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.,
                 h + 200, f'{int(h):,}',
                 ha='center', va='bottom',
                 fontsize=11, fontweight='bold')

    ax1.set_title('🛒 Orders by Sales Channel',
                  fontsize=14, fontweight='bold', color=AMAZON_DARK)
    ax1.set_xlabel('Sales Channel')
    ax1.set_ylabel('Number of Orders')
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # --- Right: Pie ---
    ax2.pie(channel_counts['count'],
            labels=channel_counts['channel'],
            autopct='%1.1f%%',
            colors=[AMAZON_ORANGE, AMAZON_BLUE,
                    AMAZON_DARK][:len(channel_counts)],
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax2.set_title('🛒 Channel Share (%)',
                  fontsize=14, fontweight='bold', color=AMAZON_DARK)

    plt.tight_layout()
    save_chart("04_sales_channel.png")
    plt.show()

    top_ch = channel_counts.iloc[0]['channel']
    top_pct = (channel_counts.iloc[0]['count'] /
               channel_counts['count'].sum() * 100)
    print(f"\n   🔍 INSIGHT: '{top_ch}' dominates with "
          f"{top_pct:.1f}% of all orders.")
    print(f"   💼 ACTION: Focus marketing budget on '{top_ch}' "
          f"for maximum ROI.")


# =============================================================
# CHART 5: Category vs Size Heatmap
# BUSINESS QUESTION: Which size is most popular in each category?
# =============================================================

def chart_5_category_size_heatmap(df):
    print("\n📊 Chart 5: Category × Size Heatmap")

    cat_col  = [c for c in df.columns if 'category' in c.lower()]
    size_col = [c for c in df.columns if 'size' in c.lower()]

    if not cat_col or not size_col:
        print("   ⚠️  Missing category or size column — skipping")
        return

    cat_col  = cat_col[0]
    size_col = size_col[0]

    # Create a pivot table: rows=Category, cols=Size, values=count
    # This is exactly like an Excel Pivot Table!
    pivot = (df.groupby([cat_col, size_col])
               .size()
               .unstack(fill_value=0))

    # Keep only top 10 sizes for readability
    top_sizes = df[size_col].value_counts().head(10).index
    pivot = pivot[[s for s in top_sizes if s in pivot.columns]]

    fig, ax = plt.subplots(figsize=(16, 8))

    sns.heatmap(pivot,
                annot=True,           # show numbers in cells
                fmt=',',              # format as 1,234
                cmap='YlOrRd',        # yellow → red color scale
                linewidths=0.5,
                linecolor='white',
                ax=ax,
                cbar_kws={'label': 'Number of Orders'})

    ax.set_title('🔥 Orders Heatmap: Category × Size',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Size', fontsize=12)
    ax.set_ylabel('Category', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    save_chart("05_category_size_heatmap.png")
    plt.show()

    print(f"\n   🔍 INSIGHT: Darker cells = highest demand "
          f"combinations.")
    print(f"   💼 ACTION: Use this heatmap for inventory "
          f"planning — stock more of the dark red combinations.")


# =============================================================
# CHART 6: Courier Status by Category — Stacked Bar
# BUSINESS QUESTION: Which categories have the most cancellations?
# =============================================================

def chart_6_status_by_category(df):
    print("\n📊 Chart 6: Courier Status by Category")

    cat_col     = [c for c in df.columns if 'category' in c.lower()]
    courier_col = [c for c in df.columns if 'courier' in c.lower()
                   or 'status' in c.lower()]

    if not cat_col or not courier_col:
        print("   ⚠️  Missing columns — skipping")
        return

    cat_col     = cat_col[0]
    courier_col = courier_col[0]

    # Pivot: each row = category, each col = status, value = count
    pivot = (df.groupby([cat_col, courier_col])
               .size()
               .unstack(fill_value=0))

    # Normalize to percentages so categories are comparable
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(14, 7))

    pivot_pct.plot(kind='bar',
                   stacked=True,
                   ax=ax,
                   color=PALETTE[:len(pivot_pct.columns)],
                   edgecolor='white',
                   linewidth=0.5)

    ax.set_title('📦 Delivery Status by Category (%)',
                 fontsize=16, fontweight='bold', color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Product Category', fontsize=12)
    ax.set_ylabel('Percentage of Orders (%)', fontsize=12)
    ax.legend(title='Courier Status',
              bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    save_chart("06_status_by_category.png")
    plt.show()

    print(f"\n   🔍 INSIGHT: Categories with high red/cancel bars "
          f"need supply chain investigation.")
    print(f"   💼 ACTION: Flag high-cancellation categories for "
          f"operations team review.")


# =============================================================
# CHART 7: Sales Channel by Category — Grouped Bar
# BUSINESS QUESTION: Which categories sell more on which channel?
# =============================================================

def chart_7_channel_by_category(df):
    print("\n📊 Chart 7: Sales Channel by Category")

    cat_col     = [c for c in df.columns if 'category' in c.lower()]
    channel_col = [c for c in df.columns
                   if 'channel' in c.lower() and
                   df[c].dtype == 'object']

    if not cat_col or not channel_col:
        print("   ⚠️  Missing columns — skipping")
        return

    cat_col     = cat_col[0]
    channel_col = channel_col[0]

    pivot = (df.groupby([cat_col, channel_col])
               .size()
               .unstack(fill_value=0))

    fig, ax = plt.subplots(figsize=(14, 7))

    pivot.plot(kind='bar',
               ax=ax,
               color=[AMAZON_ORANGE, AMAZON_BLUE,
                      AMAZON_DARK][:len(pivot.columns)],
               edgecolor='white',
               linewidth=0.5,
               width=0.7)

    ax.set_title('🛒 Sales Channel by Product Category',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Product Category', fontsize=12)
    ax.set_ylabel('Number of Orders', fontsize=12)
    ax.legend(title='Sales Channel',
              bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    save_chart("07_channel_by_category.png")
    plt.show()

    print(f"\n   🔍 INSIGHT: Some categories may perform better "
          f"on specific channels.")
    print(f"   💼 ACTION: Tailor channel-specific promotions "
          f"per category.")


# =============================================================
# CHART 8: Top 10 SKUs by Order Volume
# BUSINESS QUESTION: Which specific products sell the most?
# =============================================================

def chart_8_top_skus(df):
    print("\n📊 Chart 8: Top 10 Best-Selling SKUs")

    sku_col = [c for c in df.columns if 'sku' in c.lower()
               or 'asin' in c.lower() or 'product' in c.lower()]
    if not sku_col:
        print("   ⚠️  No SKU/product column found — skipping")
        return
    sku_col = sku_col[0]

    top_skus = (df[sku_col]
                .value_counts()
                .head(10)
                .reset_index())
    top_skus.columns = ['sku', 'count']
    top_skus = top_skus.sort_values('count')  # ascending for horizontal bar

    fig, ax = plt.subplots(figsize=(12, 8))

    # Color gradient: darker = more orders
    colors = plt.cm.YlOrRd(
        np.linspace(0.3, 0.9, len(top_skus)))

    bars = ax.barh(top_skus['sku'],
                   top_skus['count'],
                   color=colors,
                   edgecolor='white')

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 10,
                bar.get_y() + bar.get_height() / 2,
                f'{int(w):,}',
                va='center', fontsize=10, fontweight='bold')

    ax.set_title('🏆 Top 10 Best-Selling SKUs',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Number of Orders', fontsize=12)
    ax.set_ylabel('SKU / Product', fontsize=12)
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout()
    save_chart("08_top_skus.png")
    plt.show()

    top_sku = top_skus.iloc[-1]['sku']
    print(f"\n   🔍 INSIGHT: '{top_sku}' is your #1 best-selling SKU.")
    print(f"   💼 ACTION: Ensure this SKU is always in stock "
          f"and featured prominently in listings.")


# =============================================================
# CHART 9: Order Status Funnel
# BUSINESS QUESTION: How do orders flow from placed → delivered?
# =============================================================

def chart_9_order_funnel(df):
    print("\n📊 Chart 9: Order Status Funnel")

    status_col = [c for c in df.columns
                  if 'status' in c.lower()]
    if not status_col:
        print("   ⚠️  No status column found — skipping")
        return
    status_col = status_col[0]

    status_counts = (df[status_col]
                     .value_counts()
                     .reset_index())
    status_counts.columns = ['status', 'count']
    status_counts = status_counts.sort_values('count', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Create funnel-style bar chart with decreasing width
    bar_colors = []
    for s in status_counts['status']:
        s_lower = str(s).lower()
        if 'ship' in s_lower or 'deliver' in s_lower:
            bar_colors.append('#28A745')   # green = good
        elif 'cancel' in s_lower:
            bar_colors.append('#DC3545')   # red = bad
        elif 'return' in s_lower:
            bar_colors.append('#FFC107')   # yellow = warning
        else:
            bar_colors.append(AMAZON_BLUE) # default

    bars = ax.bar(range(len(status_counts)),
                  status_counts['count'],
                  color=bar_colors,
                  edgecolor='white',
                  linewidth=0.8)

    for i, bar in enumerate(bars):
        h = bar.get_height()
        pct = h / status_counts['count'].sum() * 100
        ax.text(bar.get_x() + bar.get_width() / 2.,
                h + 100,
                f'{int(h):,}\n({pct:.1f}%)',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold')

    ax.set_xticks(range(len(status_counts)))
    ax.set_xticklabels(status_counts['status'],
                       rotation=30, ha='right', fontsize=10)
    ax.set_title('📬 Order Status Breakdown',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_ylabel('Number of Orders', fontsize=12)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Add color legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#28A745', label='Shipped/Delivered'),
        Patch(facecolor='#DC3545', label='Cancelled'),
        Patch(facecolor='#FFC107', label='Returned'),
        Patch(facecolor=AMAZON_BLUE, label='Other'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()
    save_chart("09_order_status_funnel.png")
    plt.show()

    total = status_counts['count'].sum()
    print(f"\n   🔍 INSIGHT: Full order lifecycle breakdown shown.")
    print(f"   💼 ACTION: Green = revenue. Red/Yellow = loss. "
          f"Minimize red to protect revenue.")


# =============================================================
# CHART 10: Category vs Courier Status — 100% Stacked Bar
# BUSINESS QUESTION: Fulfillment efficiency per category
# =============================================================

def chart_10_fulfillment_efficiency(df):
    print("\n📊 Chart 10: Fulfillment Efficiency by Category")

    cat_col     = [c for c in df.columns if 'category' in c.lower()]
    courier_col = [c for c in df.columns if 'courier' in c.lower()
                   or 'status' in c.lower()]

    if not cat_col or not courier_col:
        print("   ⚠️  Missing columns — skipping")
        return

    cat_col     = cat_col[0]
    courier_col = courier_col[0]

    # Build pivot with % breakdown
    pivot = (df.groupby([cat_col, courier_col])
               .size()
               .unstack(fill_value=0))
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    # Sort by "Shipped" column descending if it exists
    shipped_col = [c for c in pivot_pct.columns
                   if 'ship' in str(c).lower()]
    if shipped_col:
        pivot_pct = pivot_pct.sort_values(
            shipped_col[0], ascending=False)

    fig, ax = plt.subplots(figsize=(14, 8))

    pivot_pct.plot(kind='barh',
                   stacked=True,
                   ax=ax,
                   color=PALETTE[:len(pivot_pct.columns)],
                   edgecolor='white',
                   linewidth=0.5)

    ax.set_title('⚙️ Fulfillment Efficiency by Category (%)',
                 fontsize=16, fontweight='bold',
                 color=AMAZON_DARK, pad=20)
    ax.set_xlabel('Percentage (%)', fontsize=12)
    ax.set_ylabel('Category', fontsize=12)
    ax.legend(title='Order Status',
              bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.axvline(x=80, color='red', linestyle='--',
               alpha=0.5, label='80% target line')
    plt.tight_layout()
    save_chart("10_fulfillment_efficiency.png")
    plt.show()

    print(f"\n   🔍 INSIGHT: Categories with <80% shipped rate "
          f"need logistics review.")
    print(f"   💼 ACTION: Set KPI target: 90%+ fulfillment rate "
          f"per category.")


# =============================================================
# CHART 11: SKU Concentration — Top 20 vs Rest
# BUSINESS QUESTION: Do 20% of SKUs drive 80% of orders?
#                    (Pareto / 80-20 Rule)
# =============================================================

def chart_11_pareto_sku(df):
    print("\n📊 Chart 11: Pareto Analysis — SKU Concentration")

    sku_col = [c for c in df.columns
               if 'sku' in c.lower() or 'asin' in c.lower()]
    if not sku_col:
        print("   ⚠️  No SKU column found — skipping")
        return
    sku_col = sku_col[0]

    sku_counts = df[sku_col].value_counts().reset_index()
    sku_counts.columns = ['sku', 'count']
    sku_counts = sku_counts.sort_values('count', ascending=False)
    sku_counts['cumulative_pct'] = (
        sku_counts['count'].cumsum() /
        sku_counts['count'].sum() * 100
    )
    sku_counts['sku_rank_pct'] = (
        np.arange(1, len(sku_counts) + 1) /
        len(sku_counts) * 100
    )

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Bar chart for order counts (top 30 SKUs)
    top30 = sku_counts.head(30)
    ax1.bar(range(len(top30)),
            top30['count'],
            color=AMAZON_ORANGE,
            alpha=0.8,
            label='Order Count')
    ax1.set_xlabel('SKU Rank (Top 30)', fontsize=12)
    ax1.set_ylabel('Orders per SKU', color=AMAZON_ORANGE, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=AMAZON_ORANGE)

    # Line chart for cumulative % (secondary axis)
    ax2 = ax1.twinx()
    ax2.plot(sku_counts['sku_rank_pct'],
             sku_counts['cumulative_pct'],
             color=AMAZON_DARK,
             linewidth=2.5,
             label='Cumulative %')
    ax2.axhline(y=80, color='red', linestyle='--',
                alpha=0.7, label='80% line')
    ax2.set_ylabel('Cumulative Order % ', color=AMAZON_DARK, fontsize=12)
    ax2.set_ylim(0, 105)

    ax1.set_title('📈 Pareto Analysis: Do Top SKUs Drive 80% of Orders?',
                  fontsize=16, fontweight='bold',
                  color=AMAZON_DARK, pad=20)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               loc='center right')
    plt.tight_layout()
    save_chart("11_pareto_sku.png")
    plt.show()

    # Find what % of SKUs drive 80% of orders
    skus_for_80 = sku_counts[
        sku_counts['cumulative_pct'] <= 80]
    pct_skus = len(skus_for_80) / len(sku_counts) * 100
    print(f"\n   🔍 INSIGHT: Top {pct_skus:.1f}% of SKUs drive "
          f"80% of all orders — classic Pareto pattern.")
    print(f"   💼 ACTION: Focus inventory investment and ads "
          f"on these top SKUs only.")


# =============================================================
# SECTION: SUMMARY STATISTICS REPORT
# =============================================================

def print_summary_report(df):
    """Print a clean business summary of the entire dataset"""

    print("\n" + "="*60)
    print("📊 AMAZON SALES — EXECUTIVE SUMMARY REPORT")
    print("="*60)

    print(f"\n📦 Total Orders Analysed : {len(df):,}")
    print(f"🗂️  Total Columns         : {df.shape[1]}")

    # Category summary
    cat_col = [c for c in df.columns if 'category' in c.lower()]
    if cat_col:
        print(f"\n📂 Product Categories    : "
              f"{df[cat_col[0]].nunique()} unique")
        print(f"   Top Category         : "
              f"{df[cat_col[0]].value_counts().index[0]}")

    # Size summary
    size_col = [c for c in df.columns if 'size' in c.lower()]
    if size_col:
        print(f"\n👕 Size Variants         : "
              f"{df[size_col[0]].nunique()} unique")
        print(f"   Most Ordered Size    : "
              f"{df[size_col[0]].value_counts().index[0]}")

    # Channel summary
    channel_col = [c for c in df.columns
                   if 'channel' in c.lower()
                   and df[c].dtype == 'object']
    if channel_col:
        print(f"\n🛒 Sales Channels        : "
              f"{df[channel_col[0]].nunique()} unique")
        print(f"   Top Channel          : "
              f"{df[channel_col[0]].value_counts().index[0]}")

    # SKU summary
    sku_col = [c for c in df.columns if 'sku' in c.lower()]
    if sku_col:
        print(f"\n🏷️  Unique SKUs           : "
              f"{df[sku_col[0]].nunique():,}")

    print("\n" + "="*60)
    print("✅ EDA Complete — Charts saved to /visualizations/")
    print("="*60)


# =============================================================
# MAIN: RUN ALL CHARTS IN ORDER
# =============================================================

if __name__ == "__main__":

    print("🚀 Starting Amazon Sales EDA...")
    print("="*60)

    # Load cleaned data
    df = load_cleaned_data()

    # Run all 11 charts
    chart_1_sales_by_category(df)
    chart_2_size_distribution(df)
    chart_3_courier_status(df)
    chart_4_sales_channel(df)
    chart_5_category_size_heatmap(df)
    chart_6_status_by_category(df)
    chart_7_channel_by_category(df)
    chart_8_top_skus(df)
    chart_9_order_funnel(df)
    chart_10_fulfillment_efficiency(df)
    chart_11_pareto_sku(df)

    # Print final summary
    print_summary_report(df)