<template>
    <h1>Filter by Customer Name</h1>
    <form @submit.prevent="handleSubmit">
        <select name="customer_name" v-model="formData.customer_name">
            <option value="-1" disabled>Pick a customer</option>
            <option v-for="(customer, index) in existingCustomers" :key="index" :value="customer.customer_name">{{ customer.customer_name }}</option>
        </select>
        <button type="submit">Filter</button>
    </form>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
    props: {
        onSubmit: {
            type: Function,
            default: () => {},
        },
        existingCustomers: {
            type: Array,
            default: [] as CustomerType[],
        }
    },
    setup({ onSubmit, existingCustomers }: { onSubmit: Function; existingCustomers: CustomerType[]; }) {
        const formData = ref<CustomerType>({
            customer_name: '',
        });

        const handleSubmit = ()=>{
            onSubmit && onSubmit(formData.value.customer_name);         
        };

        return {
            handleSubmit,
            formData,
            existingCustomers,
        };
    },
};
</script>

<style scoped></style>
