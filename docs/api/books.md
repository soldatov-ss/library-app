# Books
Supports viewing, creating, and updating books.

## Get a list of books

**Request**:

`GET` `/books/`

**Response**:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "page_count": 180,
        "availability": true
    }
  ]
}
```

## Create a new book

**Request**:

`POST` `/books/`

**Response**:

```json
{
  "id": 2,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "page_count": 180,
  "availability": true
}
```

## Update a book

**Request**:

`PUT` `/books/:id`

**Response**:

```json
{
  "id": 2,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "page_count": 180,
  "availability": false
}
```

## Delete a book

**Request**:

`DELETE` `/books/:id`

**Response**:

Empty response with status code `204 No Content`.

## Get a book by ID

**Request**:

`GET` `/books/:id`

**Response**:

```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "page_count": 180,
  "availability": true
}
```

## Borrow a book

**Request**:

`POST` `/books/:id/borrow/`

**Response**:

```json
{
    "id": 1,
    "borrowed_at": "2021-01-01",
    "returned_at": null,
    "book_id": 1,
    "user_id": 1
}
```

## Return a book

**Request**:

`PUT` `/books/:id/return/`

**Response**:

```json
{
    "id": 1,
    "borrowed_at": "2021-01-01",
    "returned_at": "2021-01-02",
    "book_id": 1,
    "user_id": 1
}
```
