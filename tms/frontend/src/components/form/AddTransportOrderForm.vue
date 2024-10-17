<template>

    <form @submit.prevent="handleSubmit">
        <div class="form-row">
            <label for="order_number">Order number:</label>
            <input id="order_number" v-model="formData.order_number" type="number" />
        </div>
        <div class="form-row">
            <label for="customer_name">Customer name:</label>
            <input id="customer_name" v-model="formData.customer_name" type="text" autofocus />
        </div>
        <div class="form-row">
            <label for="order_date">Order date:</label>
            <input id="order_date" v-model="formData.order_date" type="date" />
        </div>
        <!-- TODO: Extract to a separate MultipleWaypointsSelect component. -->
        <div class="form-row waypoints-container">
            <label for="waypoint">Waypoints:</label>

            <div class="waypoint" v-for="(waypoint, index) in waypoints" :key="index">
                {{ waypoint.location_name ?? waypoint.address ?? waypoint.address }}
                <span class="material-symbols-outlined action-btn btn-red"
                    @click="removeWaypoint(waypoint.id)">cancel</span>
            </div>
            <select name="waypoint" id="waipoint" @change="addWaypoint($event)" v-model="selectedWaypoint">
                <option value="-1" disabled>Pick a waypoint</option>

                <option v-for="(waypoint, index) in really_available_waypoints()" :key="index" :value="waypoint.id">{{
                    waypoint.location_name ?? waypoint.address }}
                </option>

            </select>
        </div>
        <button type="submit">Submit</button>
    </form>
</template>

<script lang="ts">
import { ref, inject } from 'vue';
// TODO: inject
import { postJson } from '../../helpers/api';

export default {
    props: {
        onSubmit: {
            type: Function,
            default: () => { },
        },
        available_waypoints: {
            type: Object as () => { waypoints: WaypointType[]; },
            required: true,
        }
    },
    setup({ onSubmit, available_waypoints }: { onSubmit: Function; available_waypoints: { waypoints: WaypointType[]; }; }) {

        // holds selected waypoints
        const waypoints = ref<WaypointType[]>([] as WaypointType[]);

        const apiResource = inject<Function>('apiResource', () => { throw new Error('apiResource is not provided!'); });

        const really_available_waypoints = () => available_waypoints.waypoints.filter(item => !waypoints.value.includes(item));

        // TODO: make it reactive
        let selectedWaypoint = '';

        const addWaypoint = (event) => {
            const selectedValue = event.target.value;
            selectedWaypoint = '';

            if (!selectedValue) return;

            const new_waypoint = really_available_waypoints().find((waypoint) => waypoint.id == selectedValue);

            if (new_waypoint) {
                waypoints.value.push(new_waypoint);
            }
        };

        const removeWaypoint = (id: IdType) => {
            selectedWaypoint = '';
            const index = waypoints.value.findIndex((waypoint) => waypoint.id == id);
            if (index !== -1) {
                waypoints.value.splice(index, 1);
            }
        };

        const formData = ref<Omit<TransportOrderFormType, 'waypoints'>>({
            // TODO: remove random functions in PROD
            order_number: (() => Number(Math.floor((Math.random() * 1000)) + '' + (new Date()).toISOString().slice(0, 10).replace(/-/g, '')))(),
            customer_name: '',
            // TODO: remove random functions in PROD
            order_date: (() => new Date(new Date('2000-01-01').getTime() + Math.random() * (new Date('2024-12-31').getTime() - new Date('2000-01-01').getTime())).toISOString().split('T')[0])(),
        });

        const handleSubmit = () => {
            const { order_number, customer_name, order_date } = formData.value;
            const url = apiResource('transport_order', 'add');

            /** Validation TODO: display error messages */
            if (
                (!isNaN(order_number) && order_number > 0) &&
                (typeof customer_name === 'string' && customer_name.length > 0) &&
                (typeof order_date === 'string' && order_date.length > 0)
            ) {
                const waypoint_ids = waypoints.value.map((waypoint) => waypoint.id);

                postJson(url, { order_number, customer_name, order_date, waypoints: waypoint_ids })
                    .then((json) => {
                        onSubmit && onSubmit(json);
                    });
            }

        };


        return {
            handleSubmit,
            formData,
            really_available_waypoints,
            waypoints,
            addWaypoint,
            removeWaypoint,
            selectedWaypoint,
        };
    },
};
</script>

<style scoped lang="scss">
.waypoints-container {
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    gap: 0.5rem;

    label {
        text-align: left;
    }

    select,
    option {
        padding: 0.5rem;
    }
}
</style>
