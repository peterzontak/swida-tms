<template>
    <h1>Filter by Transport Order Date</h1>
    <form @submit.prevent="handleSubmit">
        <label for="order_date_from">
            <span>Not Before the Date</span>
            <input type="date" v-model="formData.order_date_from" id="order_date_from"/>
        </label>
        <label for="order_date_to">
            <span>Until Date</span>
            <input type="date" v-model="formData.order_date_to" id="order_date_to"/>
        </label>
        <button type="submit">Filter</button>
    </form>
</template>

<script lang="ts">
import { ref } from 'vue';

type OrderFormData = {
    order_date_from: TransportOrderType['order_date'];
    order_date_to: TransportOrderType['order_date'];
}

export default {
    props: {
        onSubmit: {
            type: Function,
            default: null,
        },
        existingCustomers: {
            type: Array,
            default: [],
        }
    },
    setup({ onSubmit }: { onSubmit: Function;}) {
        
        // TODO: Fetch the minimum and maximum order dates from the API and disable invalid dates in the form.
        const formData = ref<OrderFormData>({
            order_date_from: '',
            order_date_to: '',
        });

        const handleSubmit = ()=>{
            const {order_date_from: from, order_date_to: to} = formData.value;
            onSubmit && onSubmit({from,to});
        };

        return {
            handleSubmit,
            formData,
        };
    },
};
</script>

<style scoped lang="scss">
    h1{
        margin-bottom: 2em;
    }
    input{
        cursor: pointer;
    }
    label{
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        opacity: .75;
        &:hover{
            opacity: 1;
        }
    }
</style>
