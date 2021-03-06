from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.visualisation.plot import histogram, mini_histogram


def render_date(summary):
    varid = summary["varid"]
    # TODO: render common?
    template_variables = {}

    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Date",
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
                "name": "唯一值比例 (%)",
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
                "name": "缺失值比例(%)",
                "value": summary["p_missing"],
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

    table2 = Table(
        [
            {"name": "最小", "value": summary["min"], "fmt": "fmt", "alert": False},
            {"name": "最大", "value": summary["max"], "fmt": "fmt", "alert": False},
        ]
    )

    mini_histo = Image(
        mini_histogram(*summary["histogram"], date=True),
        image_format=image_format,
        alt="Mini histogram",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    # Bottom
    bottom = Container(
        [
            Image(
                histogram(*summary["histogram"], date=True),
                image_format=image_format,
                alt="Histogram",
                caption=f"<strong>Histogram with fixed size bins</strong> (bins={len(summary['histogram'][1]) - 1})",
                name="Histogram",
                anchor_id=f"{varid}histogram",
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
