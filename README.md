Run the commands below to start server on website with https

choco install mkcert -y  

mkcert -install   

mkcert localhost 127.0.0.1 ::1         

streamlit run agentX.py --server.port 8501 --server.sslCertFile localhost+2.pem --server.sslKeyFile localhost+2-key.pem