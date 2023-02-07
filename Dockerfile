FROM python:3-alpine
LABEL org.opencontainers.image.source github.com/afterglow/mktxp
WORKDIR /mktxp
COPY . .
RUN pip install ./ && apk add nano
EXPOSE 49090
RUN addgroup -S mktxp && adduser -S mktxp -G mktxp
USER mktxp
ENTRYPOINT ["/usr/local/bin/mktxp"]
CMD ["export"]
