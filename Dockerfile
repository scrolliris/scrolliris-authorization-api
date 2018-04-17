FROM gentoo/portage:20180410 as portage
FROM gentoo/stage3-amd64-nomultilib:20180410

COPY --from=portage /usr/portage /usr/portage

# venv
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
ADD constraints.txt /app/constraints.txt
ADD . app/

WORKDIR app/

# python
RUN set -eux; \
    \
    eselect news read --quiet new >/dev/null 2>&1; \
    emerge -qv =dev-lang/python-3.5.5;
    \
    virtualenv /env -p python3.5

ENV ENV production
ENV WSGI_URL_SCHEME http
ENV HOST 0.0.0.0
ENV PORT 8080

RUN make setup

EXPOSE 8080

CMD make start
