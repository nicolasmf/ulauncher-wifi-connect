import subprocess
from black import out
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class WifiPicker(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):

        output = []

        try:
            # -> List nearby devices ssid. <-
            result = subprocess.run(
                ["/usr/bin/nmcli", "--fields", "ssid", "device", "wifi"],
                stdout=subprocess.PIPE,
            )

            ssids = set(str(result.stdout).split("\\n")[1:-1])

            for i in range(len(ssids)):
                output.append(
                    ExtensionResultItem(
                        icon="images/error.png",
                        name=ssids[i],
                        description="nmcli package not found.",
                        on_enter=HideWindowAction(),
                    )
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


if __name__ == "__main__":
    WifiPicker().run()
