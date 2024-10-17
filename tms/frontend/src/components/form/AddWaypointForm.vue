<template>
    <form @submit.prevent="handleSubmit">
        <div class="form-row">
            <label for="address">Address:</label>
            <input id="address" v-model="formData.address" type="text" />
        </div>
        <div class="form-row">
            <label for="location_name">Location Name:</label>
            <input id="location_name" v-model="formData.location_name" type="text" />
        </div>
        <div class="form-row">
            <label for="type">Waypoint Type:</label>
            <select v-model="formData.type">
                <option v-for="type in waypoint_types" :key="type">{{ type }}</option>
            </select>
        </div>
        <button type="submit">Submit</button>
    </form>
</template>

<script lang="ts">
import { ref, reactive, inject } from 'vue';
// TODO: inject
import { postJson } from '../../helpers/api';

export default {
    props: {
        onSubmit: {
            type: Function,
            default: () => {},
        },
        waypoint_types: {
            type: Array as () => WaypointEnumType[],
            default: () => [],
        }
    },
    setup({ onSubmit, waypoint_types }: { onSubmit: Function; waypoint_types: WaypointEnumType[]; }) {

        const apiResource = inject<Function>('apiResource', () => { throw new Error('apiResource is not provided!'); });

        const formData: WaypointFormType = reactive({
            address: '',
            location_name: '',
            // TODO: remove in PROD
            type: (() => Math.random() < 0.5 ? waypoint_types[0] : waypoint_types[1])(),
        });



        const handleSubmit = () => {
            const { address, type } = formData;
            const url = apiResource('waypoint', 'add');

            /** Validation
                TODO: display error messages
            */
            if (
                (typeof address === 'string' && address.length > 0) &&
                (typeof type === 'string' && waypoint_types.includes(type))
            ) {
                postJson(url, formData)
                    .then((json) => {
                        onSubmit && onSubmit(json);
                    });
            }

        };


        return {
            handleSubmit,
            formData,
            waypoint_types,
        };
    },
};
</script>

<style scoped lang="scss">
.form-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
}
</style>
