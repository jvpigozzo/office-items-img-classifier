# Fast API - Office Items Image Classifier
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

This project is an API built using **Python, FastAPI, MongDB as the database.** The API was developed to solve office items image classification and management.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Contributing](#contributing)

## Installation

#### 1. Clone the repository:

```bash
git clone https://github.com/jvpigozzo/office-items-img-classifier.git
```

### Usage

#### 2. Building and running the application with docker:

When you're ready, start your application by running:


```bash
docker compose up --build
```

Your application will be available at http://localhost:80.

## API Endpoints

#### 3. The API provides the following endpoints:

**GET USERS**
```markdown
GET /users - Retrieve a list of all users.
```
```json
[
  {
    "name": "João Vitor Pigozzo",
    "email": "jvpigozzo@gmail.com",
    "nickname": "jvpigozzo",
    "id": "66492f93e509e0279f9dafd0"
  }
]
```

**POST USERS**
```markdown
POST /users - Register a new user into the App
```
```json
{
    "name": "João Vitor Pigozzo",
    "email": "jvpigozzo@gmail.com",
    "nickname": "jvpigozzo"
}
```

**GET ITEMS**
```markdown
GET /users - Retrieve a list of all items.
```
```json
[
  {
    "name": "pen1",
    "label_id": "2",
    "image_url": "/vol/media/img_20231102_132236.jpg",
    "is_validated": false,
    "id": "6648acc879284bb3f952ff98"
  }
]
```

**POST ITEMS**
```markdown
POST /items - Register a new item into the App
```
```json
{
  "name": "pencil1",
  "label_id": "1",
  "is_validated": true
}
```

**POST ITEMS IMAGE**
```markdown
POST /items/image-upload/{item_id} - Upload image file
```
- `item_id` : The unique identifier of the item.
- `image` (form-data): The image file to be uploaded.

**POST ITEMS RECOGNIZE**
```markdown
POST /items/recognize/{item_id} - Recognize image with chosen model
```
```json
{
  "item_id": "6648acc879284bb3f952ff98",
  "prompt_template": "What's in the image?",
  "model_name": "gpt-4-turbo"
}
```

## Database
The project utilizes [MongoDB](https://www.mongodb.com/docs/) as the database.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request to the repository.
