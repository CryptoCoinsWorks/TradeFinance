import subprocess

cmd = "C:\\Users\\vince\\AppData\\Roaming\\Python\\Python39\\Scripts\\pyside2-uic.exe main_window.ui > main_window.py"
# cmd = "C:\\Users\\vince\\AppData\\Roaming\\Python\\Python39\\Scripts\\pyside2-uic.exe search.ui > search.py"
# main_window markets_widget article  indicator_settings_dialog sentimentals splashscreen order order_list_widget order_modify_widget
subprocess.run(cmd, shell=True)
