# Blog

<!-- Это проект, на примере которого я изучаю Django. За его ознову взяты обучающие видео с канала Codemy.com на YouTube
(https://www.youtube.com/channel/UCFB0dxMudkws1q8w5NJEAmw).

В данный момент реализован следующий функционал:
* регистрация и аутентификация пользователей
* добавление поста/категории в блог
* редактирование и удаление поста
* поиск постов по тегу/категории/имени пользователя
* профиль с личной информацией о пользователе и его редактирование
* комментарии к постам
* возможность комментировать комментарии
* возможность подписки на блоги других пользователей
* личная лента
* списки подписчиков/подписок

Также написаны тесты для всех моделей, форм и отображений.

В планах:
* отрефакторить код (возможно, добавить тестов)
* добавить на home page что-нибудь помимо блога (TODO list etc)

Был сделан deploy на Heroku. Блог доступен по данной ссылке:
https://myawesome2021blog.herokuapp.com

В данный момент с каждым новым деплоем теряются статические файлы (изображения). 
Это связано с особенностями Heroku, а создавать свой bucket AWS S3 не готова. -->

This is the project I learn Django with. Educational videos from [Codemy.com](https://www.youtube.com/channel/UCFB0dxMudkws1q8w5NJEAmw) 
Youtube channel were used as a basis.

 Following functionality is implemented at the moment: 
* registration and authentication
* the main page with all posts 
* adding post or category to the blog
* editing and deleting post
* searching by tag/category/username
* profile 
* comments to posts and replies to comments
* ability to follow other users 
* personal feed

I also wrote tests for all views, models and forms.

TODO:
* refactor code
* add new test scenario
* add something new to home page in addition to Blog

I've done deploy to Heroku. Blog is available here: 
https://myawesome2021blog.herokuapp.com

At the moment after every new deploy static files (images) get lost. This happens due to
Heroku specificity. To prevent this an AWS S3 bucket can be used, but I'm not going to (this isn't free).
