## link_shortener app by Django Framework( with nginx and postgres)
-run project by this command: docker-compose up or docker-compose up -d\
-create superuser by this command :docker container exec -it (container name) -c "python manage.py createsuperuser"\
-run app in browser by this address: localhost:8008\
-create staffusers by register in register api
>*Notice:*\
for making a short link you should be logedin\
only superusers can see the analysis api\
each staff user can see her statics in the statics api
