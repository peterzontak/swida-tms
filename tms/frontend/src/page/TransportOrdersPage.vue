<template>
    <h1>Transport Orders
        <span class="material-symbols-outlined action-btn btn-green" @click="openModal('addTransportOrderForm')">
            add_notes
        </span>
    </h1>
    <div class="filters">
        <span class="filter-name" v-if="appliedFilter" @click="clearFilter(appliedFilter)">{{ appliedFilter }}</span>
    </div>
    <table class="table table-striped transport-orders-table">
        <thead class="thead-dark">
            <tr>
                <th>Order number</th>
                <th>Customer name <span class="material-symbols-outlined action-btn"
                        @click="openModal('filterByCustomerName')">filter_alt</span></th>
                <th>Date <span class="material-symbols-outlined action-btn"
                        @click="openModal('filterByTransportOrderDate')">filter_alt</span></th>
                <th>Waypoint</th>
                <th></th>
            </tr>

        </thead>
        <tbody>
            <tr v-for="(transport_order, index) in fetchedTransportOrdersData" :key="index" class="item">
                <td>{{ transport_order.order_number }}</td>
                <td>{{ transport_order.customer_name }}</td>
                <td>{{ transport_order.order_date }}</td>
                <td class="waypoints-table">
                    <div v-for="(transport_order_waypoint, index) in transport_order.waypoints" :key="index"
                        class="item">
                        <span>{{ transport_order_waypoint.waypoint.location_name ??
                            transport_order_waypoint.waypoint.address }}</span>
                        <span>{{ transport_order_waypoint.waypoint.type }}</span>
                    </div>
                </td>
                <td>
                    <div class="row-menu">
                        <span class="material-symbols-outlined action-btn btn-red" @click="removeTransportOrder">
                            cancel
                        </span>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    <FullPageModal ref="addTransportOrderModal">
        <AddTransportOrderForm :onSubmit="formSubmit_addTransportOrder" :available_waypoints="fetchedWaipointsData" />
    </FullPageModal>
    <FullPageModal ref="filterByCustomerNameModal">
        <FilterByCustomerName :onSubmit="formSubmit_filterByCustomerName"
            :existingCustomers="fetchedExistingCustomers" />
    </FullPageModal>
    <FullPageModal ref="filterByTransportOrderDateModal">
        <FilterByTransportOrderDate :onSubmit="formSubmit_filterByTransportOrderDate" />
    </FullPageModal>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref, inject, isRef, reactive } from 'vue';
import { getJson, deleteJson } from '../helpers/api';

import FullPageModal from '../components/popup/FullPageModal.vue';
import AddTransportOrderForm from '../components/form/AddTransportOrderForm.vue';
import FilterByTransportOrderDate from '../components/form/FilterByTransportOrderDate.vue';

import FilterByCustomerName from '../components/form/FilterByCustomerName.vue';

export default defineComponent({
    name: 'TransportOrdersPage',
    components: {
        FullPageModal,
        AddTransportOrderForm,
        FilterByCustomerName,
        FilterByTransportOrderDate,
    },
    methods: {},
    setup() {
        const apiResource = inject<Function>('apiResource', () => { throw new Error('apiResource is not provided!'); });
        const apiFilter = inject<Function>('apiFilter', () => { throw new Error('apiFilter is not provided!'); });

        const appliedFilter = ref<string | null>(null);

        // TODO: better typing
        const addTransportOrderModal = ref<InstanceType<typeof FullPageModal> | null>(null);
        const filterByCustomerNameModal = ref<InstanceType<typeof FullPageModal> | null>(null);
        const filterByTransportOrderDateModal = ref<InstanceType<typeof FullPageModal> | null>(null);

        const fetchedTransportOrdersData = ref<TransportOrderType[]>([]);
        const fetchedWaipointsData = reactive({
            waypoints: [] as WaypointType[], // Initialize as an empty array
        });
        const fetchedExistingCustomers = ref<CustomerType[]>([]);

        const openModal = async (form: string) => {
            switch (form) {
                case 'addTransportOrderForm':
                    await getJson(apiResource('waypoint', 'index')).then((json) => {
                        if (json) {
                            fetchedWaipointsData.waypoints = json;
                        }
                    });
                    
                    addTransportOrderModal.value?.openModal();
                    break;
                case 'filterByCustomerName':
                    await getJson(apiResource('customer', 'index')).then((json) => {
                        if (json) {
                            fetchedExistingCustomers.value = json;
                        }
                    });
                    filterByCustomerNameModal.value?.openModal();
                    break;
                case 'filterByTransportOrderDate':
                    filterByTransportOrderDateModal.value?.openModal();
                    break;
            }

        };

        const clearFilter = (filterName: string) => {
            // TODO: use filterName
            fetchTransportOrdersData();
            appliedFilter.value = null;
        };

        // TODO: add toast
        const removeTransportOrder = (e) => {
            const currentTarget = e.currentTarget;
            const currentTargetRow = e.currentTarget.closest('tr');
            const tbody = currentTarget.closest('tbody');
            const index = ([...tbody.children]).indexOf(currentTargetRow);
            const transportOrder = fetchedTransportOrdersData.value[index];

            if (transportOrder) {
                const id = transportOrder.id;

                if (id) {
                    const url = apiResource('transport_order', 'delete', transportOrder.id);
                    if (confirm("Are you sure you want to delete this order?")) {
                        deleteJson(url).then((res: { success: boolean, id: number, error?: string; }) => {
                            if (res.success) {
                                fetchedTransportOrdersData.value.splice(index, 1);
                            } else {
                                alert(res.error);
                            }
                        });
                    }
                }
                else {
                    console.warn(`${id} not found`);
                }
            }

        };

        // TODO: add toast
        const formSubmit_addTransportOrder: (data: TransportOrderType) => void = (res) => {
            if (res && res.order_number) {
                fetchedTransportOrdersData.value.push(res);
                addTransportOrderModal.value?.closeModal();
            }
        };

        // TODO: add toast
        const formSubmit_filterByCustomerName = async (customer_name: string) => {
            await getJson(apiFilter('transport_order', 'customer_name', customer_name)).then((json) => {
                // console.log({ json });
                if (Array.isArray(json)) {
                    fetchedTransportOrdersData.value = json;
                    appliedFilter.value = customer_name;
                }
            }).catch((error) => {
                console.error(error);
            }).finally(() => {
                filterByCustomerNameModal.value?.closeModal();
            });
        };

        // TODO: add toast
        // TODO: add multiple types of fetch (to is possibly undefined)
        const formSubmit_filterByTransportOrderDate = async ({ from, to }: { from?: string, to?: string; }) => {
            if(!from && !to){
                return fetchTransportOrdersData();
            }


            let filterName: string = 'transport_order_date_from_to';
            let args: string [];
            
            if(from && to){
                args = [from, to];
            }
            if(from && !to){
                filterName = 'transport_order_date_from';
                args = [from];
            }
            else if(!from && to){
                filterName = 'transport_order_date_to';
                args = [to];
            }

            await getJson(apiFilter('transport_order', filterName!, ...args!)).then((json: TransportOrderType[]) => {
                if(Array.isArray(json)){
                    appliedFilter.value = `${from?.replace(/-/g, '/')} - ${to?.replace(/-/g, '/')}`;
                    fetchedTransportOrdersData.value = json;
                }
            }).catch((error) => {
                console.error(error);
            }).finally(() => {
                filterByTransportOrderDateModal.value?.closeModal();
            });
        };

        const fetchTransportOrdersData = async () => {
            await getJson(apiResource('transport_order', 'index')).then((json) => {
                if(Array.isArray(json)){
                    fetchedTransportOrdersData.value = json;
                }
            });
        };


        // Fetch initial data from the Django API when the component is mounted
        onMounted(fetchTransportOrdersData);



        return {
            /** Data */
            fetchedTransportOrdersData,
            fetchedWaipointsData,
            fetchedExistingCustomers,
            appliedFilter,

            /** Default */
            showModal: false,

            /** Methods */
            removeTransportOrder,
            openModal,
            clearFilter,


            /** Modals with Methods*/
            addTransportOrderModal,
            formSubmit_addTransportOrder,

            filterByCustomerNameModal,
            formSubmit_filterByCustomerName,

            filterByTransportOrderDateModal,
            formSubmit_filterByTransportOrderDate,
        };
    }
});
</script>
<style scoped lang="scss">
.filters {
    height: 5em;
    padding: 1em;
    display: flex;

    .filter-name:not(:empty) {
        cursor: pointer;
        border-radius: 0.2em;
        background: rgba(189, 189, 189, .7);
        font-weight: bold;
        padding: 0.5em;

        &:hover {
            background: rgba(189, 189, 189, 1);
        }
    }
}
</style>
