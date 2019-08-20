# Szukajka movie link scrapper

The script sends a query to [Szukajka.tv](https://lmgtfy.com/?q=szukajka.tv) and parses the website.

## install chromedriver for selenium
```
wget https://chromedriver.storage.googleapis.com/77.0.3865.10/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d .
sudo mv ./chromedriver /usr/local/share/
sudo ln -sf /usr/local/share/chromedriver /usr/local/bin
```

## requirements
```
requests==2.22.0
selenium==3.141.0
bs4==0.0.1
tqdm==4.33.0
```

## how to use
```
python main.py
    --title <TITLE> (required)
    --source <SOURCE> (optional: 'all', 'gounlimited', 'openload', 'streamango', 'streamcherry', 'verystream', 'vidoza')
    --version <VERSION> (optional: 'all', 'dub', 'org', 'sub')
    -d (optional flag to automatically download from link)
```
