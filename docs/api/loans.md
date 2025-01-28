# Loans  
Supports managing book loans, including creating, viewing, and deleting loan records.

## Create a new loan  

**Request**:  

`POST` `/loans/`  

Parameters:

Name         | Type      | Required | Description  
-------------|-----------|----------|-------------  
user         | integer      | Yes      | The UUID of the user borrowing the book.  
book         | integer   | Yes      | The ID of the book being borrowed.  

*Note:*  

- **[Authorization Protected](authentication.md)** for Admin users  

**Response**:  

```json
Content-Type application/json  
201 Created  

{
  "id": 1,
  "user": 1,
  "book": 5,
  "borrowed_at": "2025-01-28T09:04:37.765816Z",
  "returned_at": null
}
```  

Here’s an updated section of your API documentation for the `Loan` resource, including details about the list endpoint with pagination:  

---

## List all loans  

**Request:**  
`GET` `/loans/`  

### Parameters:  

| Name     | Type   | Required | Description                  |
|----------|--------|----------|------------------------------|
| page     | int    | No       | The page number to retrieve. |
| page_size| int    | No       | Number of records per page.  |  

*Note:*  
- **[Authorization Protected]**: Admin users only.  
- Default pagination values are set by the system.  

**Response:**  
```json
Content-Type: application/json  
200 OK  

{
  "count": 3,
  "next": "http://api.example.com/loans/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "borrowed_at": "2025-01-01T14:30:00Z",
      "returned_at": null,
      "user": {
        "id": "c9123e67-5f83-4be9-8c18-6d27aa40c122",
        "username": "john_doe"
      },
      "book": {
        "id": "f84e8e91-1c36-4e25-8099-5b7aa02c9e9f",
        "title": "The Great Gatsby"
      }
    }
  ]
}
```

### Notes:  
- Pagination links (`next`, `previous`) may be `null` if there are no additional pages.  
- Default `page_size` is 10 but can be adjusted by providing the `page_size` parameter.  


---

## Retrieve a loan  

**Request**:  

`GET` `/loans/:id`  

*Note:*  

- **[Authorization Protected](authentication.md)** for Admin users  

**Response**:  

```json
Content-Type application/json  
200 OK  

{
  "id": 1,
  "user": 1,
  "book": 5,
  "borrowed_at": "2025-01-28T09:04:37.765816Z",
  "returned_at": null
}
```

---

## Delete a loan  

**Request**:  

`DELETE` `/loans/:id`  

*Note:*  

- **[Authorization Protected](authentication.md)** for Admin users  

**Response**:  

```json
Content-Type application/json  
204 No Content
```