FROM python:3.8
WORKDIR "${HOME}"
COPY ["happy.h5", "mask_model.h5", "gender_model.h5", "main.py","haarcascade_frontalface_default.xml", "requirements.txt" ,"./"]
RUN pip install -r requirements.txt --no-cache-dir
RUN pip uninstall  keras --yes

EXPOSE 8501
#CMD [ 'streamlit run --server.port --device="//dev/video0:/dev/video0" $PORT main.py']
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
#CMD [ 'streamlit run --server.port --device="//dev/video0:/dev/video0" $PORT main.py']
##CMD [ "streamlit run main.py"]
#ENTRYPOINT ["streamlit", "run"]
#CMD ["main.py"]
##CMD [ "streamlit run main.py"]