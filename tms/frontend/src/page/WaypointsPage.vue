<template>
    <h1>Waypoints
        <span class="material-symbols-outlined action-btn btn-green" @click="openModal">
            add_notes
        </span>
    </h1>
    <table class="table table-striped transport-orders-table">
        <thead class="thead-dark">
            <tr>
                <th>Address</th>
                <th>Location Name</th>
                <th>Waypoint Type</th>
                <th></th>
            </tr>

        </thead>
        <tbody>
            <tr v-for="(waypoint, index) in fetchedData" :key="index" class="item">
                <td>{{ waypoint.address }}</td>
                <td>{{ waypoint.location_name }}</td>
                <td>{{ waypoint.type }}</td>
                <td>
                    <div class="row-menu">
                        <span class="material-symbols-outlined action-btn btn-red" @click="removeWaypoint">
                            cancel
                        </span>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    <FullPageModal ref="modalRef" :class="modalClass">
        <AddWaypointForm :onSubmit="formSubmit_addTransportOrder" :waypoint_types="waypoint_types"/>
    </FullPageModal>
</template>
<script lang="ts">
import { defineComponent, reactive, onMounted, ref, inject } from 'vue';
import { getJson, deleteJson } from '../helpers/api';

import FullPageModal from '../components/popup/FullPageModal.vue';
import AddWaypointForm from '../components/form/AddWaypointForm.vue';

export default defineComponent({
    name: 'TransportOrdersPage',
    components: {
        FullPageModal,
        AddWaypointForm,
    },
    methods: {},
    setup() {
        const apiResource = inject<apiResourceType>('apiResource',()=>{throw new Error('apiResource is not provided!')});
        const modalRef = ref<InstanceType<typeof FullPageModal> | null>(null);
        const fetchedData = reactive<WaypointType[]>([]);

        const removeWaypoint = (e) => {
            const currentTarget = e.currentTarget;
            const currentTargetRow = e.currentTarget.closest('tr');
            const tbody = currentTarget.closest('tbody');
            
            const index = ([...tbody.children]).indexOf(currentTargetRow);
            const waypoint = fetchedData[index];
            const id = waypoint.id;

            if (id) {
                const url = apiResource('waypoint', 'delete', waypoint.id);
                
                if (confirm("Are you sure you want to delete this order?")) {
                    deleteJson(url).then((res: { success: boolean, id: number, error?: string; }) => {
                        if (res.success) {
                            fetchedData.splice(index, 1);
                        } else {
                            alert(res.error);
                        }
                    });
                }
            }
            else {
                console.warn(`${id} not found`);
            }

        };


        const openModal = () => {
            modalRef.value?.openModal();
        };

        const formSubmit_addTransportOrder: (data: WaypointType) => void = (res) => {
            if (res && res.id) {
                fetchedData.push(res);
                modalRef.value?.closeModal();
            }
        };


        const fetchData = async () => {
            await getJson(apiResource('waypoint', 'index')).then((json) => {
                json && fetchedData.push(...json);
            });
        };

        // Fetch initial data from the Django API when the component is mounted
        onMounted(fetchData);

        return {
            fetchedData,
            formSubmit_addTransportOrder,
            showModal: false,
            openModal,
            modalRef,
            removeWaypoint,
            modalClass: 'simple-add-modal',
            waypoint_types: ['pickup', 'delivery'],
        };
    }
});
</script>
<style scoped></style>
