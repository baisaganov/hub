FROM python:3.12.0a4-alpine3.17
WORKDIR /usr/workspace

#Install playwright
RUN pip install playwright==@1.50.0 && \
    playwright install --with-deps


# Install reqs
RUN pip3 install -r requirements.txt





#WORKDIR /app
#
#COPY requirements.txt .
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#FROM mcr.microsoft.com/playwright:v1.45.2-jammy
#
#WORKDIR /app
#
#COPY --from=builder /usr/local/lib/python3.12/site-packages \
#                    /usr/local/lib/python3.12/site-packages
#
#COPY . .
#
#RUN mkdir -p allure-results traces screenshots logs
#
#ENTRYPOINT ["pytest"]
#CMD ["tests/", "-v", "--alluredir=allure-results", "--clean-alluredir"]
