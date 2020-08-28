from pandas_profiling.config import config
from pandas_profiling.report.formatters import fmt_array
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import histogram, mini_histogram


def render_count(summary):
    varid = summary["varid"]
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Real number (&Ropf; / &Ropf;<sub>&ge;0</sub>)",
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
        [
            {
                "name": "唯一值计数",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "唯一值 (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "alert": False,
            },
            {
                "name": "缺失值",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "缺失值比例 (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "alert": False,
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
                "alert": False,
            },
            {
                "name": "零值 (%)",
                "value": summary["p_zeros"],
                "fmt": "fmt_percent",
                "alert": False,
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

    quantile_statistics = {
        "name": "定性分析",
        "items": [
            {
                "name": "最小值",
                "value": summary["min"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "5-th 百分位",
                "value": summary["quantile_5"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Q1",
                "value": summary["quantile_25"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "中位数",
                "value": summary["quantile_50"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Q3",
                "value": summary["quantile_75"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "95-th 百分位",
                "value": summary["quantile_95"],
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
                "name": "区间",
                "value": summary["range"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "四分位距",
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
        ],
    }

    descriptive_statistics = {
        "name": "描述性统计",
        "items": [
            {
                "name": "标准差",
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "变异系数",
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": "峰度", "value": summary["kurt"], "fmt": "fmt_numeric"},
            {"name": "均数", "value": summary["mean"], "fmt": "fmt_numeric"},
            {"name": "MAD", "value": summary["mad"], "fmt": "fmt_numeric"},
            {"name": "偏度", "value": summary["skew"], "fmt": "fmt_numeric"},
            {"name": "积", "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": "方差", "value": summary["var"], "fmt": "fmt_numeric"},
        ],
    }

    # TODO: Make sections data structure
    # statistics = ItemRenderer(
    #     'statistics',
    #     'Statistics',
    #     'table',
    #     [
    #         quantile_statistics,
    #         descriptive_statistics
    #     ]
    # )

    seqs = [
        Image(
            histogram(*summary["histogram"]),
            image_format=image_format,
            alt="Histogram",
            caption=f"<strong>Histogram with fixed size bins</strong> (bins={len(summary['histogram'][1]) - 1})",
            name="Histogram",
            anchor_id="histogram",
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id="common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name="Minimum 5 values",
                anchor_id="firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="Maximum 5 values",
                anchor_id="lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name="极值",
        anchor_id="extreme_values",
    )

    template_variables["bottom"] = Container(
        [
            # statistics,
            Container(
                seqs, sequence_type="tabs", name="直方图", anchor_id="histograms"
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    return template_variables
