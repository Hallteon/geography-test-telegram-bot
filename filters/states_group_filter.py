from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter

from states import Test


class IsInStatesGroup(BoundFilter):

    async def check(self, callback: types.CallbackQuery, state: FSMContext):
        state_name = await state.get_state()

        return state_name in Test.all_states_names[1:]



