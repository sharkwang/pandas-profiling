from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import histogram, mini_histogram


def render_real(summary):
    varid = summary["varid"]
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    if summary["min"] >= 0:
        name = "Real number (&Ropf;<sub>&ge;0</sub>)"
    else:
        name = "Real number (&Ropf;)"

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        name,
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
        [
            {
                "name": "唯一值计数",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "alert": "n_unique" in summary["warn_fields"],
            },
            {
                "name": "唯一值比例 (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "alert": "p_unique" in summary["warn_fields"],
            },
            {
                "name": "缺失值",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "alert": "n_missing" in summary["warn_fields"],
            },
            {
                "name": "缺失值比例(%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "alert": "p_missing" in summary["warn_fields"],
            },
            {
                "name": "无穷值",
                "value": summary["n_infinite"],
                "fmt": "fmt",
                "alert": "n_infinite" in summary["warn_fields"],
            },
            {
                "name": "无穷值比例 (%)",
                "value": summary["p_infinite"],
                "fmt": "fmt_percent",
                "alert": "p_infinite" in summary["warn_fields"],
            },
        ]
    )

    table2 = Table(
        [
            {
                "name": "均数",
                "value": summary["mean"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "最小值",
                "value": summary["min"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "最大值",
                "value": summary["max"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "零值",
                "value": summary["n_zeros"],
                "fmt": "fmt",
                "alert": "n_zeros" in summary["warn_fields"],
            },
            {
                "name": "零值比例 (%)",
                "value": summary["p_zeros"],
                "fmt": "fmt_percent",
                "alert": "p_zeros" in summary["warn_fields"],
            },
            {
                "name": "内存占用",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    mini_histo = Image(
        mini_histogram(*summary["histogram"]),
        image_format=image_format,
        alt="Mini histogram",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {"name": "最小值", "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": "5百分位", "value": summary["5%"], "fmt": "fmt_numeric"},
            {"name": "25百分位", "value": summary["25%"], "fmt": "fmt_numeric"},
            {"name": "中位", "value": summary["50%"], "fmt": "fmt_numeric"},
            {"name": "75百分位", "value": summary["75%"], "fmt": "fmt_numeric"},
            {"name": "95-百分位", "value": summary["95%"], "fmt": "fmt_numeric"},
            {"name": "最大值", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "极差", "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": "四分位距 (IQR)",
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
        name="定性统计",
    )

    if summary["monotonic_increase_strict"]:
        monotocity = "严格递增"
    elif summary["monotonic_decrease_strict"]:
        monotocity = "严格递减"
    elif summary["monotonic_increase"]:
        monotocity = "递增"
    elif summary["monotonic_decrease"]:
        monotocity = "递减"
    else:
        monotocity = "非单调"

    descriptive_statistics = Table(
        [
            {
                "name": "标准差",
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "变异系数 (CV)",
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": "峰度", "value": summary["kurtosis"], "fmt": "fmt_numeric"},
            {"name": "均数", "value": summary["mean"], "fmt": "fmt_numeric"},
            {
                "name": "中位绝对偏差 (MAD)",
                "value": summary["mad"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "偏度",
                "value": summary["skewness"],
                "fmt": "fmt_numeric",
                "class": "alert" if "skewness" in summary["warn_fields"] else "",
            },
            {"name": "总和", "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": "方差", "value": summary["variance"], "fmt": "fmt_numeric"},
            {"name": "单调性", "value": monotocity, "fmt": "fmt"},
        ],
        name="描述性统计",
    )

    statistics = Container(
        [quantile_statistics, descriptive_statistics],
        anchor_id=f"{varid}statistics",
        name="统计",
        sequence_type="grid",
    )

    hist = Image(
        histogram(*summary["histogram"]),
        image_format=image_format,
        alt="Histogram",
        caption=f"<strong>固定大小的直方图</strong> (bins={len(summary['histogram'][1]) - 1})",
        name="直方图",
        anchor_id=f"{varid}histogram",
    )

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="常见值",
        anchor_id=f"{varid}common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name="最小10个",
                anchor_id=f"{varid}firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="最大10个",
                anchor_id=f"{varid}lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name="极值",
        anchor_id=f"{varid}extreme_values",
    )

    template_variables["bottom"] = Container(
        [statistics, hist, fq, evs], sequence_type="tabs", anchor_id=f"{varid}bottom",
    )

    return template_variables
