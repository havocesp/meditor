cls

pushd ..

rmdir build /s /q
rmdir dist\meditor /s /q

pyinstaller --clean --noconfirm --noconsole --name meditor --icon "meditor\data\meditor-text-editor.ico" --add-data "meditor\data;data" --hidden-import PyQt5.sip run.py

popd
