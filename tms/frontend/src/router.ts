import { createRouter, createWebHistory } from 'vue-router';
import TransportOrdersPage from './page/TransportOrdersPage.vue';
import WaypointsPage from './page/WaypointsPage.vue';
import appSettings from '../config/config.json';


const routes = [
    { path:  '/' + appSettings.routes.transport_orders, component: TransportOrdersPage },
    { path:  '/' + appSettings.routes.waypoints, component: WaypointsPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
