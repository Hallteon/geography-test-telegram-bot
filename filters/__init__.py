from .is_admin_filter import IsAdmin
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)