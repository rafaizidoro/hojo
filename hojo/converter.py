from datetime import date

from cattrs import Converter
from cattrs.preconf.json import make_converter
from pendulum import date, datetime
from pendulum import parser as pendulum_parser

SchemaConverter = make_converter()

# pendulum Date
# SchemaConverter.register_unstructure_hook(date, lambda dt: dt.to_date_string())
# SchemaConverter.register_structure_hook(
#     Date, lambda dt, _: pendulum_parser.parse(dt).date()
# )


# # pendulum DateTime
# SchemaConverter.register_unstructure_hook(datetime, lambda dt: dt.to_date_string())
# SchemaConverter.register_structure_hook(date, lambda dt, _: pendulum_parser.(dt))
