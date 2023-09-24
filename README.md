# Recipe App API
The Recipe App API is a pet project designed to provide hands-on experience with various technologies including Django, Django REST Framework, and Docker in conjunction with Docker Compose.
## Features

- A User API that includes user registration, token creation, and user management.
- A Recipe API where you can manage recipes, tags, and ingredients. Each recipe can be associated with multiple tags and multiple ingredients.
- Image upload capability for recipes.
- Search and filtering functionality in the Recipe API, so you can retrieve recipes containing certain ingredients or tags.
- Token-based Authentication and permissions.

## Technologies Used

- Django
- Django Rest Framework 
- Docker
- Docker Compose
- PostgreSQL
- Nginx 

## How to Build and Run

1. Make sure Docker and Docker Compose are installed on your machine.
2. Clone this repository and navigate into the root directory of this project.
3. Rename the file `.env.sample` to `.env`.
4. Access the `.env` file and adjust the variables as needed based on your environment. It's also possible to use the default values in the .env file. These defaults are designed to ensure the application operates correctly for quick testing or development setups.
5. Execute the following commands to build and run the application:

For running on localhost:
```bash
docker-compose up
````
For running in a production setup:

```bash
docker-compose -f docker-compose-deploy.yml up
```

# API

## User API

- `POST /api/users/`: Create a new user
- `POST /api/users/token/`: Create a new token for the user
- `GET, PUT, PATCH /api/users/me/`: Retrieve and update the authenticated user

## Recipe API

- `GET, POST /api/recipes/recipes/`: Retrieve all recipes, or create a new recipe
- `GET, PUT, PATCH, DELETE /api/recipes/recipes/{id}/`: Retrieve, update, partial update or delete a recipe
- `POST /api/recipes/recipes/{id}/upload-image/`: Upload an image to a recipe
- `GET, POST /api/recipes/tags/`: Retrieve all tags, or create a new tag
- `GET, PUT, PATCH, DELETE /api/recipes/tags/{id}/`: Retrieve, update, partial update, or delete a tag
- `GET, POST /api/recipes/ingredients/`: Retrieve all ingredients, or create a new ingredient
- `GET, PUT, PATCH, DELETE /api/recipes/ingredients/{id}/`: Retrieve, update, partial update, or delete an ingredient