type CustomerType = {
    customer_name: string;
};

type WaypointEnumType = 'delivery' | 'pickup';

type WaypointType = {
    id: IdType;
    address: string;  // falls back to location_name
    location_name: string;
    type: WaypointEnumType;
};
type WaypointFormType = Omit<WaypointType, 'id'>

type TransportOrderWaypoint = {
    id: IdType;
    waypoint: WaypointType;
    order_index: number;
}

type TransportOrderType = {
    id: IdType;
    order_number: number;
    customer_name: string;
    order_date: string;
    waypoints: TransportOrderWaypoint[]
};
type TransportOrderFormType = Omit<TransportOrderType, 'id'>

type ResourceEnumType = 'waypoint' | 'transport_order';
type WaypointTypeEnumType = 'pickup' | 'delivery';

type apiResourceType = (resourceName: ResourceEnumType, actionName: string, id?: IdType) => string;



type ModalStyleEnum = 'simple-add-modal'

/**
// TODO:

type CustomerType = {};
type DateType = {};


*/
