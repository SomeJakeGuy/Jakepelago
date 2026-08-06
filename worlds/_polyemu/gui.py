import typing

from kivy.metrics import dp
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.menu import MDDropdownMenu

import Utils
from .core import AutoAdapterRegister

if typing.TYPE_CHECKING:
    from kvui import GameManager
    from .context import PolyEmuClientContext


def build_manager(base_ui: "type[GameManager]") -> "type[GameManager]":
    class PolyEmuManager(base_ui):
        ctx: "PolyEmuClientContext"

        adapter_dropdown_item: MDDropDownItem
        adapter_dropdown_label: MDDropDownItemText
        adapter_menu: MDDropdownMenu

        def build(self):
            container = super().build()
            self._build_adapter_selector()
            return container

        def _build_adapter_selector(self) -> None:
            current_name = self.ctx.polyemu_ctx.adapter.name

            self.adapter_dropdown_label = MDDropDownItemText(text=current_name, font_style="Title", role="small")
            self.adapter_dropdown_item = MDDropDownItem(
                self.adapter_dropdown_label,
                size_hint_x=None, width=dp(220),
                size_hint_y=None, height=dp(40),
                pos_hint={"center_y": 0.5},
            )

            menu_items = [
                {
                    "text": adapter_name,
                    "on_release": lambda name=adapter_name: self._on_adapter_selected(name),
                }
                for adapter_name in AutoAdapterRegister.adapter_types
            ]
            self.adapter_menu = MDDropdownMenu(
                caller=self.adapter_dropdown_item, items=menu_items, width=dp(220),
            )
            self.adapter_dropdown_item.bind(on_release=lambda *args: self.adapter_menu.open())

            self.connect_layout.add_widget(self.adapter_dropdown_item)

        def _on_adapter_selected(self, adapter_name: str) -> None:
            self.adapter_menu.dismiss()

            if adapter_name == self.ctx.polyemu_ctx.adapter.name:
                return

            self.adapter_dropdown_label.text = adapter_name
            Utils.async_start(self.ctx.switch_adapter(adapter_name))

    return PolyEmuManager