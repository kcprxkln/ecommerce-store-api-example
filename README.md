# FastAPI + mongoDB e-commerce store scheme

Api created with FastApi python framework that connects to the MongoDB databases, and gives preview of what e-commerce store API can look like.

There are two groups of endpoints, that have separate collections in the db: *Customers* and *Items*.

Additionally, there is the test for every single endpoint in order to make sure everything works correctly.
Tests are using classical CRUD scheme to make sure that after tests, there won't be any unexpected data.

### Possible methods
**Items related:**

`/items/add` - Add new item.

`/items/search` - Search for item with arguments that you want.

`/items/update/{item_id}` - Update item.  *(serial_id must be unique)*

`/items/delete/{item_id}` - Delete item.

**Customer related:**

`/customers/add` - Add new customer.

`/customers/search` - Search for customer with arguments that you want.

`/customers/update/{customer_id}` - Update customer. *(id must be unique)*

`/customers/delete/{customer_id}` - Delete customer.


More details can be found after running the project locally, and then opening */docs* endpoint.
Please note that this is only the example and can be further expanded.
