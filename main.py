import sys
from PyQt5.QtCore import QThread, QUrl
from PyQt5.QtWidgets import QApplication, QPushButton, QComboBox, QLineEdit, QFormLayout, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from make_Video import start as make_video_start, close


class StartVideoRecording(QThread):
    path: str = ""

    def __init__(self):
        super(StartVideoRecording, self).__init__()

    def run(self):
        print('aabb,son threading in ....', self.path)
        make_video_start("", self.path)


class StopVideoRecording(QThread):
    def run(self):
        close()


class MyWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.container = QVBoxLayout()  # 外层是垂直布局
        self.resize_()
        self.main()
        self.folder = ""  # 文件保存的目录
        self.start_video = StartVideoRecording()
        self.stop_video = StopVideoRecording()

    def resize_(self):
        # self.resize(300, 200)
        self.setFixedSize(300, 200)

    @classmethod
    def create_label(cls, label_text: str) -> QLabel:
        """
        返回一个label
        :param label_text: label的字体
        :return:
        """
        return QLabel(label_text)

    @classmethod
    def create_form_lay_out(cls) -> QFormLayout:
        """返回一个表单布局"""
        return QFormLayout()

    def create_line_edit(self, label: str, layout: QVBoxLayout, placeholder: str = "",
                         echoMode: int = QLineEdit.Normal) -> QLineEdit:
        """
        创建输入框
        :param label: label内容
        :param layout:  布局
        :param placeholder: 输入框提示信息
        :param echoMode: 是否展示输入的内容 todo https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QLineEdit.html
        :return:
        """
        label = self.create_label(label)
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(placeholder)
        line_edit.setEchoMode(echoMode)
        layout.addRow(label, line_edit)
        return line_edit

    def create_button(self, btn_text: str, call_fun) -> QPushButton:
        """
        返回一个按钮
        :param btn_text: 按钮上面的文字
        :param call_fun 回调函数
        :return: QPushButton
        """

        btn = QPushButton(btn_text, self)
        btn.clicked.connect(lambda: call_fun(btn))
        return btn

    def create_q_msg(self, msg: str, title: str = '提示信息') -> None:
        """
        返回一个信息提示框
        :param msg: 提示的信息
        :param title:  标题
        :return:
        """
        QMessageBox.information(self, title, msg)

    @property
    def create_result_dir(self) -> QUrl:
        """
        选择测试案例报告目录
        :return:
        """
        return self.create_file_choice.getExistingDirectoryUrl()

    def btn_click(self, btn: QPushButton):
        """
        按钮的点击事件
        :param btn:
        :return:
        """
        if btn.text() == '选择视频保存目录':
            self.folder = self.create_result_dir.path()[1:]
        elif btn.text() == '开始录制':
            if not self.folder:
                return self.create_q_msg("请先选择视频存放目录", "提示信息")
            else:
                self.create_q_msg("开始录制", "提示信息")
            self.start_video.path = self.folder
            self.start_video.start()

        elif btn.text() == '结束录制':
            self.create_q_msg("停止录制", "提示信息")
            self.stop_video.start()

    @classmethod
    def create_q_h_box_layout(cls) -> QHBoxLayout:
        """创建一个水平布局"""
        return QHBoxLayout()

    @property
    def create_file_choice(self) -> QFileDialog:
        """
        创建文件选择器
        :return:
        """
        return QFileDialog()

    def main(self):
        form_lay_out: QFormLayout = self.create_form_lay_out()
        self.container.addLayout(form_lay_out)

        qh_box = self.create_q_h_box_layout()
        qh_box.addWidget(self.create_button("开始录制", self.btn_click))
        qh_box.addWidget(self.create_button("结束录制", self.btn_click))
        qh_box.addWidget(self.create_button("选择视频保存目录", self.btn_click))

        self.container.addLayout(qh_box)
        self.setLayout(self.container)


def main():
    app = QApplication(sys.argv)

    window = MyWindow('alex录频')
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
