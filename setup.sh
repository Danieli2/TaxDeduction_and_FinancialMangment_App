mkdir -p ~/.streamlit/
echo "\
[theme]
base='light'
primaryColor='#77c19f'
backgroundColor='#f5efef'
secondaryBackgroundColor='#d6b361'
font='monospace'
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml