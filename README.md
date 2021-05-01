# sushi
Sushoshop franchazy web app


для nginx:

location /ws/chat/ {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_redirect off;
      proxy_buffering off;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_pass http://0.0.0.0:8080; # или на каком порту запущен будет aiochat.py


}
запустить aiobot.py  в той же среде что и Django,
добавить к модели пользователя поле с аватаром(если его нет)
