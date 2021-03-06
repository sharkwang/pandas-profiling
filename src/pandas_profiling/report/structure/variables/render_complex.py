from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.visualisation.plot import scatter_complex


def render_complex(summary):
    varid = summary["varid"]
    template_variables = {}
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Complex number (&Copf;)",
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
        [
            {"name": "唯一值计数", "value": summary["n_unique"], "fmt": "fmt"},
            {"name": "唯一值比例 (%)", "value": summary["p_unique"], "fmt": "fmt_percent"},
            {"name": "缺失值", "value": summary["n_missing"], "fmt": "fmt"},
            {
                "name": "缺失值比例(%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
            },
            {
                "name": "内存占用",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    table2 = Table(
        [
            {"name": "均数", "value": summary["mean"], "fmt": "fmt_numeric"},
            {"name": "最小值", "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": "最大值", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "零值", "value": summary["n_zeros"], "fmt": "fmt_numeric"},
            {"name": "零值比例 (%)", "value": summary["p_zeros"], "fmt": "fmt_percent"},
        ]
    )

    placeholder = HTML("")

    template_variables["top"] = Container(
        [info, table1, table2, placeholder], sequence_type="grid"
    )

    # Bottom
    items = [
        Image(
            scatter_complex(summary["scatter_data"]),
            image_format=image_format,
            alt="Scatterplot",
            caption="Scatterplot in the complex plane",
            name="Scatter",
            anchor_id=f"{varid}scatter",
        )
    ]

    bottom = Container(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables
