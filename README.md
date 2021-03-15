# Blog

![Build Status](https://github.com/AnnaStepakova/Blog/actions/workflows/ci.yml/badge.svg?branch=github-ci)

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

I've done two deployments to Heroku. 
Blog, deployed with Docker is available here:
https://myblog2021deploywithdocker.herokuapp.com

Deploy without Docker:
https://myawesome2021blog.herokuapp.com

At the moment after every new deploy static files (images) get lost. This happens due to
Heroku specificity. To prevent this an AWS S3 bucket can be used, but I'm not going to (this isn't free).
