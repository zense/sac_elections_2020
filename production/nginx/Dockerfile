FROM nginx:latest

# remove the default nginx config file
RUN rm /etc/nginx/conf.d/default.conf

WORKDIR .

# copy config file to config directory (apparently it is  conf.d and not config.d)
COPY sac_elections.conf /etc/nginx/conf.d/sac_elections.conf