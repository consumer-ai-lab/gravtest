# WCL Test Application: Windows Application

This contains required documentation for windows application created using `Python Tkinter`.

## Running the application

1. Make `venv` environment

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Run
```bash
python main.py
```

## Making of `.exe`

1. Install pyInstaller
```python
pip install -U pyinstaller
```

2. Create `installer` folder
```python
pyinstaller main.py --name="wcl-app" --add-data '.env;.' --add-data 'data;data'
```

### Explanation of flags

`-F`: Make a single `.exe` file rather than folder <br>
`--name=`: Application name <br>
`--add-data`: Add additional file/folder to the `.exe` destination,<br>
format `<source>;<destination>` <br>
example: `.env;.`
