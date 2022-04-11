import io
import requests
import pandas as pd
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QTableWidgetItem

from window import Ui_MainWindow
import pyodbc


class UI(Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # target url taken from sharepoint and credentials
        url = r'https://anvisabr.sharepoint.com/:x:/s/InformativoGGTPS/ETabGa6_9jpCvVO5vhgkOk8BmYNJlfZ8nIq2TDPisSlEvQ?download=1'

        response = requests.get(url)

        # save data to BytesIO stream
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)  # set file object to start

        # read excel file and each sheet into pandas dataframe
        self.df = pd.read_excel(bytes_file_obj, sheet_name='Planilha1')
        self.consulta = pd.DataFrame()

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        self.comboBox_Gerencia.activated.connect(self.combobox_Updated)
        self.comboBox_Primaria.activated.connect(self.combobox_Updated)
        self.comboBox_Peticao.activated.connect(self.combobox_Updated)
        self.comboBox_CO_Assunto.activated.connect(self.combobox_Updated)
        self.comboBox_DS_Assunto.activated.connect(self.combobox_Updated)

        self.checkBox_Gerencia.toggled.connect(self.checkBox_Selected)
        self.checkBox_Primaria.toggled.connect(self.checkBox_Selected)
        self.checkBox_Peticao.toggled.connect(self.checkBox_Selected)
        self.checkBox_CO_Assunto.toggled.connect(self.checkBox_Selected)
        self.checkBox_DS_Assunto.toggled.connect(self.checkBox_Selected)
        self.checkBox_Entrada.toggled.connect(self.checkBox_Selected)

        self.pushButton_Limpar.clicked.connect(self.clear_Form)
        self.pushButton_Gerar.clicked.connect(self.fill_Table)
        self.pushButton_Salvar.clicked.connect(self.export_Table)

        self.dateEdit_EntradaFim.setDate(QDate.currentDate())

        self.checkBox_Selected()
        self.combobox_Updated()

    def clear_Form(self):
        self.comboBox_Gerencia.clear()
        self.comboBox_Primaria.clear()
        self.comboBox_Peticao.clear()
        self.comboBox_CO_Assunto.clear()
        self.comboBox_DS_Assunto.clear()

        self.comboBox_Gerencia.addItems(self.df['GERÊNCIA'].unique())
        self.comboBox_Primaria.addItems(self.df['TIPO PETIÇÃO'].unique())
        self.comboBox_Peticao.addItems(self.df['PETIÇÃO'].unique())
        self.comboBox_CO_Assunto.addItems(self.df['CO_ASSUNTO'].unique().astype('str'))
        self.comboBox_DS_Assunto.addItems(self.df['DS_ASSUNTO'].unique())

        self.checkBox_Gerencia.setChecked(False)
        self.checkBox_Primaria.setChecked(False)
        self.checkBox_Peticao.setChecked(False)
        self.checkBox_CO_Assunto.setChecked(False)
        self.checkBox_DS_Assunto.setChecked(False)
        self.checkBox_Entrada.setChecked(False)

        self.comboBox_Gerencia.setEnabled(False)
        self.comboBox_Primaria.setEnabled(False)
        self.comboBox_Peticao.setEnabled(False)
        self.comboBox_CO_Assunto.setEnabled(False)
        self.comboBox_DS_Assunto.setEnabled(False)

        self.dateEdit_EntradaInicio.setEnabled(False)
        self.dateEdit_EntradaFim.setEnabled(False)

        self.progressBar_Gerar.setEnabled(False)
        self.progressBar_Gerar.setValue(0)
        self.progressBar_Salvar.setEnabled(False)
        self.progressBar_Salvar.setValue(0)


    def combobox_Updated(self):

        assuntos_selecionados = self.df
        gerenciaSelecionada = None
        primariaSelecionada = None
        peticaoSelecionada = None
        coAssuntoSelecionado = None
        dsAssuntoSelecionado = None

        if self.comboBox_Gerencia.isEnabled():
            gerenciaSelecionada = self.comboBox_Gerencia.currentText()
            assuntos_selecionados = assuntos_selecionados[assuntos_selecionados['GERÊNCIA'] == gerenciaSelecionada]
        if self.comboBox_Primaria.isEnabled():
            primariaSelecionada = self.comboBox_Primaria.currentText()
            assuntos_selecionados = assuntos_selecionados[assuntos_selecionados['TIPO PETIÇÃO'] == primariaSelecionada]
        if self.comboBox_Peticao.isEnabled():
            peticaoSelecionada = self.comboBox_Peticao.currentText()
            assuntos_selecionados = assuntos_selecionados[assuntos_selecionados['PETIÇÃO'] == peticaoSelecionada]
        if self.comboBox_CO_Assunto.isEnabled():
            coAssuntoSelecionado = self.comboBox_CO_Assunto.currentText()
            assuntos_selecionados = assuntos_selecionados[assuntos_selecionados['CO_ASSUNTO'] == int(coAssuntoSelecionado)]
        if self.comboBox_DS_Assunto.isEnabled():
            dsAssuntoSelecionado = self.comboBox_DS_Assunto.currentText()
            assuntos_selecionados = assuntos_selecionados[assuntos_selecionados['DS_ASSUNTO'] == dsAssuntoSelecionado]

        self.comboBox_Gerencia.clear()
        self.comboBox_Primaria.clear()
        self.comboBox_Peticao.clear()
        self.comboBox_CO_Assunto.clear()
        self.comboBox_DS_Assunto.clear()

        self.comboBox_Gerencia.addItems(assuntos_selecionados['GERÊNCIA'].unique())
        self.comboBox_Primaria.addItems(assuntos_selecionados['TIPO PETIÇÃO'].unique())
        self.comboBox_Peticao.addItems(assuntos_selecionados['PETIÇÃO'].unique())
        self.comboBox_CO_Assunto.addItems(assuntos_selecionados['CO_ASSUNTO'].unique().astype('str'))
        self.comboBox_DS_Assunto.addItems(assuntos_selecionados['DS_ASSUNTO'].unique())

        if gerenciaSelecionada is not None:
            self.comboBox_Gerencia.setCurrentText(gerenciaSelecionada)
        if primariaSelecionada is not None:
            self.comboBox_Primaria.setCurrentText(primariaSelecionada)
        if peticaoSelecionada is not None:
            self.comboBox_Peticao.setCurrentText(peticaoSelecionada)
        if coAssuntoSelecionado is not None:
            self.comboBox_CO_Assunto.setCurrentText(coAssuntoSelecionado)
        if dsAssuntoSelecionado is not None:
            self.comboBox_DS_Assunto.setCurrentText(dsAssuntoSelecionado)

    def checkBox_Selected(self):
        if self.checkBox_Gerencia.isChecked():
            self.comboBox_Gerencia.setEnabled(True)
        else:
            self.comboBox_Gerencia.setEnabled(False)

        if self.checkBox_Primaria.isChecked():
            self.comboBox_Primaria.setEnabled(True)
        else:
            self.comboBox_Primaria.setEnabled(False)

        if self.checkBox_Peticao.isChecked():
            self.comboBox_Peticao.setEnabled(True)
        else:
            self.comboBox_Peticao.setEnabled(False)

        if self.checkBox_CO_Assunto.isChecked():
            self.comboBox_CO_Assunto.setEnabled(True)
        else:
            self.comboBox_CO_Assunto.setEnabled(False)

        if self.checkBox_DS_Assunto.isChecked():
            self.comboBox_DS_Assunto.setEnabled(True)
        else:
            self.comboBox_DS_Assunto.setEnabled(False)

        if self.checkBox_Entrada.isChecked():
            self.dateEdit_EntradaInicio.setEnabled(True)
            self.dateEdit_EntradaFim.setEnabled(True)
        else:
            self.dateEdit_EntradaInicio.setEnabled(False)
            self.dateEdit_EntradaFim.setEnabled(False)

        if self.tableResultado.rowCount() == 0:
            self.pushButton_Salvar.setEnabled(False)

    def fill_Table(self):

        self.progressBar_Gerar.setEnabled(True)
        self.progressBar_Gerar.setValue(10)

        SERVER_NAME = 'anvssdf522'
        DATABASE_NAME = 'BI_PRODUTOSAUDE'

        conn = pyodbc.connect(
            r'DRIVER={SQL Server};'
            r'SERVER=anvssdf522;'
            r'DATABASE=BI_PRODUTOSAUDE;'
            r'UID=helio.filho;'
            r'PWD=@H3L10MAc;')

        assuntos_selecionados = self.df

        assuntos_selecionados = (
            assuntos_selecionados[assuntos_selecionados[
                                      'GERÊNCIA'] == self.comboBox_Gerencia.currentText()] if self.comboBox_Gerencia.isEnabled() else assuntos_selecionados)

        assuntos_selecionados = (
            assuntos_selecionados[assuntos_selecionados[
                                      'TIPO PETIÇÃO'] == self.comboBox_Primaria.currentText()] if self.comboBox_Primaria.isEnabled() else assuntos_selecionados)
        assuntos_selecionados = (
            assuntos_selecionados[assuntos_selecionados[
                                      'PETIÇÃO'] == self.comboBox_Peticao.currentText()] if self.comboBox_Peticao.isEnabled() else assuntos_selecionados)

        assuntos_selecionados = (
            assuntos_selecionados[assuntos_selecionados[
                                      'CO_ASSUNTO'] == int(
                self.comboBox_CO_Assunto.currentText())] if self.comboBox_CO_Assunto.isEnabled() else assuntos_selecionados)
        assuntos_selecionados = (
            assuntos_selecionados[assuntos_selecionados[
                                      'DS_ASSUNTO'] == self.comboBox_DS_Assunto.currentText()] if self.comboBox_DS_Assunto.isEnabled() else assuntos_selecionados)

        assuntos = '(' + ','.join([str(i) for i in assuntos_selecionados['CO_ASSUNTO'].to_list()]) + ')'

        sql = f'select * from ta_pps_protocolo where co_assunto in {assuntos}'
        sql = sql + f' and dt_entrada >= convert(datetime, \'{self.dateEdit_EntradaInicio.date().toString("yyyy-MM-dd")}\') and dt_entrada <= convert(datetime,\'{self.dateEdit_EntradaFim.date().toString("yyyy-MM-dd")}\')' if self.checkBox_Entrada.isChecked() else sql

        self.consulta = pd.read_sql(sql, conn).applymap(lambda x: x.encode('unicode_escape').
                                                        decode('utf-8') if isinstance(x, str) else x)

        self.progressBar_Gerar.setValue(20)

        nRows = len(self.consulta.index)
        nColumns = len(self.consulta.columns)
        self.tableResultado.setRowCount(nRows)
        self.tableResultado.setColumnCount(nColumns)
        self.tableResultado.setHorizontalHeaderLabels(self.consulta.columns)
        for i in range(self.tableResultado.rowCount()):
            self.progressBar_Gerar.setValue(20 + (80 * i) // self.tableResultado.rowCount())
            for j in range(self.tableResultado.columnCount()):
                x = self.consulta.iloc[i, j]
                self.tableResultado.setItem(i, j, QTableWidgetItem(str(x)))
        self.pushButton_Salvar.setEnabled(True)

        self.progressBar_Gerar.setValue(100)

    def export_Table(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.tableResultado, 'Salvar arquivo', '',
                                                            'Arquivo Excel (*.xlsx)')
        self.progressBar_Salvar.setEnabled(True)
        self.progressBar_Salvar.setValue(50)
        self.consulta.to_excel(filename, index=False, encoding='utf-8', sheet_name='Planilha1')
        self.progressBar_Salvar.setValue(100)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
