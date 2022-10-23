mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"a.n.filanovich@urfu.ru\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
