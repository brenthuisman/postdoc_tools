from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

class BSlider(QWidget):
	def __init__(self, title, minval, maxval, slot=None, defval=0, orientation=Qt.Horizontal, parent=None):
		super().__init__(parent)

		self.value = defval

		self.slider = QSlider(orientation,self)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setValue(defval)
		self.slider.valueChanged[int].connect(self.changeValue)
		if slot != None:
			self.slider.valueChanged[int].connect(slot)

		self.title = QLabel(title,self)

		if isinstance(minval, str):
			# assume this is a switch with just two values.
			self.slider.setMinimum(0)
			self.slider.setMaximum(1)
			t = QHBoxLayout()
			t.setContentsMargins(0, 0, 0, 0)
			t.addWidget(QLabel(minval,self))
			t.addStretch(1)
			t.addWidget(QLabel(maxval,self))
		else:
			self.slider.setMinimum(minval)
			self.slider.setMaximum(maxval)
			self.vallabel = QLabel(str(defval),self)
			self.vallabel.setAlignment(Qt.AlignCenter)

		l = QVBoxLayout()
		l.setContentsMargins(0, 0, 0, 0)
		l.addWidget(self.title)
		l.addWidget(self.slider)
		if isinstance(minval, str):
			l.addLayout(t)
		else:
			l.addWidget(self.vallabel)

		self.setLayout(l)

	def changeValue(self,v):
		self.value = v
		# print(self.title.text(),v)
		try:
			self.vallabel.setText(str(v))
		except:
			pass

