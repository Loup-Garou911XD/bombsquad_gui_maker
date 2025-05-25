# ba_meta require api 9
import babase
import bauiv1 as bui
import bascenev1 as bs

"""GUI Maker plugin by LoupGarou
This plugin allows you to create a GUI using buttons and labels."""


def Print(*args):
    out = ""
    for arg in args:
        a = str(arg)
        out += a
    bui.screenmessage(out)


def cprint(*args):
    out = ""
    for arg in args:
        a = str(arg)
        out += a
    bs.chatmessage(out)


class SettingWindow(bui.Window):
    def __init__(self):
        self._widgets = []
        self._layout = []
        self.width, self.height = babase.get_virtual_screen_size()
        self.buffer_y = 10
        self.buffer_x = 20
        self.btn_size = [120, 40]
        self.control_panel_size = [150, self.height - (self.buffer_y + 10)]

        self.draw_ui()

    def draw_ui(self):
        self.uiscale = bui.app.ui_v1.uiscale

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self.width, self.height),
                background=False,
                on_outside_click_call=self._close,
                transition="in_right",
            )
        )
        self.builder_panel = bui.containerwidget(
            parent=self._root_widget,
            size=(self.width - self.control_panel_size[0], self.height),
            position=(0, 0),
        )
        self.control_panel = bui.containerwidget(
            parent=self._root_widget,
            size=(self.control_panel_size[0], self.control_panel_size[1]),
            position=(self.width - self.control_panel_size[0], 0),
            color=(0.5, 0.5, 0.5),
            transition="in_right",
        )
        pos_y = self.control_panel_size[1] - self.btn_size[1] - self.buffer_y

        bui.buttonwidget(
            parent=self.control_panel,
            label='Add Button',
            position=(self.buffer_x, pos_y),
            size=(self.btn_size[0], self.btn_size[1]),
            on_activate_call=self._add_button,
        )
        pos_y -= self.buffer_y + self.btn_size[1]
        bui.buttonwidget(
            parent=self.control_panel,
            label='Add Label',
            position=(self.buffer_x, pos_y),
            size=(self.btn_size[0], self.btn_size[1]),
            on_activate_call=self._add_label,
        )
        pos_y -= self.buffer_y + self.btn_size[1]
        bui.buttonwidget(
            parent=self.control_panel,
            label='Export Code',
            position=(self.buffer_x, pos_y),
            size=(self.btn_size[0], self.btn_size[1]),
            on_activate_call=self._export_code,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            label='Close',
            position=(0, self.height - self.btn_size[1]),
            size=(self.btn_size[0], self.btn_size[1]),
            on_activate_call=self._close,
        )

    def _add_button(self):
        y = 260 - len(self._layout) * 50
        data = {'type': 'button', 'label': 'Button', 'position': (40, y), 'size': (200, 40)}
        btn = bui.buttonwidget(
            parent=self.builder_panel,
            label=data['label'],
            position=data['position'],
            size=data['size'],
            on_activate_call=lambda: self._edit_button_attributes(btn, data),
        )
        self._layout.append(data)
        self._widgets.append(btn)

    def _edit_button_attributes(self, btn_widget, data):
        AttributeEditorWindow(self, btn_widget, data)

    def _add_label(self):
        y = 260 - len(self._layout) * 50
        lbl = bui.textwidget(
            parent=self.builder_panel,
            text='Label',
            position=(300, y),
            size=(0, 0),
            scale=1.0,
            color=(1, 1, 1),
        )
        self._layout.append(
            {'type': 'label', 'text': 'Label', 'position': (300, y), 'size': (0, 0)}
        )
        self._widgets.append(lbl)

    def _export_code(self):
        code = "import bauiv1 as bui\n\n"
        code += "def create_window():\n"
        code += "    root = bui.containerwidget(size=(600, 400))\n"
        for w in self._layout:
            if w['type'] == 'button':
                code += (
                    "    bui.buttonwidget(parent=root, label={!r}, position={}, size={})\n".format(
                        w['label'], w['position'], w['size']
                    )
                )
            elif w['type'] == 'label':
                code += "    bui.textwidget(parent=root, text={!r}, position={}, size=(0, 0), scale=1.0, color=(1,1,1))\n".format(
                    w['text'], w['position']
                )
        code += "    return root\n"
        bui.clipboard_set_text(code)
        bui.screenmessage('Exported code copied to clipboard!', color=(0, 1, 0))

    def _close(self):
        bui.containerwidget(
            edit=self._root_widget,
            transition="out_right",
        )


class AttributeEditorWindow(bui.Window):
    def __init__(self, parent_window, btn_widget, data):
        self._parent_window = parent_window
        self._btn_widget = btn_widget
        self._data = data
        self.width = 320
        self.height = 240
        super().__init__(
            root_widget=bui.containerwidget(size=(self.width, self.height), transition='in_scale')
        )
        bui.textwidget(
            parent=self._root_widget,
            position=(self.width * 0.5, self.height - 40),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='Edit Button Attributes',
            scale=1.0,
            color=(1, 1, 1),
        )
        # Label
        bui.textwidget(
            parent=self._root_widget,
            position=(30, self.height - 80),
            size=(0, 0),
            text='Label:',
            scale=0.8,
            color=(1, 1, 1),
            h_align='left',
        )
        self._label_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            position=(100, self.height - 85),
            size=(180, 40),
            text=self._data['label'],
            v_align='center',
            h_align='left',
            color=(1, 1, 1),
            maxwidth=180,
        )
        # X Position
        bui.textwidget(
            parent=self._root_widget,
            position=(30, self.height - 120),
            size=(0, 0),
            text='X:',
            scale=0.8,
            color=(1, 1, 1),
            h_align='left',
        )
        self._x_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            position=(100, self.height - 125),
            size=(60, 40),
            text=str(self._data['position'][0]),
            v_align='center',
            h_align='left',
            color=(1, 1, 1),
            maxwidth=60,
        )
        # Y Position
        bui.textwidget(
            parent=self._root_widget,
            position=(170, self.height - 120),
            size=(0, 0),
            text='Y:',
            scale=0.8,
            color=(1, 1, 1),
            h_align='left',
        )
        self._y_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            position=(200, self.height - 125),
            size=(60, 40),
            text=str(self._data['position'][1]),
            v_align='center',
            h_align='left',
            color=(1, 1, 1),
            maxwidth=60,
        )
        # Save button
        bui.buttonwidget(
            parent=self._root_widget,
            label='Save',
            position=(self.width * 0.5 - 60, 30),
            size=(120, 40),
            on_activate_call=self._save,
        )
        # Cancel button
        bui.buttonwidget(
            parent=self._root_widget,
            label='Cancel',
            position=(self.width * 0.5 - 60, 80),
            size=(120, 40),
            on_activate_call=self._close,
        )

    def _save(self):
        # Get updated values
        label = bui.textwidget(query=self._label_field)
        try:
            x = int(bui.textwidget(query=self._x_field))
            y = int(bui.textwidget(query=self._y_field))
        except Exception:
            bui.screenmessage('Invalid position values!', color=(1, 0, 0))
            return
        # Update data
        self._data['label'] = label
        self._data['position'] = (x, y)
        # Update the button widget
        bui.buttonwidget(edit=self._btn_widget, label=label, position=(x, y))
        self._close()

    def _close(self):
        bui.containerwidget(edit=self._root_widget, transition='out_scale')


# ba_meta export plugin
class Loup(babase.Plugin):
    def __init__(self):
        pass

    def on_app_running(self):
        # SettingWindow()
        pass

    def show_settings_ui(self, source_widget):
        SettingWindow()

    def has_settings_ui(self):
        return True
