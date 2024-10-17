<template>
    <div v-if="isVisible" class="overlay" @click.self="closeModal">
        <div :class="['modal-content', modalStyle]">
            <span class="material-symbols-outlined action-btn btn-red btn-close" @click="closeModal">
                cancel
            </span>
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';

type propsType = {
    modalStyle?: ModalStyleEnum;
};

export default {
    props: {
        modalStyle: {
            type: String,
            default: 'simple-add-modal'
        },
    },
    setup({ modalStyle = 'simple-add-modal' }: propsType) {
        const isVisible = ref(false);

        const openModal = () => {
            isVisible.value = true;
        };

        const closeModal = () => {
            isVisible.value = false;
        };

        return {
            isVisible,
            openModal,
            closeModal,
            modalStyle,
        };
    },
};
</script>

<style scoped lang="scss">
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: white;
    padding: 2em;
    border-radius: 0.2em;
    width: 75%;
    max-width: 600px;

    .btn-close {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
    }

}

:deep(.simple-add-modal){
    form {
        display: flex;
        flex-direction: column;
        gap: 1em;

        div.form-row{
            display: flex;
            justify-content: space-between;

            input {
                text-align: center;
                width: 70%;
            }

            option {
                padding: 0.5rem;
            }
        }
    }
}
</style>
