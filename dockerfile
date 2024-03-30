FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer
COPY ./spider /spider/
WORKDIR /spider/
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

CMD [ "python3" , "-m" , "app"]