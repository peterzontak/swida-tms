# Transport Management System (TMS)

## Models Structure
(TransportOrder has many Waypoints)

### TransportOrder
- **order_number**
- **customer_name**
- **date**

### Waypoint
- **location_name** (Can be left empty)
- **address**       (Used as the name if the location name is empty)
- **type**          `"pickup"` | `"delivery"`

### TransportOrderWaypoint
- **transport_order**   (Reference to the associated transport order.)
- **waypoint**          (Reference to the associated waypoint.)
- **order_index**       (Index indicating the order of waypoints.)


## User Interface

In line with the principle of prioritizing functionality over aesthetics, I chose a minimalist Bootstrap navbar and tables with minimal styling. For icons, I utilized Google Icons. Both Bootstrap and the icons are included in the main `base.html` file via CDNs, ensuring they are accessible throughout the application.


## Application Structure

I divided the application into two Django apps:
- **`app`**     Responsible for the user interface.
- **`crud`**    Handles API endpoints.

The `app` consists of:
- Homepage
- Transport Orders listing
- Waypoints listing

Both listings are interactive and incorporate the core logic central to your assignment. The backend and frontend share the same configuration file located at `tms/frontend/config/config.json`.

The application forms still contain temporary code snippets that generate and pre-fill forms for quicker testing. For error display, I opted for a straightforward approach using simple `alert` and `console.log` methods, which are not intended for production use.

As an intermediary between the frontend and the `crud` Django application on the backend, I created a helper file containing functions for making requests using the JavaScript Fetch API. The `main.ts` file provides helper functions for generating correct URLs for backend API calls related to CRUD operations and filtering.

During testing i registered JSON exception middleware for better error console output and used `whitenoise package` for serving static files.

#### Migrations were created, applied, and the database was pre-populated with dummy data
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py seed`

#### Superuser was created
- `python manage.py createsuperuser`

#### The JavaScript bundle is pre-built
- `npm run build-prod`

#### Static assets were collected
- `python manage.py collectstatic --noinput`


## TODO

Currently, I have no time left for potential enhancements. Here are tasks to consider:
1. Separate the **MultipleWaypointsSelect** component.
2. Implement sorting of TransportOrders by:
   - Date
   - Customer Name
   - Order Number
3. Display error messages within forms.
4. Use toast notifications instead of alerts.
5. Make Waypoints reorderable.
6. Enable editing of TransportOrders and Waypoints.
7. Create pagination for both models.
8. Improve client-side and server-side validation.
9. Prompt user confirmation before deleting a Waypoint if there are related TransportOrders.
10. Remove temporary code snippets if they are no longer needed.
