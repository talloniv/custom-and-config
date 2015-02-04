import matplotlib as mpl
import matplotlib.pyplot as plt

import radar

import demodata


colors = mpl.rcParams['axes.color_cycle']

def hide_axes(axes):
    axes.set_frame_on(False)
    [n.set_visible(False) for n in axes.get_xticklabels() + axes.get_yticklabels()]
    [n.set_visible(False) for n in axes.get_xticklines() + axes.get_yticklines()]

def make_autos_radar_plot(figure, gs, pddata):
    min_data = pddata.groupby("make", sort=True).min()
    max_data = pddata.groupby("make", sort=True).max()
    mean_data = pddata.groupby("make", sort=True).mean()
    projection = radar.RadarAxes(spoke_count=len(mean_data.columns))
    (row_num, col_num) = gs.get_geometry()
    # setup title grid axes
    title_axes = figure.add_subplot(gs[0, :])
    title_axes.set_title("Radar Plot on 7 Dimensions\nFor 12 Manufacturers",
                         fontsize=20)
    hide_axes(title_axes)
    # setup inner grid axes
    inner_axes = [plt.subplot(m, projection=projection) for m in [n for n in gs][col_num:]]
    for i, make in enumerate(demodata.get_make_names(pddata)):
        axes = inner_axes[i]
        axes.set_title(
            make.title(), size='large', position=(0.5, 1.1),
            horizontalalignment='center', verticalalignment='center')
        for (color, alpha, data) in zip([1, 2, 0],
                                        [0.2, 0.3, 0.4],
                                        [max_data, mean_data, min_data]):
            axes.fill(axes.radar_theta, data.loc[make], color=colors[color],
                      alpha=alpha)
            axes.plot(axes.radar_theta, data.loc[make], color=colors[color])
        axes.set_varlabels([x.replace(" ", "\n") for x in mean_data.columns])
        axes.set_yticklabels([])
    gs.tight_layout(figure)
    return [title_axes, inner_axes]


def make_empty_plot(figure, gs):
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Empty Plot", fontsize=20)
    gs.tight_layout(figure)
    return axes


def make_autos_mpg_plot(figure, gs, pddata):
    data = demodata.get_numeric_data(pddata)
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Ranges of City and Highway MPG", fontsize=20)
    axes.scatter(data["make"], data["highway mpg"], c=colors[3],
                 s=500, alpha=0.4)
    axes.scatter(data["make"], data["city mpg"], c=colors[0],
                 s=500, alpha=0.4)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(demodata.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("MPG", fontsize=16)
    city_patch = mpl.patches.Patch(color=colors[0], alpha=0.7, label="City")
    highway_patch = mpl.patches.Patch(color=colors[3], alpha=0.7, label="Highway")
    axes.legend(handles=[city_patch, highway_patch], loc=2)
    gs.tight_layout(figure)
    return axes


def make_autos_price_plot(figure, gs, pddata):
    min_data = pddata.groupby("make", sort=True)["price"].min()
    max_data = pddata.groupby("make", sort=True)["price"].max()
    mean_data = pddata.groupby("make", sort=True)["price"].mean()
    make_ids = demodata.get_make_ids(pddata)
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Auto Price Ranges", fontsize=20)
    axes.plot(make_ids, min_data, c=colors[2], linewidth=4, alpha=0.7)
    axes.plot(make_ids, mean_data, c=colors[3], linewidth=4, alpha=0.7)
    axes.plot(make_ids, max_data, c=colors[4], linewidth=4, alpha=0.7)
    axes.set_xticks(range(-1, 13))
    axes.set_xticklabels([" "] + demodata.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("Price", fontsize=16)
    high_patch = mpl.patches.Patch(color=colors[4], alpha=0.7, label="High")
    mean_patch = mpl.patches.Patch(color=colors[3], alpha=0.7, label="Mean")
    low_patch = mpl.patches.Patch(color=colors[2], alpha=0.7, label="Low")
    axes.legend(handles=[high_patch, mean_patch, low_patch], loc=2)
    gs.tight_layout(figure)
    return axes


def make_autos_riskiness_plot(figure, gs, pddata):
    risk_mins = pddata.groupby("make")["riskiness"].min().values
    risk_means = pddata.groupby("make")["riskiness"].mean().values
    risk_maxs = pddata.groupby("make")["riskiness"].max().values
    make_ids = demodata.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Stacked Riskiness (Inverted, Normalized)", fontsize=20)
    mins_bar = axes.bar(make_ids, risk_mins, width=0.5, align="center",
                        color=min_color, alpha=0.7)
    means_bar = axes.bar(make_ids, risk_means, width=0.5, align="center",
                         bottom=risk_mins, color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, risk_maxs, width=0.5, align="center",
                        bottom=risk_means + risk_mins, color=max_color, alpha=0.7)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(demodata.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("Inverse Risk", fontsize=16)
    axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc=2)
    gs.tight_layout(figure)
    return axes


def make_autos_losses_plot(figure, gs, pddata):
    loss_mins = pddata.groupby("make")["losses"].min().values
    loss_means = pddata.groupby("make")["losses"].mean().values
    loss_maxs = pddata.groupby("make")["losses"].max().values
    make_ids = demodata.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title("Stacked Losses (Inverted, Normalized)", fontsize=20)
    mins_bar = axes.bar(make_ids, loss_mins, width=0.5, align="center",
                        color=min_color, alpha=0.7)
    means_bar = axes.bar(make_ids, loss_means, width=0.5, align="center",
                         bottom=loss_mins, color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, loss_maxs, width=0.5, align="center",
                        bottom=loss_means + loss_mins, color=max_color, alpha=0.7)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(demodata.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("Inverse Losses", fontsize=16)
    axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc=2)
    gs.tight_layout(figure)
    return axes


def make_autos_loss_and_risk_plot(figure, gs, pddata):
    risk_mins = pddata.groupby("make")["riskiness"].min().values
    risk_means = pddata.groupby("make")["riskiness"].mean().values
    risk_maxs = pddata.groupby("make")["riskiness"].max().values
    loss_mins = pddata.groupby("make")["losses"].min().values
    loss_means = pddata.groupby("make")["losses"].mean().values
    loss_maxs = pddata.groupby("make")["losses"].max().values
    mins = risk_mins + loss_mins
    means = risk_means + loss_means
    maxs = risk_maxs + loss_maxs
    make_ids = demodata.get_make_ids(pddata)
    min_color = colors[0]
    mean_color = colors[3]
    max_color = colors[2]
    axes = figure.add_subplot(gs[0, 0])
    axes.set_title(("Stacked Combined Losses and Riskiness Data\n"
                    "(Inverted, Normalized)"),
                   fontsize=20)
    mins_bar = axes.bar(make_ids, mins, align="center", color=min_color,
                        alpha=0.7)
    means_bar = axes.bar(make_ids, means, align="center", bottom=mins,
                         color=mean_color, alpha=0.7)
    maxs_bar = axes.bar(make_ids, maxs, align="center", bottom=means + mins,
                        color=max_color, alpha=0.7)
    axes.set_xticks(range(0, 13))
    axes.set_xticklabels(demodata.get_make_labels(pddata))
    axes.set_xlabel("Make", fontsize=16)
    axes.set_ylabel("Inverse Losses\nand Riskiness", fontsize=16)
    axes.legend([mins_bar, means_bar, maxs_bar], ["Min", "Mean", "Max"], loc=2)
    gs.tight_layout(figure)
    return axes
