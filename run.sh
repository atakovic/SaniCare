#!/bin/bash

# Stelle sicher, dass pyenv initialisiert ist
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Setze pyenv-Version (optional, falls du mehrere hast)
pyenv shell 3.10.6

# Starte Streamlit-App
streamlit run /home/alen/PycharmProjects/PythonProject/streamlit/Login.py
