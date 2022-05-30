import subprocess, os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction


class WifiPicker(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):

        output = []

        try:
            # -> List nearby devices ssid. <-
            result = subprocess.run(
                ["/usr/bin/nmcli", "--fields", "ssid", "device", "wifi"],
                stdout=subprocess.PIPE,
            )

            ssids = list(set(str(result.stdout).split("\\n")[1:-1]))

            if len(ssids) == 0:
                return RenderResultListAction(
                    ExtensionResultItem(
                        icon="images/error.png",
                        name="No devices found",
                        on_enter=ExtensionCustomAction(
                            on_enter=HideWindowAction(),
                        ),
                    )
                )

            for i in range(len(ssids)):
                output.append(
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=ssids[i],
                        description="Connect",
                        on_enter=ExtensionCustomAction(
                            data={ssids[i]}, keep_app_open=True
                        ),
                    ),
                )

            return RenderResultListAction(output)

        except FileNotFoundError:

            package_not_found_error = ExtensionResultItem(
                icon="images/error.png",
                name="Error !",
                description="nmcli package not found.",
                on_enter=HideWindowAction(),
            )

            return RenderResultListAction(package_not_found_error)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):

        ssid = event.get_data().pop()
        os.system(f"bash -c '/usr/bin/nmcli dev wifi connect {ssid}'")

        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Connected to {ssid}",
                    on_enter=HideWindowAction(),
                )
            ]
        )


if __name__ == "__main__":
    WifiPicker().run()
