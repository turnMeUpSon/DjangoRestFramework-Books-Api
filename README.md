# Books API

  

I have created the books REST api service that let users:

- Get information about books (id, name, price, discount, price with discount, author, likes count, in bookmarks count, mark, max rating of book, min rating of book, owner name, readers of book)

- Search and filter books

- Create, update, delete, like and rate books
- Authorization with GitHub

  

## Getting Started

  

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

  

### Prerequisites

  

You need to have docker desktop is installed on your computer

  
### Installing

1. Open your Docker Desktop 
2.  ```git clone https://github.com/turnMeUpSon/django-books-api.git```
3. ```docker-compose build```
4. ```docker-compose up```
5. Example of response:  ```[  {  "id":  1,  "name":  "Perfume",  "price":  "15.00",  "discount":  "15.00",  "discounted_price":  "12.75",  "author":  "Patrick Suskind",  "annotated_likes":  3,  "annotated_in_bookmarks_count":  1,  "mark":  "2.75",  "max_rating":  "4.00",  "min_rating":  "1.00",  "owner_name":  "user1",  "readers":  [  {  "first_name":  "Jack",  "last_name":  "Grealish"  },  {  "first_name":  "Ian",  "last_name":  "Miller"  },  {  "first_name":  "Fabio",  "last_name":  "Tavares"  },  {  "first_name":  "Blanco",  "last_name":  "Leopard"  }  ]  },  {  "id":  2,  "name":  "The Collector",  "price":  "1000.00",  "discount":  "0.00",  "discounted_price":  "1000.00",  "author":  "John Fowles",  "annotated_likes":  3,  "annotated_in_bookmarks_count":  2,  "mark":  "4.00",  "max_rating":  "5.00",  "min_rating":  "3.00",  "owner_name":  "turnMeUpSon",  "readers":  [  {  "first_name":  "Jack",  "last_name":  "Grealish"  },  {  "first_name":  "Ian",  "last_name":  "Miller"  },  {  "first_name":  "Fabio",  "last_name":  "Tavares"  },  {  "first_name":  "Blanco",  "last_name":  "Leopard"  }  ]  },  {  "id":  3,  "name":  "The Alchemist",  "price":  "30.00",  "discount":  "0.00",  "discounted_price":  "30.00",  "author":  "Paulo Coelho",  "annotated_likes":  0,  "annotated_in_bookmarks_count":  0,  "mark":  null,  "max_rating":  null,  "min_rating":  null,  "owner_name":  null,  "readers":  []  },  {  "id":  4,  "name":  "Programming in Python 3",  "price":  "150.00",  "discount":  "0.00",  "discounted_price":  "150.00",  "author":  "Mark Summerfield",  "annotated_likes":  0,  "annotated_in_bookmarks_count":  0,  "mark":  null,  "max_rating":  null,  "min_rating":  null,  "owner_name":  "admin",  "readers":  []  },  {  "id":  5,  "name":  "Writer, Sailor, Soldier, Spy: Ernest Hemingway's Secret Adventures",  "price":  "700.00",  "discount":  "0.00",  "discounted_price":  "700.00",  "author":  "Nicholas Reynolds",  "annotated_likes":  1,  "annotated_in_bookmarks_count":  1,  "mark":  "2.00",  "max_rating":  "2.00",  "min_rating":  "2.00",  "owner_name":  "turnMeUpSon",  "readers":  [  {  "first_name":  "Ian",  "last_name":  "Miller"  }  ]  }  ]```


## Running the tests

  

1.  ```cd backend```
2.  ```docker-compose run --rm web-app sh -c "./manage.py test"```
3.  ```docker-compose run --rm web-app sh -c "coverage report"```

  

### Break down into end to end tests
```
docker-compose run --rm web-app sh -c "./manage.py test store.tests.test_serializers"
```
``` ✔ Container django-books-api-database-1  Created                                                                                        0.0s 
[+] Running 1/1
 ✔ Container django-books-api-database-1  Started                                                                                        0.2s 
/usr/local/lib/python3.11/site-packages/social_django/fields.py:13: UserWarning: SOCIAL_AUTH_POSTGRES_JSONFIELD has been renamed to SOCIAL_AUTH_JSONFIELD_ENABLED and will be removed in the next release.
  warnings.warn(
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.019s

OK
Destroying test database for alias 'default'...`
```

  
## Built With

  

* [Django](https://www.djangoproject.com/) 

* [Django REST Framework](https://www.django-rest-framework.org/) 

* [Docker](https://hub.docker.com/) 
* [Postgresql](https://hub.docker.com/_/postgres)

  

## Author

  

**Ian Miller** 

  

## License

  

This project is licensed under the MIT License
