Start the web interface for Ragents

streamlit run main.py --browser.serverAddress=localhost

but this should REALLY be set up in /.streamlit/config.toml

Long Form:
streamlit run main.py --logger.level=debug --server.maxUploadSize=200 --server.address=localhost --server.port=8501 --browser.serverAddress=localhost --browser.serverPort=8501 --browser.gatherUsageStats=false