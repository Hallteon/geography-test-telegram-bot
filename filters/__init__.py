from .states_group_filter import IsInStatesGroup
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsInStatesGroup)